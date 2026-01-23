# sen0343/sensor.py
import esphome.codegen as cg
import esphome.config_validation as cv

from esphome.components import sensor, i2c
from esphome.const import CONF_ID, CONF_ADDRESS
from esphome.const import UNIT_PASCAL

DEPENDENCIES = ['i2c']
AUTO_LOAD = ['i2c']

from . import sen0343_ns, SEN0343

CONF_SCALE_FACTOR = 'scale_factor'

# Build a PLATFORM_SCHEMA in a way that works across ESPhome versions:
# - If sensor.PLATFORM_SCHEMA exists, extend it.
# - Otherwise fall back to sensor.SENSOR_SCHEMA (older/newer builds differ).
try:
    BASE_PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA
except AttributeError:
    BASE_PLATFORM_SCHEMA = sensor.SENSOR_SCHEMA

PLATFORM_SCHEMA = BASE_PLATFORM_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(SEN0343),
    cv.Optional(CONF_ADDRESS, default=0x01): cv.hex_uint8_t,
    cv.Optional(CONF_SCALE_FACTOR, default=64.0): cv.float_,
}).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], SEN0343)
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)

    address = config.get(CONF_ADDRESS)
    cg.add(var.set_address(address))

    scale = config.get(CONF_SCALE_FACTOR)
    cg.add(var.set_scale_factor(scale))
