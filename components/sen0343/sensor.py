# sen0343/sensor.py
import esphome.codegen as cg
import esphome.config_validation as cv

# Import sensor module as sensor_mod to avoid shadowing names
from esphome.components import sensor as sensor_mod, i2c
from esphome.const import CONF_ID, CONF_ADDRESS

DEPENDENCIES = ['i2c']
AUTO_LOAD = ['i2c']

from . import sen0343_ns, SEN0343

CONF_SCALE_FACTOR = 'scale_factor'

# Try multiple possible schema attribute names used across ESPhome versions.
_schema_candidates = [
    'PLATFORM_SCHEMA',
    'SENSOR_SCHEMA',
    '_SENSOR_SCHEMA',
    '_PLATFORM_SCHEMA',
]

BASE_PLATFORM_SCHEMA = None
for name in _schema_candidates:
    BASE_PLATFORM_SCHEMA = getattr(sensor_mod, name, None)
    if BASE_PLATFORM_SCHEMA is not None:
        break

# If none found, fall back to a minimal schema that accepts common sensor keys.
if BASE_PLATFORM_SCHEMA is None:
    # Minimal fallback: accept id/name/filters/update_interval and allow extension
    BASE_PLATFORM_SCHEMA = cv.Schema({
        cv.GenerateID(): cv.declare_id(SEN0343),
        cv.Optional(CONF_ADDRESS, default=0x01): cv.hex_uint8_t,
        cv.Optional(CONF_SCALE_FACTOR, default=64.0): cv.float_,
        cv.Optional('name'): cv.string,
        cv.Optional('id'): cv.declare_id(SEN0343),
        cv.Optional('update_interval'): cv.time_period,
        cv.Optional('filters'): cv.ensure_list,
    })

# Now extend the chosen base schema with our options and component schema
PLATFORM_SCHEMA = BASE_PLATFORM_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(SEN0343),
    cv.Optional(CONF_ADDRESS, default=0x01): cv.hex_uint8_t,
    cv.Optional(CONF_SCALE_FACTOR, default=64.0): cv.float_,
}).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], SEN0343)
    await cg.register_component(var, config)
    # Register as a sensor so standard sensor options (name, filters) work
    await sensor_mod.register_sensor(var, config)

    address = config.get(CONF_ADDRESS)
    cg.add(var.set_address(address))

    scale = config.get(CONF_SCALE_FACTOR)
    cg.add(var.set_scale_factor(scale))
