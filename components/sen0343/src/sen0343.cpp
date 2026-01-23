#include "sen0343.h"

namespace sen0343 {

static const uint8_t READ_REG = 0x01;  // register to read data from

void SEN0343Sensor::setup() {
  // Create I2C device instance for the configured address
  i2c_ = new esphome::i2c::I2CDevice(address_);
}

void SEN0343Sensor::update() {
  uint8_t buf[3] = {0};
  bool ok = false;

  // Try register-based read first
  ok = i2c_->read_bytes(READ_REG, buf, 3);

  // If that fails, try raw read
  if (!ok) {
    ESP_LOGW("sen0343", "Register read failed at addr 0x%02X, trying raw read", address_);
    ok = i2c_->read_bytes(buf, 3);
  }

  if (!ok) {
    ESP_LOGW("sen0343", "I2C read failed at address 0x%02X", address_);
    return;
  }

  // Combine 3 bytes into a signed 24-bit integer
  uint32_t raw24 = ((uint32_t)buf[0] << 16) |
                   ((uint32_t)buf[1] << 8) |
                   (uint32_t)buf[2];

  int32_t signed_raw;
  if (raw24 & 0x800000) {
    signed_raw = (int32_t)(raw24 | 0xFF000000);  // sign-extend
  } else {
    signed_raw = (int32_t)raw24;
  }

  float pressure_pa = (float)signed_raw / scale_factor_;

  publish_state(pressure_pa);

  ESP_LOGD("sen0343",
           "raw24=0x%06X signed=%d scale=%.3f pressure=%.3f Pa",
           raw24, signed_raw, scale_factor_, pressure_pa);
}

}  // namespace sen0343
