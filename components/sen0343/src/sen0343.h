#pragma once

#include "esphome.h"

namespace esphome {
namespace sen0343 {

class SEN0343 : public PollingComponent, public sensor::Sensor {
 public:
  explicit SEN0343() : PollingComponent(15000) {}  // default 15s polling; overridden by YAML update_interval
  void set_address(uint8_t address) { address_ = address; }
  void setup() override;
  void update() override;

 protected:
  uint8_t address_{0x28};
  i2c::I2CDevice *i2c_{nullptr};
};

}  // namespace sen0343
}  // namespace esphome
