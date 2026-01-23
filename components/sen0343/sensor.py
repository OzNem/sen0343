import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    UNIT_PASCAL,
    ICON_GAUGE,
)

# Namespace and class binding to C++ implementation
sen0343_ns = cg.esphome_ns.namespace("sen0343")
SEN0343Sensor = sen0343_ns.class_("SEN0343Sensor", sensor.Sensor, cg.PollingComponent)

# YAML configuration schema
CONFIG_SCHEMA = (
    sensor.sensor_schema(
        unit_of_measurement=UNIT_PASCAL,
        icon=ICON_GAUGE,
        accuracy_decimals=1,
    )
    .extend(
        {
            cv.GenerateID(): cv.declare_id(SEN0343Sensor),
            cv.Optional("address", default=0x58): cv.i2c_address,
            cv.Optional("scale_factor", default=64.0): cv.float_,
        }
    )
    .extend(i2c.i2c_device_schema(0x58))
)

# Code generation for ESPHome
async def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])

    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    await i2c.register_i2c_device(var, config)

    if "scale_factor" in config:
        cg.add(var.set_scale_factor(config["scale_factor"]))
