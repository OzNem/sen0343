#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/i2c/i2c.h"

namespace sen0343 {

class SEN0343Sensor : public esphome::PollingComponent, public esphome::sensor::Sensor {
 public:
  SEN0343Sensor() : PollingComponent(15000) {}  // default 15s polling

  void set_address(uint8_t address) { address_ = address; }
  void set_scale_factor(float scale) { scale_factor_ = scale; }

  void setup() override;
  void update() override;

 protected:
  uint8_t address_{0x58};  // default I2C address for SEN0343
  float scale_factor_{64.0f};
  esphome::i2c::I2CDevice *i2c_{nullptr};
};

}  // namespace sen0343
