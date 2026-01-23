#include "sen0343.h"

namespace esphome {
namespace sen0343 {

static const uint8_t READ_REG = 0x01;  // register to read data from (per your doc)

void SEN0343::setup() {
  // Create I2C device instance for the configured address
  // Note: address_ is the 7-bit I2C address of the device (or 0x00 if your device uses that).
  i2c_ = new i2c::I2CDevice(address_);
  // Optionally: perform any device init here (reset, config registers, etc.)
}

void SEN0343::update() {
  // Read 3 bytes of raw pressure data from READ_REG
  uint8_t buf[3] = {0};
  bool ok = false;

  // Try register-based read first
  ok = i2c_->read_bytes(READ_REG, buf, 3);

  // If that fails and the device uses "raw" reads without a register, try a direct read
  if (!ok) {
    ESP_LOGW("sen0343", "Register read failed at addr 0x%02X, trying raw read", address_);
    ok = i2c_->read_bytes(buf, 3);
  }

  if (!ok) {
    ESP_LOGW("sen0343", "I2C read failed at address 0x%02X", address_);
    // Optionally publish NaN or skip publishing
    return;
  }

  // Combine 3 bytes into a signed 24-bit integer
  uint32_t raw24 = ((uint32_t)buf[0] << 16) | ((uint32_t)buf[1] << 8) | (uint32_t)buf[2];

  // Sign-extend 24-bit to 32-bit signed integer
  int32_t signed_raw;
  if (raw24 & 0x800000) {
    // negative number
    signed_raw = (int32_t)(raw24 | 0xFF000000);
  } else {
    signed_raw = (int32_t)raw24;
  }

  // Convert to Pascals using scale factor
  float pressure_pa = (float)signed_raw / scale_factor_;

  // Publish the pressure
  this->publish_state(pressure_pa);

  // Optional debug log
  ESP_LOGD("sen0343", "raw24=0x%06X signed=%d scale=%.3f pressure=%.3f Pa", raw24, signed_raw, scale_factor_, pressure_pa);
}

}  // namespace sen0343
}  // namespace esphome
