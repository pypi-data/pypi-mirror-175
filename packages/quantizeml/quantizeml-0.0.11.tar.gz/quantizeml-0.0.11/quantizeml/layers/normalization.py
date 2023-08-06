#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
import tensorflow as tf
import keras
from tensorflow.python.framework import ops

from .layers import deserialize_quant_object, Calibrable, CalibrableVariable
from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH


__all__ = ["QuantizedLayerNormalization", "LayerMadNormalization"]


@tf.keras.utils.register_keras_serializable()
class LayerMadNormalization(keras.layers.LayerNormalization):
    r"""Approximates the :obj:`keras.layers.LayerNormalization` (LN), replacing the computation of
    the standard deviation by the mean average deviation (mad).

    Taking into account the complexity of the calculate required in the standard deviation,
    the LayerMadNormalization (LMN) is intended to replace the :math:`std(x)` by :math:`mad(x)`,
    defined as:

    .. math:: mad(x) = |x - mean(x)| * 2^\text{-nb_channels}

    Then, the equation of the layer is defined as:

    .. math:: LMN(x) = \gamma\frac{x - mean(x)}{mad(x)} + \beta

    Also, to develop a hardware compatible quantization, we make the approximation of mean
    on a Power Of Two (PoT):

    .. math:: mean(x) = sum(x) * 2^\text{-nb_channels}

    Where nb_channels = :math:`round(log2(inputs.shape[axis]))`

    .. note::
        A tuning step in the switching procedure between the LN to LMN layer will be required
        to find the :math:`(\gamma, \beta)` parameters that match the standard deviation changes.
    """

    def build(self, input_shape):
        super().build(input_shape)

        # Save an approximation of nb_channels as PoT to calculate the mean of inputs as:
        # mean_inputs = sum(inputs) * 2 ** -mean_shift
        if len(self.axis) > 1:
            raise ValueError(f"{self.__class__.__name__} does not support multiple axis.")
        nb_channels = tf.cast(input_shape[self.axis[0]], tf.float32)
        self.mean_shift = tf.math.round(tf.math.log(nb_channels) / tf.math.log(2.))

    def _moments(self, inputs, axis, *args, name=None, **kwargs):
        """Compute the mean and mean absolute deviation (mad).

        Args:
            inputs (:obj:`tensorflow.Tensor`): input tensor.
            axis (array of ints): axis along which to compute mean and mad.
            name (str, optional): name used to scope the operations that compute the moments.
                Defaults to None.
            *args, **kwargs (dict, optional): additional arguments of :func:`tf.math.reduce_mean`.

        Returns:
            :obj:`tensorflow.Tensor`, :obj:`tensorflow.Tensor`: mean around the axis and
            mean absolute deviation (mad).
        """
        # Compute the mean and mad, taking into account the approximation:
        # nb_channels \approx 2 ** round(log2(inputs.shape[axis]))
        nb_channels_inv = 2.0 ** -self.mean_shift
        with ops.name_scope(name, "_moments", [inputs, axis]):
            mean = tf.math.reduce_sum(
                inputs, axis, *args, **kwargs, name="mean")
            mean = mean * nb_channels_inv
            mad = tf.math.reduce_sum(tf.math.abs(
                inputs - mean), axis, *args, **kwargs, name="mad")
            mad = mad * nb_channels_inv
        return mean, mad

    def call(self, inputs, training=None):
        """Use the same call as the parent, changing tf.nn.moments instead of self._moments."""
        # Compute the axis along which to reduce the mean / mad
        input_shape = inputs.shape
        ndims = len(input_shape)

        # Broadcasting only necessary for norm when the axis is not just the last dimension
        broadcast_shape = [1] * ndims
        for dim in self.axis:
            broadcast_shape[dim] = input_shape.dims[dim].value

        def _broadcast(v):
            if (v is not None and len(v.shape) != ndims and self.axis != [ndims - 1]):
                return tf.reshape(v, broadcast_shape)
            return v

        input_dtype = inputs.dtype
        if input_dtype in ('float16', 'bfloat16') and self.dtype == 'float32':
            # If mixed precision is used, cast inputs to float32 so that this is at
            # least as numerically stable as the fused version.
            inputs = tf.cast(inputs, 'float32')

        # Calculate the moments on the last axis (layer activations).
        mean, mad = self._moments(inputs, self.axis, keepdims=True)
        scale, offset = _broadcast(self.gamma), _broadcast(self.beta)

        # Compute layer normalization as layer mad normalization
        outputs = scale * (inputs - mean) / (mad + self.epsilon) + offset
        outputs = tf.cast(outputs, input_dtype)

        # If some components of the shape got lost due to adjustments, fix that.
        outputs.set_shape(input_shape)

        return outputs


