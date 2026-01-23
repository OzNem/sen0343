import esphome.codegen as cg
from esphome.components import sensor
from esphome.const import CONF_ID

sen0343_ns = cg.esphome_ns.namespace('sen0343')
# C++ class name SEN0343, inherits Component and sensor::Sensor
SEN0343 = sen0343_ns.class_('SEN0343', cg.Component, sensor.Sensor)
