## Made for ESPHome Checklist

- [x] Project is powered by an ESP32 or _supported_ variant such as C3, C6, S2, S3 etc.
- [x] Project is using ESPHome firmware
- [x] Project name cannot contain **ESPHome** except in the case of _ending with_ **for ESPHome**
- [x] ESPHome configuration is open source and available for end users to modify/update
- If the device uses Wi-Fi:
  - [x] Configuration contains `improv_ble:` ([documentation](https://esphome.io/components/improv_ble/))
  - [x] Configuration contains `improv_serial:` if there is a USB port ([documentation](https://esphome.io/components/improv_serial))
- Users should be able to apply updates to your device:
  - [x] Device can be "taken control" of by the user using the ESPHome Builder
    - [ ] Configuration includes `dashboard_import:` to facilitate this ([documentation](https://esphome.io/components/esphome.html#adding-the-mac-address-as-a-suffix-to-the-device-name))
    - [x] Configuration contains the `ota`.`esphome` component ([documentation](https://esphome.io/components/ota/esphome))
    - [x] Serial flashing is not disabled
    - [ ] There are no references to secrets in the configuration - not even
          `!secret wifi_ssid` / `!secret wifi_password`. Users provision their
          own Wi-Fi credentials, so anything baked in only leaves dummy values
          in the device's storage; secrets belong in the configuration a user
          ends up with **after** taking control
    - [ ] There are no passwords in the configuration - neither literal values
          nor `!secret` references on any `password:` / `psk:` key
    - [x] There are no static IP addresses in the configuration
    - [x] The configuration **must** be valid, compile and run successfully _without any user changes_ after taking control
    - [ ] Every entity/component (sensor, switch, etc.) **must** have an `id` defined
  - [ ] OTA Updates are provided via the `update`.`http_request` component ([documentation](https://esphome.io/components/update/http_request))
