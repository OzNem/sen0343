import esphome.codegen as cg
import esphome.config_validation as cv

from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_ADDRESS,
    UNIT_PASCAL,
)
from esphome import automation

DEPENDENCIES = ['i2c']
AUTO_LOAD = ['i2c']

from . import sen0343_ns, SEN0343

CONF_SCALE_FACTOR = 'scale_factor'

# Use sensor.PLATFORM_SCHEMA so standard sensor options (name, id, filters, update_interval, etc.)
# are accepted, and we can extend with our custom options.
PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA.extend({
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
