# embinotec WeatherStation

[![CI](https://github.com/embinotec/weatherstation/actions/workflows/ci.yml/badge.svg)](https://github.com/embinotec/weatherstation/actions/workflows/ci.yml)
[![Made for ESPHome](https://img.shields.io/badge/Made%20for-ESPHome-blue?logo=esphome)](https://esphome.io/guides/made_for_esphome/)
[![ESPHome Version](https://img.shields.io/badge/ESPHome-%E2%89%A52026.8.0-green)](https://esphome.io/changelog/)
[![License](https://img.shields.io/github/license/embinotec/weatherstation)](LICENSE)

![Made for ESPHome](https://esphome.io/images/made-for-esphome-black-on-white.svg)

ESPHome-basierte Wetterstation auf Basis eines ESP32-C6, konform zu den "Made for ESPHome"-Anforderungen. Die Station misst Windgeschwindigkeit, Windrichtung, Niederschlag, Außentemperatur/-feuchte, Helligkeit/Spektrum, barometrischer Druck sowie den eigenen Lade- und Betriebszustand (Solar/Akku) und stellt alle Werte über die ESPHome-API in Home Assistant bereit.

## Funktionsumfang

| Messgröße | Sensor / Prinzip | Einheit |
|---|---|---|
| Windgeschwindigkeit | Reed-Kontakt-Anemometer (Pulse Counter, 2 Pulse/Umdrehung) | m/s |
| Windrichtung | 2× ADC (Potentiometer-Paar), Winkel via `atan2` | ° |
| Niederschlagsrate | Wippen-Regenmesser (Pulse Counter) | mm/h |
| Niederschlagssumme | Wippen-Regenmesser (Total) | mm |
| Außentemperatur / -feuchte | SHTC3 (i2c) | °C / % |
| Licht / Beleuchtungsstärke | tsl2591 (i2c) | – / lx |
| Akkuspannung | ADC über Spannungsteiler | V |
| Solarpanel-Spannung | ADC über Spannungsteiler | V |
| WLAN-Signalstärke | ESPHome intern | dBm |
| Ladevorgang aktiv | GPIO (Binary Sensor) | – |
| Barrometrischer druck | BMP5580 (i2c) | Oa|

## Hardware

- **Mikrocontroller:** ESP32-C6 (Variante `esp32c6`), 4 MB Flash, ESP-IDF-Framework
- **Stromversorgung:** 3× AA NiMH-Akkus (max. ~4,5 V) plus Solarpanel (max. ~8 V bei voller Sonne), jeweils über Spannungsteiler und schaltbare Messzweige geführt, um Ruhestrom zu sparen
- **Externe Komponente:** [`esphome-ec`](https://github.com/embinotec/esphome-ec) (liefert den `si1133`-Treiber)
- Mechanischer Aufbau mit Windfahne/-bechern, Wippen-Regenmesser, Solarpanel und Sensorarm entspricht dem klassischen Aufbau handelsüblicher Wetterstations-Sensorköpfe (Windbecher, Windfahne, Regenauffangtrichter, UV-/Lichtsensor, Thermo-Hygrometer-Strahlungsschutz, Edelstahl-Montagestange).

### Pinbelegung (ESP32-C6-WROOM-1)

| GPIO | Funktion |
|---|---|
| GPIO0 | Status-LED |
| GPIO1 | Ladezustand (Charge in progress, low-aktiv) |
| GPIO2 | Windrichtung, Achse X (ADC) |
| GPIO3 | Windrichtung, Achse Y (ADC) |
| GPIO4 | Akkuspannung (ADC) |
| GPIO5 | Solarpanel-Spannung (ADC) |
| GPIO6 | I²C SDA |
| GPIO7 | I²C SCL |
| GPIO9 | Boot-/User-Taste (WLAN ein/aus) |
| GPIO10 | Regenmesser (Pulse Counter) |
| GPIO11 | Windgeschwindigkeit (Pulse Counter) |
| GPIO22 | Spannungsteiler Solar aktivieren (intern) |
| GPIO23 | Spannungsteiler Akku aktivieren (intern) |

Weitere Pinout-Referenzen (ESP32-S3-DevKitC-1, ESP32-C6 SuperMini) sind als Kommentare direkt in der YAML-Datei hinterlegt.

## Diagramme

```plantuml {include} timing.puml
```




## Voraussetzungen

- ESPHome ≥ `2026.8.0`
- Home Assistant (für die API-Anbindung und optional die Zeitsynchronisation via `time: platform: homeassistant`)
- Eine `secrets.yaml` im selben Verzeichnis mit folgenden Einträgen:

```yaml
wifi_ssid: "DEIN_WLAN_NAME"
wifi_password: "DEIN_WLAN_PASSWORT"
encryption_key: "BASE64_32_BYTE_KEY"   # generieren z. B. über https://generate-random.org/base64-string (32 Byte)
ota_password: "DEIN_OTA_PASSWORT"
```

## Erstinbetriebnahme

1. Repository klonen und `secrets.yaml` wie oben anlegen.
2. Erstflashen per USB (WebSerial/`improv_serial` wird unterstützt) oder über `esphome run embinotec-weatherstation.yaml`.
3. WLAN-Zugangsdaten können per Improv-WLAN direkt über den Browser (WebSerial) eingerichtet werden – ausgelöst über die Boot-Taste (`esp32_improv: authorizer: user_button`).
4. Schlägt die WLAN-Verbindung fehl, öffnet das Gerät automatisch den Fallback-Hotspot **„Weatherstation Fallback Hotspot“** (Passwort: `embinotec`).
5. Nach erfolgreicher Ersteinrichtung ist die Station unter `embinotec-weatherstation.local` erreichbar (mDNS), inklusive integriertem Webserver auf Port 80. Weitere Updates erfolgen anschließend per OTA.

## Betriebsverhalten

- **Deep Sleep:** Die Station ist standardmäßig 1 Minute aktiv (`run_duration`) und schläft danach 2 Minuten (`sleep_duration`), um die Batterie über den ganzen Tag zu schonen.
- **Messzyklus:** Alle 30 s werden die Spannungsteiler für Solar/Akku kurz aktiviert, nach 10 ms Einschwingzeit ausgelesen und anschließend Wind, Regen sowie Außentemperatur/-feuchte aktualisiert.
- **Status-LED** (GPIO0 bei ESP32-C6, GPIO2 bei ESP32-S3):

  | Muster | Bedeutung |
  |---|---|
  | Aus | Alles in Ordnung |
  | Langsames Blinken | Nicht verbunden, Verbindungsaufbau läuft |
  | Schnelles Blinken | Fehler |

## Windgeschwindigkeitsberechnung

Das Anemometer liefert 2 Pulse pro Umdrehung über einen Reed-Kontakt (Pulse-Counter-Plattform, normalisiert auf Pulse/Minute). Umrechnung in m/s:

```
Umdrehungen/s = Pulse/Minute / 2 / 60
Umfang (m)    = 0,09 m Radius × 2 × π ≈ 0,5652 m
m/s           = 1,18 (Anemometerfaktor) × Umfang × Umdrehungen/s
```

Der resultierende Multiplikator für den `pulse_counter`-Filter beträgt `0,0055578` (Pulse/Minute → m/s).

> **Hinweis:** Im aktuellen Stand der YAML ist als aktiver Filter `multiply: 0.0124327986` eingetragen – dieser Wert entspricht rechnerisch **mph**, nicht m/s, obwohl `unit_of_measurement: 'm/s'` gesetzt ist. Vor Inbetriebnahme prüfen, welcher der beiden Filter aktiv sein soll, und `unit_of_measurement` entsprechend anpassen.

Der Debounce des Reed-Kontakts läuft aktuell ausschließlich über `internal_filter: 13us` – das ist zugleich die harte Obergrenze des ESP32-PCNT-Hardwarefilters (10-Bit-Register, APB-Takt). Für mechanisches Kontaktprellen im ms-Bereich reicht das ggf. nicht aus; Abhilfe schaffen ein RC-Tiefpass direkt am Reed-Kontakt oder eine softwareseitige Entprellung über einen `binary_sensor` mit eigenem Pulszähler.

## Bekannte Einschränkungen / offene Punkte

- [ ] Einheit/Filter der Windgeschwindigkeit vereinheitlichen (m/s vs. mph, siehe oben)
- [ ] Reed-Kontakt-Entprellung ggf. per Hardware (RC-Glied) oder Software (`binary_sensor` + `delayed_on_off`) ergänzen
- [ ] Lizenz für dieses Repository ist noch nicht festgelegt



## Lizenz

Noch nicht festgelegt.
