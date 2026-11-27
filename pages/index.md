---
layout: default
---

![embinotec WeatherStation mit Windfahne, Windrad, Regenmesser und Solarpanel](assets/images/weatherStation-clean-nologo.png){: width="600" style="display:block;margin:0 auto;max-width:100%;height:auto" }

## Dein Wetter. Dein Garten. Deine Daten.

Die Wetter-App meldet Sonne, und draußen regnet es? Mit der **embinotec WeatherStation** misst du dort, wo es zählt: bei dir zu Hause. Wind, Regen, Temperatur, Luftfeuchte, Luftdruck und Licht landen direkt in **Home Assistant** und werden zum Auslöser für deine Automationen.

Keine Bastelei, keine verschlossene Firmware: Die Station ist für **ESPHome** gemacht, und die Konfiguration liegt offen auf GitHub. Du kannst sie nutzen, wie sie ist, oder an deine Ideen anpassen.

**[🛒 Zur Wetterstation im embinotec-Shop](https://www.embinotec.de/produktseite/wetterstation){: .btn style="color:#fff;background-color:#157878" }**

**149,00 €** · Vorbestellung möglich · laut Shop voraussichtlich lieferbar ab November 2026<br>
<small>Stand: 27.11.2026. Verbindlich sind die Angaben im Shop.</small>

## Das misst die Station

| | Messwert |
|---|---|
| 🌬️ | Windgeschwindigkeit und Windrichtung |
| 🌧️ | Regenintensität und Regenmenge |
| 🌡️ | Außentemperatur und Luftfeuchtigkeit |
| 🧭 | Luftdruck mit Wettertrend |
| ☀️ | Lichtstärke mit sichtbarem und infrarotem Anteil |
| 🔋 | Solar- und Akkuspannung, Ladezustand, WLAN-Signal |

## Ideen für deine Automationen

- **Markise schützen:** bei starkem Wind automatisch einfahren.
- **Clever bewässern:** die Gartenbewässerung pausieren, wenn es geregnet hat.
- **Licht nach Bedarf:** Beleuchtung nach der tatsächlichen Helligkeit schalten.
- **Wetterumschwung bemerken:** bei fallendem Luftdruck eine Nachricht erhalten.

Die Automationen richtest du in Home Assistant passend zu deinen Geräten ein.

## Technik

- **ESP32-C6** mit **ESPHome**-Firmware
- Anbindung an Home Assistant über die ESPHome-API
- Stromversorgung mit **Solarpanel** und **3 × AA-NiMH-Akkus**
- **Deep Sleep** zum Energiesparen: Die Messwerte kommen in Intervallen
- WLAN-Einrichtung per Improv oder Fallback-Hotspot
- Laut Shop Verbindung über WLAN oder Thread möglich. Die Standard-Konfiguration nutzt WLAN.

## Für Maker und Tüftler

- [Quellcode und Dokumentation](https://github.com/embinotec/embinotec-esphome-weatherstation)
- [ESPHome-Konfiguration](https://github.com/embinotec/embinotec-esphome-weatherstation/blob/master/esphome/embinotec-weatherstation.yaml)
- [Releases und Firmware-Downloads](https://github.com/embinotec/embinotec-esphome-weatherstation/releases)
- [Fehler melden oder Idee vorschlagen](https://github.com/embinotec/embinotec-esphome-weatherstation/issues)
- [Lizenz](https://github.com/embinotec/embinotec-esphome-weatherstation/blob/master/LICENSE.md)

## Aktuelle Firmware

| Download | Verwendung | Prüfsumme |
|---|---|---|
| [**OTA-Firmware**](firmware/firmware.ota.bin){: download="firmware.ota.bin" } | Update einer Station über WLAN | [MD5](firmware/firmware.ota.bin.md5) |
| [**Factory-Firmware**](firmware/firmware.factory.bin){: download="firmware.factory.bin" } | Erstinstallation oder Wiederherstellung per USB | [MD5](firmware/firmware.factory.bin.md5) |

## Hol dir dein eigenes Wetter ins Smart Home

**[Jetzt die embinotec WeatherStation ansehen](https://www.embinotec.de/produktseite/wetterstation){: .btn style="color:#fff;background-color:#157878" }**
