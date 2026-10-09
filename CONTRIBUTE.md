# Contributing to embinotec WeatherStation

Danke für dein Interesse, zur embinotec WeatherStation beizutragen!
Dieses Projekt ist **Made for ESPHome** zertifiziert – alle Beiträge
müssen diese Anforderungen weiterhin erfüllen.

---

## Inhaltsverzeichnis

- [Contributing to embinotec WeatherStation](#contributing-to-embinotec-weatherstation)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Arten von Beiträgen](#arten-von-beiträgen)
  - [Bevor du anfängst](#bevor-du-anfängst)
  - [Entwicklungsumgebung einrichten](#entwicklungsumgebung-einrichten)
    - [Voraussetzungen](#voraussetzungen)
    - [Setup](#setup)
    - [secrets.example.yaml](#secretsexampleyaml)
  - [Beiträge zur Firmware (YAML)](#beiträge-zur-firmware-yaml)
    - [Regeln für YAML-Änderungen](#regeln-für-yaml-änderungen)
    - [CI muss grün sein](#ci-muss-grün-sein)
  - [Beiträge zur Hardware](#beiträge-zur-hardware)
    - [Was wir akzeptieren](#was-wir-akzeptieren)
    - [Was wir nicht akzeptieren](#was-wir-nicht-akzeptieren)
    - [Format](#format)
  - [Pull Request Prozess](#pull-request-prozess)
    - [Branch-Namenskonvention](#branch-namenskonvention)
  - [Made for ESPHome Anforderungen](#made-for-esphome-anforderungen)
  - [Code-Stil](#code-stil)
    - [YAML](#yaml)
    - [Sensor-Benennung](#sensor-benennung)
    - [Lambda-Code](#lambda-code)
  - [Issues melden](#issues-melden)
    - [Bug-Report](#bug-report)
    - [Feature-Request](#feature-request)
  - [Kontakt](#kontakt)

---

## Arten von Beiträgen

Wir freuen uns über:

| Art | Beispiele |
|---|---|
| 🐛 **Bugfixes** | Falsche Berechnungen, Timing-Probleme, Tippfehler in YAML |
| ✨ **Features** | Neue Sensoren, bessere Algorithmen, zusätzliche Statusanzeigen |
| 📖 **Dokumentation** | README verbessern, Kommentare in YAML, Schaltplan-Erklärungen |
| 🌍 **Übersetzungen** | Englische Übersetzung der deutschen Kommentare |
| 🧪 **Tests** | Neue Kalibrierungsdaten, Feldmessungen, Hardware-Varianten |
| 🔧 **Hardware** | Schaltplan-Korrekturen, PCB-Verbesserungen, Bestückungslisten |

Nicht erwünscht: Änderungen die die Made for ESPHome Anforderungen verletzen
(hardcodierte Credentials, fehlende IDs, Entfernen von `dashboard_import`).

---

## Bevor du anfängst

- **Suche erst nach bestehenden Issues** – dein Problem oder deine Idee
  könnte schon diskutiert worden sein.
- **Öffne ein Issue bevor du größere Änderungen startest** – so vermeidest
  du Arbeit die wir nicht mergen können.
- **Kleine Änderungen** (Tippfehler, Kommentare, Bugfixes) können direkt
  als Pull Request kommen.

---

## Entwicklungsumgebung einrichten

### Voraussetzungen

- Python ≥ 3.11
- ESPHome ≥ 2026.8.0
- Git

### Setup

```bash
# Repository klonen
git clone https://github.com/embinotec/weatherstation.git
cd weatherstation

# ESPHome installieren
pip install esphome

# secrets.yaml anlegen (wird nicht committet)
cp secrets.example.yaml secrets.yaml
# → eigene Werte eintragen

# YAML validieren (kein Kompilieren nötig für einfache Checks)
esphome config embinotec-weatherstation.yaml

# Firmware kompilieren (dauert beim ersten Mal länger)
esphome compile embinotec-weatherstation.yaml
```

### secrets.example.yaml

Die Datei `secrets.example.yaml` im Repository enthält Platzhalter:

```yaml
wifi_ssid: "DEIN_WLAN_NAME"
wifi_password: "DEIN_WLAN_PASSWORT"
encryption_key: "BASE64_32_BYTE_KEY"
ota_password: "DEIN_OTA_PASSWORT"
fallback_pw: "FALLBACK_PASSWORT"
```

> ⚠️ **Niemals** `secrets.yaml` mit echten Werten committen.
> Sie steht in `.gitignore` und wird vom CI automatisch mit Dummy-Werten erstellt.

---

## Beiträge zur Firmware (YAML)

### Regeln für YAML-Änderungen

1. **Jede Komponente braucht eine `id`** – Pflicht für Made for ESPHome.
```yaml
   # ✅ richtig
   sensor:
     - platform: adc
       id: battery_voltage_raw
       name: "Battery.Voltage"
   
   # ❌ falsch
   sensor:
     - platform: adc
       name: "Battery.Voltage"
```

2. **Keine hardcodierten Secrets** – alle sensitiven Werte über `!secret`.

3. **Kommentare auf Englisch oder Deutsch** – doppeltes `##` für
   Abschnitts-Headlines, einfaches `#` für Inline-Kommentare.

4. **`update_interval:  never`** bei Sensoren die per `interval` gesteuert
   werden – nie selbstständig feuern lassen.

5. **Einheiten und `device_class` korrekt setzen** – ESPHome und
   Home Assistant werten das für Energie-Dashboards aus.

6. **Kalibrierungswerte dokumentieren** – woher kommt ein Wert, wie wurde
   er gemessen:
```yaml
   filters:
     - calibrate_linear:
         datapoints:
           - 0.0   -> 0.0      ## Nullpunkt
           - 2.493 -> 2.652    ## Gemessen: 3,97V am Multimeter, ADC-Rohwert 2,493V
```

### CI muss grün sein

Jeder Pull Request muss beide CI-Jobs bestehen:

- `✅ Validate YAML` – `esphome config` ohne Fehler
- `🔨 Compile Firmware` – vollständiges Kompilieren ohne Fehler

---

## Beiträge zur Hardware

Schaltpläne und PCB-Layouts stehen unter **CERN-OHL-P v2**.

### Was wir akzeptieren

- Korrekturen an Bauteilwerten (z.B. falscher Widerstand im Schaltplan)
- Verbesserungen am PCB-Layout (Leiterbahnführung, Testpunkt-Größen)
- Neue Testpunkte oder Bestückungsvarianten
- Fehlerkorrekturen in der BOM (Bill of Materials)

### Was wir nicht akzeptieren

- Änderungen die das Made for ESPHome Pinout (siehe README) brechen
- Änderungen die die YAML-Konfiguration ungültig machen ohne
  gleichzeitige YAML-Anpassung

### Format

- Schaltpläne als **KiCad** (bevorzugt) oder EasyEDA/EasyEDA Pro
- Gerber-Dateien bitte **nicht** committen – werden beim Release generiert
- BOM als CSV mit Spalten: `Bezeichner`, `Wert`, `Gehäuse`, `LCSC-Nr.`

---

## Pull Request Prozess

1. **Fork** das Repository und erstelle einen Branch:
```bash
   git checkout -b fix/battery-voltage-calibration
   # oder
   git checkout -b feat/uv-sensor-support
```

2. **Ändere nur was nötig ist** – kein Reformatieren von unverändertem Code.

3. **Teste lokal**:
```bash
   esphome config embinotec-weatherstation.yaml
   esphome compile embinotec-weatherstation.yaml
```

4. **Committe mit aussagekräftiger Nachricht**:
5. 5. **Öffne den Pull Request** gegen `main` mit:
   - Beschreibung **was** geändert wurde und **warum**
   - Hinweis ob Hardware-Tests durchgeführt wurden
   - Messwerte vor/nach der Änderung (bei Kalibrierungsänderungen)

6. **CI muss grün sein** bevor wir mergen.

### Branch-Namenskonvention

| Präfix | Verwendung |
|---|---|
| `fix/` | Bugfix |
| `feat/` | Neues Feature |
| `docs/` | Nur Dokumentation |
| `hw/` | Hardware-Änderungen |
| `ci/` | CI/Workflow-Änderungen |
| `refactor/` | Umstrukturierung ohne Funktionsänderung |

---

## Made for ESPHome Anforderungen

Alle Beiträge **müssen** diese Anforderungen weiterhin erfüllen.
Der CI-Job `🏷️ Made for ESPHome Checklist` prüft das automatisch.

| Anforderung | Details |
|---|---|
| `esphome.project` | Name und Version müssen gesetzt sein |
| `dashboard_import` | `package_import_url` muss auf den `main`-Branch zeigen |
| `esp32_improv` | BLE-Provisioning muss aktiv bleiben |
| `improv_serial` | USB-Provisioning muss aktiv bleiben |
| `api` | Native API muss konfiguriert sein |
| `ota: platform: esphome` | OTA-Update muss funktionieren |
| Alle Komponenten haben `id` | Für Extend/Remove nach Adoption |
| Keine hardcodierten Secrets | `wifi_ssid`, `wifi_password`, Keys etc. |

---

## Code-Stil

### YAML

```yaml
## ------ ABSCHNITT MIT DOPPELTEM HASH ------
# Inline-Kommentar mit einfachem Hash
sensor:
  ## SUB: ----- UNTERABSCHNITT -----
  - platform: adc
    pin: GPIO4
    name: "Battery.Voltage"   # Punkt-Notation: Kategorie.Name
    id: battery_voltage_raw   # snake_case für IDs
    unit_of_measurement: "V"  # immer setzen
    device_class: voltage     # immer setzen wenn vorhanden
    state_class: measurement  # immer setzen
```

### Sensor-Benennung

Wir verwenden `Kategorie.Name` mit Punkt als Trennzeichen:

    Battery.Voltage
    Battery.status
    Solar.Voltage
    Wind.Speed
    Wind.Degrees
    Wind.Direction
    Outside.Temperature
    Outside.Humidity
    Licht.Lux
    Baro.Luftdruck
    WiFi.Signal strength

### Lambda-Code

```cpp
// Konstanten am Anfang, UPPERCASE
const float VCE_SAT = 0.30f;
const float R1      = 56000.0f;  // Kommentar: Ohm, Bauteilbezeichner R11

// Frühzeitig returnen bei Grenzfällen
if (x < VCE_SAT) return 0.0f;

// Berechnungen mit sprechenden Zwischenvariablen
float v_in = (x - VCE_SAT) * (R1 + R2) / R2 + VCE_SAT;
return v_in;
```

---

## Issues melden

### Bug-Report

Bitte folgende Informationen mitgeben:
Hardware Rev: 1.3
ESPHome Version: 2026.8.0
Home Assistant Version: 2026.9.0

Beschreibung:
Die Batteriespannung zeigt immer 0,3V an, obwohl Akkus eingelegt sind.

Erwartetes Verhalten:
Spannung zwischen 3,6V und 4,35V

Tatsächliches Verhalten:
Konstant 0,3V

Log-Ausgabe:
[D][sensor] Battery ADC Rohwert: 0.3012 V
[I][sensor] Battery Spannung (berechnet): 0.300 V

Multimeter-Messung am Pin GPIO4: 0,31V
Multimeter-Messung V_BAT: 3,87V


### Feature-Request

- Was soll der neue Sensor/die neue Funktion machen?
- Welche Hardware wird benötigt (falls zusätzlich)?
- Ist das Made for ESPHome kompatibel?

---

## Kontakt

- **Issues & PRs:** [github.com/embinotec/weatherstation](https://github.com/embinotec/weatherstation)
- **Shop & Hardware:** [embinotec.de](https://www.embinotec.de)
- **ESPHome Community:** [community.home-assistant.io/c/esphome](https://community.home-assistant.io/c/esphome/)
- **ESPHome Discord:** [esphome.io/chat](https://esphome.io/chat)

---

*Mit deinem Beitrag stimmst du zu, dass er unter der
[Apache License 2.0](LICENSE) veröffentlicht wird.*