@tf.keras.utils.register_keras_serializable()
class QuantizedLayerNormalization(Calibrable, LayerMadNormalization):
    """ A LayerNormalization layer that operates on quantized inputs and weights.

     Args:
        quant_config (dict, optional): the serialized quantization configuration.
            Defaults to empty configuration.
    """
    def __init__(self, *args, quant_config={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False, False)
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        self.mad_rec_frac_bits = self.quant_config.get("mad_rec_frac_bits", 16)
        assert self.buffer_bitwidth > 0, "The buffer_bitwidth must be a strictly positive integer."
        assert self.mad_rec_frac_bits >= 0, "The mad_rec_frac_bits must be a non-negative integer."
        self.gamma_quantizer = deserialize_quant_object(
            self.quant_config, "gamma_quantizer", True, True)
        self.beta_quantizer = deserialize_quant_object(
            self.quant_config, "beta_quantizer", True, True)
        self.mad_quantizer = deserialize_quant_object(
            self.quant_config, "mad_quantizer", False, True)

        # Add objects that will store the shift values.
        self.input_shift = CalibrableVariable()
        self.x_rescaled_shift = CalibrableVariable()
        self.beta_shift = CalibrableVariable()
        self.output_shift = CalibrableVariable()

    def call(self, inputs, training=None):
        """The quantized version of the LayerNormalization with Integer-only operations.

            This normalizes the input tensor then returns a quantized output.

            inputs (:obj:`FixedPoint`): the inputs tensor.
            training (bool, optional): the training mode. Defaults to None.

            Returns:
                :obj:`FixedPoint`: output tensor.
        """
        # raise an error if the inputs are not FixedPoint
        if not isinstance(inputs, FixedPoint):
            raise TypeError(f"QuantizedLayerNormalization only accepts FixedPoint\
                              inputs. Receives {type(inputs)} inputs.")

        # Increase the value_bits of inputs to avoid saturation, then align them
        inputs, shift = inputs.promote(self.buffer_bitwidth).align()
        self.input_shift(shift)

        # Compute the Mean of the inputs
        sum_x = tf.math.reduce_sum(inputs, self.axis, keepdims=True)
        # Approximate mean_x = sum_x / 2**mean_shift
        # We could apply the shift virtually, but at this stage it is ok to drop the precision
        # on the mean as it does not change the accuracy of the operation and prevents
        # the explosion of the frac_bits.
        # From an hardware perspective, it will correspond to an unconditional right-shift.
        mean_x = sum_x.shift(-self.mean_shift)

        # Compute the Absolute Deviation (MAD)
        x_shifted = inputs - mean_x
        mad_sum = tf.math.reduce_sum(
            x_shifted.abs(), self.axis, keepdims=True, name="mad")
        # Approximate mad = mad_sum / 2**mean_shift
        mad = mad_sum >> self.mean_shift

        mad = self.mad_quantizer(mad, training=training)

        # Convert the learnable parameters gamma and beta in FixedPoint
        gamma = self.gamma_quantizer(self.gamma, training=training)
        beta = self.beta_quantizer(self.beta, training=training)

        # If the MAD is 0, then all inputs are equal to the mean, so all x_shifted are equal to 0.
        # In that case it is safe to set the mad_inv to 1.
        one = FixedPoint.quantize(1, self.mad_rec_frac_bits, self.buffer_bitwidth)
        equal_zeros = tf.equal(mad.values, 0.0)
        mad_values = tf.where(equal_zeros, [1.0], mad.values)
        mad = FixedPoint(mad_values, mad.frac_bits, self.buffer_bitwidth)

        # Compute the reciprocal of the MAD
        mad_inv = one / mad

        # Rescale inputs
        x_rescaled = x_shifted * mad_inv

        # Downscale to recover the initial fractional bits
        x_rescaled, shift = x_rescaled.downscale(x_shifted.frac_bits, self.buffer_bitwidth)
        self.x_rescaled_shift(shift)

        # Multiply by gamma
        outputs = x_rescaled * gamma

        # Before adding the bias, we need aligned results
        outputs, shift = outputs.align(beta)
        self.output_shift(shift)
        beta, shift = beta.promote(self.buffer_bitwidth).align(outputs)
        self.beta_shift(shift)
        outputs = tf.add(outputs, beta)
        outputs.values.set_shape(inputs.shape)

        # If no quantizer output is provided return the FixedPoint output tensor directly
        if self.out_quantizer is None:
            return outputs

        return self.out_quantizer(outputs, training=training)

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
