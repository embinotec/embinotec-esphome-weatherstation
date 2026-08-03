# embinotec WeatherStation

ESPHome-based weather station built around an ESP32-C6, compliant with the "Made for ESPHome" requirements. The station measures wind speed, wind direction, rainfall, outdoor temperature/humidity, UV index/illuminance, as well as its own charge and power state (solar/battery), and exposes all values via the ESPHome API to Home Assistant.

## Features

| Measurement | Sensor / Principle | Unit |
|---|---|---|
| Wind speed | Reed-switch anemometer (pulse counter, 2 pulses/revolution) | m/s |
| Wind direction | 2× ADC (potentiometer pair), angle via `atan2` | ° |
| Rain rate | Tipping-bucket rain gauge (pulse counter) | mm/h |
| Rain total | Tipping-bucket rain gauge (total) | mm |
| Outdoor temperature / humidity | SHTC3 (I²C) | °C / % |
| UV index / illuminance | SI1133 (I²C, external component) | – / lx |
| Battery voltage | ADC via voltage divider | V |
| Solar panel voltage | ADC via voltage divider | V |
| Wi-Fi signal strength | ESPHome internal | dBm |
| Charging in progress | GPIO (binary sensor) | – |

## Hardware

- **Microcontroller:** ESP32-C6 (`esp32c6` variant), 4 MB flash, ESP-IDF framework
- **Power supply:** 3× AA NiMH rechargeable batteries (max. ~4.5 V) plus a solar panel (max. ~8 V in full sunlight), each routed through a voltage divider and a switchable measurement branch to conserve standby current
- **External component:** [`esphome-ec`](https://github.com/embinotec/esphome-ec) (provides the `si1133` driver)
- The mechanical build (wind vane/cups, tipping-bucket rain gauge, solar panel, sensor arm) follows the classic layout of common weather-station sensor heads (wind cups, wind vane, rain collector funnel, UV/light sensor, thermo-hygrometer radiation shield, stainless steel mounting pole).

### Pinout (ESP32-C6-WROOM-1)

| GPIO | Function |
|---|---|
| GPIO0 | Status LED |
| GPIO1 | Charge status (charge in progress, active-low) |
| GPIO2 | Wind direction, axis X (ADC) |
| GPIO3 | Wind direction, axis Y (ADC) |
| GPIO4 | Battery voltage (ADC) |
| GPIO5 | Solar panel voltage (ADC) |
| GPIO6 | I²C SDA |
| GPIO7 | I²C SCL |
| GPIO9 | Boot/user button (Wi-Fi on/off) |
| GPIO10 | Rain gauge (pulse counter) |
| GPIO11 | Wind speed (pulse counter) |
| GPIO22 | Enable solar voltage divider (internal) |
| GPIO23 | Enable battery voltage divider (internal) |

Additional pinout references (ESP32-S3-DevKitC-1, ESP32-C6 SuperMini) are documented as comments directly in the YAML file.

## Requirements

- ESPHome ≥ `2026.5.1`
- Home Assistant (for the API connection and, optionally, time sync via `time: platform: homeassistant`)
- A `secrets.yaml` in the same directory containing:

```yaml
wifi_ssid: "YOUR_WIFI_NAME"
wifi_password: "YOUR_WIFI_PASSWORD"
encryption_key: "BASE64_32_BYTE_KEY"   # generate e.g. via https://generate-random.org/base64-string (32 bytes)
ota_password: "YOUR_OTA_PASSWORD"
```

## First-time setup

1. Clone the repository and create `secrets.yaml` as shown above.
2. Flash the device for the first time over USB (WebSerial/`improv_serial` is supported) or via `esphome run embinotec-weatherstation.yaml`.
3. Wi-Fi credentials can be provisioned directly through the browser via Improv Wi-Fi (WebSerial) — triggered via the boot button (`esp32_improv: authorizer: user_button`).
4. If the Wi-Fi connection fails, the device automatically opens a fallback hotspot named **"Weatherstation Fallback Hotspot"** (password: `embinotec`).
5. After initial setup, the station is reachable at `embinotec-weatherstation.local` (mDNS), including a built-in web server on port 80. Further updates are then delivered over OTA.

## Runtime behavior

- **Deep sleep:** By default the station stays awake for 1 minute (`run_duration`) and then sleeps for 2 minutes (`sleep_duration`) to conserve battery over the course of a day.
- **Measurement cycle:** Every 30 s the solar/battery voltage dividers are briefly enabled, read after a 10 ms settling delay, and wind, rain, and outdoor temperature/humidity are then updated.
- **Status LED** (GPIO0 on ESP32-C6, GPIO2 on ESP32-S3):

  | Pattern | Meaning |
  |---|---|
  | Off | Everything is fine |
  | Slow blink | Not connected, attempting to connect |
  | Fast blink | Error |

## Wind speed calculation

The anemometer produces 2 pulses per revolution via a reed switch (pulse counter platform, normalized to pulses/minute). Conversion to m/s:

```
revolutions/s = pulses/minute / 2 / 60
circumference (m) = 0.09 m radius × 2 × π ≈ 0.5652 m
m/s = 1.18 (anemometer factor) × circumference × revolutions/s
```

The resulting multiplier for the `pulse_counter` filter is `0.0055578` (pulses/minute → m/s).

> **Note:** In the current state of the YAML, the active filter is `multiply: 0.0124327986` — this value mathematically corresponds to **mph**, not m/s, even though `unit_of_measurement: 'm/s'` is set. Before commissioning, decide which of the two filters should be active and update `unit_of_measurement` accordingly.

Debouncing of the reed switch currently relies solely on `internal_filter: 13us` — which is also the hard upper limit of the ESP32 PCNT hardware filter (10-bit register, clocked from the APB bus). This may not be sufficient for mechanical contact bounce in the millisecond range; remedies include an RC low-pass filter directly at the reed switch, or software debouncing via a `binary_sensor` with its own pulse counter.

## Known limitations / open items

- [ ] Unify the wind speed unit/filter (m/s vs. mph, see above)
- [ ] Add reed switch debouncing, either via hardware (RC network) or software (`binary_sensor` + `delayed_on_off`)
- [ ] License for this repository has not yet been determined

## License

Not yet determined.
