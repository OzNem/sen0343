import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ID,
    CONF_ADDRESS,
    CONF_UPDATE_INTERVAL,
    UNIT_PASCAL,
    ICON_GAUGE,
)

sen0343_ns = cg.esphome_ns.namespace("sen0343")
SEN0343Sensor = sen0343_ns.class_("SEN0343Sensor", sensor.Sensor, cg.PollingComponent)

CONFIG_SCHEMA = (
    sensor.sensor_schema(UNIT_PASCAL, ICON_GAUGE, 1)
    .extend(
        {
            cv.GenerateID(): cv.declare_id(SEN0343Sensor),
            cv.Required(CONF_ADDRESS): cv.i2c_address,
            cv.Optional(CONF_UPDATE_INTERVAL, default="5s"): cv.update_interval,
        }
    )
    .extend(i2c.i2c_device_schema(0x28))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    await i2c.register_i2c_device(var, config)

    cg.add(var.set_address(config[CONF_ADDRESS]))
