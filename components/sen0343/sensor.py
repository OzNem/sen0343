import esphome.codegen as cg
import esphome.config_validation as cv

from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_ADDRESS,
    CONF_UPDATE_INTERVAL,
    UNIT_PASCAL,
    DEVICE_CLASS_PRESSURE,
)
from esphome import automation

DEPENDENCIES = ['i2c']
AUTO_LOAD = ['i2c']

from . import sen0343_ns, SEN0343

CONF_PRESSURE = 'pressure'

# sensor platform schema: reuse sensor.SENSOR_SCHEMA so user can set id, name, update_interval, filters, etc.
PLATFORM_SCHEMA = sensor.SENSOR_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(SEN0343),
    cv.Optional(CONF_ADDRESS, default=0x28): cv.hex_uint8_t,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], SEN0343)
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)

    address = config.get(CONF_ADDRESS)
    cg.add(var.set_address(address))
