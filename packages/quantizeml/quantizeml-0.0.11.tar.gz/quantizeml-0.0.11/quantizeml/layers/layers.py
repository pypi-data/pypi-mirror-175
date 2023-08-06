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
import keras
import tensorflow as tf

from ..tensors import FixedPoint, MAX_BUFFER_BITWIDTH


__all__ = ["Add", "QuantizedAdd", "deserialize_quant_object"]


def deserialize_quant_object(quant_config, object_name, weight_quantizer, mandatory=True):
    """Wrapper function of tf.keras.utils.deserialize_keras_object.
    It allows to select the right config from the config file dict,
    and raises an error if no config found or set to None.
    If one is found, it returns the corresponding deserialized Keras
    object.

    Args:
        quant_config (dict): quantization config dictionnary.
        object_name (str): keras object name to deserialize.
        weight_quantizer(bool): if true set a WeightQuantizer otherwise
            set an OutputQuantizer.
        mandatory (bool, optional): flag to specify if the object to
            deserialize is mandatory. If yes raises an Error otherwise
            returns None. Defaults to True.

    Returns:
        :obj:`tensorflow.keras.class`: the targeted deserialized keras
        object.
    """
    object_dict = quant_config.get(object_name)
    if object_dict is None:
        if mandatory:
            raise KeyError(f"'{object_name}' should be specified.")
        return None

    # Check that object_dict has the right keys
    list_available_keys = {
        "trainable": bool,
        "bitwidth": int,
        "signed": bool,
        "axis": str,
        "momentum": float,
        "dtype": str,
        "scale_bits": int
    }
    for key in object_dict:
        if key == "scale_bits" and "weight_quantizer" not in object_name:
            raise ValueError(f"'{object_name}' produces FixedPoint output. "
                             "It doesn't support 'scale_bits' key.")
        if key not in list_available_keys:
            raise KeyError(f"'{key}' is not a valid key for '{object_name}'.")
        if not isinstance(object_dict[key], list_available_keys[key]):
            raise ValueError(f"'{key}' should be of type {list_available_keys[key]}. "
                             f"Received {type(object_dict[key])}.")

    # Deserialize the object
    deserialize_dict = object_dict.copy()
    deserialize_dict["name"] = object_name
    if weight_quantizer:
        class_name = "Custom>WeightQuantizer"
    else:
        class_name = "Custom>OutputQuantizer"
    deserialize_dict = {"class_name": class_name, "config": deserialize_dict}
    deserialize_obj = tf.keras.utils.deserialize_keras_object(deserialize_dict)
    return deserialize_obj


class Calibrable():
    """A class that exhibits a 'calibration' property.

    All objects inheriting from this class share the same 'calibration' property.

    Setting the property on one instance will automatically set the property
    on all members of the class that are also Calibrable objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._calibration = False
        self.calibrables = []

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if isinstance(value, Calibrable):
            self.calibrables.append(name)

    @property
    def calibration(self):
        """Flag to specify if the object is in calibration mode or not.

        Returns:
            bool: True if the object is in calibration mode, False otherwise.
        """
        return self._calibration

    @calibration.setter
    def calibration(self, value):
        """Set the calibration mode of the object, and all its members.

        Args:
            value (bool): True if the object will be in calibration mode, False otherwise.
        """
        self._calibration = value
        for name in self.calibrables:
            calibrable = getattr(self, name)
            calibrable.calibration = value


class CalibrableVariable(Calibrable, keras.layers.Layer):
    """Wrapper class to store and retrieve a calibrable variable, e.g.: shift
    information.
    """

    def build(self, input_shape):
        super().build(input_shape)
        self._var = self.add_weight(
            shape=input_shape,
            dtype=tf.float32,
            initializer="zeros",
            synchronization=tf.VariableSynchronization.ON_READ,
            trainable=False,
            aggregation=tf.VariableAggregation.MEAN,
            experimental_autocast=False,
        )

    @property
    def value(self):
        """Get to the variable value.

        Returns:
            :obj:`tf.Tensor`: value of the stored variable.
        """
        return self._var.value()

    def call(self, inputs):
        """Updates the value of the variable if calibration is True.

        Args:
            inputs (:obj:`tf.Tensor`): new values.

        Returns:
            :obj:`tf.Tensor`: value of the variable when calibration is True, None otherwise.
        """
        if not self.calibration:
            return None
        self._var.assign(inputs)
        return inputs


@tf.keras.utils.register_keras_serializable()
class Add(keras.layers.Layer):
    """Wrapper class of `keras.layers.Add` that allows to average inputs.
    We only support a tuple of two inputs with same shape.

    Args:
        average (bool, optional): if `True`, compute the average across all inputs.
            Defaults to `False`.
    """

    def __init__(self, *args, average=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.average = average

    def build(self, input_shape):
        if not isinstance(input_shape, (list, tuple)) or len(input_shape) != 2:
            raise ValueError(f"{self.__class__.__name__} expects two input tensors")

    def call(self, inputs, training=False):
        a, b = inputs
        output = tf.add(a, b)
        if self.average:
            output /= 2
        return output

    def get_config(self):
        config = super().get_config()
        config["average"] = self.average
        return config


@tf.keras.utils.register_keras_serializable()
class QuantizedAdd(Calibrable, Add):
    """Sums two inputs and quantize the output.

    The two inputs must be provided as a list or tuple of FixedPoint or Tensors.

    The outputs are quantized according to the specified quantization configuration.

    Args:
        quant_config (dict, optional): the serialized quantization configuration.
            Defaults to empty configuration.
    """

    def __init__(self, *args, quant_config={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.buffer_bitwidth = self.quant_config.get(
            "buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False, False)
        # Add objects that will store the shift values.
        self.a_shift = CalibrableVariable()
        self.b_shift = CalibrableVariable()

    def call(self, inputs, training=None):
        a, b = inputs
        if not (isinstance(a, FixedPoint) and isinstance(b, FixedPoint)):
            # If any of the inputs is not a FixedPoint, raise an error
            raise TypeError(f"QuantizedAdd only accepts FixedPoint\
                              inputs. Receives {(type(a), type(b))} inputs.")

        # Promote a before performing the addition
        a = a.promote(self.buffer_bitwidth)
        b = b.promote(self.buffer_bitwidth)

        # Align intermediate inputs before adding them
        a, shift_ab = a.align(b)
        b, shift_ba = b.align(a)

        outputs = tf.add(a, b)
        if self.average:
            outputs = outputs >> 1

        # Compute shifts
        self.a_shift(shift_ab)
        self.b_shift(shift_ba)

        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs, training=training)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
