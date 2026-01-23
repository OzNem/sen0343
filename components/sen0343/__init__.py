# must be here 
import esphome.codegen as cg
from esphome.components import sensor
sen0343_ns = cg.esphome_ns.namespace('sen0343')
SEN0343 = sen0343_ns.class_('SEN0343', cg.Component, sensor.Sensor)
