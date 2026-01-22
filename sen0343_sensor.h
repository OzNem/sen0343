#include "esphome.h"

class SEN0343Sensor : public esphome::PollingComponent, public esphome::sensor::Sensor {
 public:
  SEN0343Sensor() : PollingComponent(5000) {}

  void update() override {
    uint8_t data[4];

    if (!esphome::i2c::global_i2c->read(0x28, data, 4)) {
      publish_state(NAN);
      return;
    }

    uint16_t raw = (data[0] << 8) | data[1];

    float pressure = (raw - 1638) * (500.0f / (14745 - 1638));

    publish_state(pressure);
  }
};
