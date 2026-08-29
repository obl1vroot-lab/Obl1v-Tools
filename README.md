<div align="center">

# ⚡ Obl1v-Tools

**A powerful all-in-one GUI toolkit with 40+ utilities across 9 categories.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)](#)

<img src="https://img.shields.io/badge/CustomTkinter-5.2+-E040FB?style=for-the-badge&logo=telegram&logoColor=white" alt="GUI">
<img src="https://img.shields.io/badge/40-Tools-orange?style=for-the-badge" alt="Tools">

<br><br>

*Obl1v-Tools* ist ein umfassendes Desktop-GUI-Toolkit, das dir **40 nützliche Werkzeuge** in einer einzigen Anwendung bietet — mit dunklem Theme und moderner Benutzeroberfläche.

*Obl1v-Tools* is a comprehensive desktop GUI toolkit providing **40 useful utilities** in a single application — with a dark theme and modern interface.

</div>

---

## 📋 Table of Contents / Inhaltsverzeichnis

- [🇩🇪 Installation (Deutsch)](#-installation-deutsch)
- [🇬🇧 Installation (English)](#-installation-english)
- [🚀 Quick Start / Schnellstart](#-quick-start--schnellstart)
- [🛠️ Included Tools / Enthaltene Werkzeuge](#️-included-tools--enthaltene-werkzeuge)
- [📁 Project Structure / Projektstruktur](#-project-structure--projektstruktur)
- [💻 Requirements / Systemanforderungen](#-requirements--systemanforderungen)
- [📄 License / Lizenz](#-license--lizenz)

---

## 🇩🇪 Installation (Deutsch)

### Voraussetzungen

| Voraussetzung | Version |
|:---|:---|
| **Python** | 3.10 oder höher |
| **pip** |_neueste Version_ |

### Schritt-für-Schritt-Anleitung

**1. Repository klonen oder herunterladen**

```bash
git clone https://github.com/Obl1v/Obl1v-Tools.git
cd Obl1v-Tools
```

Oder lade das Projekt manuell als ZIP herunter und entpacke es.

**2. Python-Abhängigkeiten installieren**

```bash
pip install -r requirements.txt
```

> 💡 **Tipp:** Es wird empfohlen, eine virtuelle Umgebung zu verwenden:
> ```bash
> python -m venv venv
> venv\Scripts\activate        # Windows
> source venv/bin/activate     # macOS / Linux
> pip install -r requirements.txt
> ```

**3. Anwendung starten**

```bash
python main.py
```

### Installierte Pakete

| Paket | Zweck |
|:---|:---|
| `customtkinter` | Modernes GUI-Framework |
| `requests` | HTTP-Anfragen |
| `dnspython` | DNS-Abfragen |
| `python-whois` | WHOIS-Abfragen |
| `Pillow` | Bildverarbeitung |
| `qrcode` | QR-Code-Generierung |
| `bcrypt` | Passwort-Hashing |
| `psutil` | System- & Prozessinformationen |

---

## 🇬🇧 Installation (English)

### Prerequisites

| Requirement | Version |
|:---|:---|
| **Python** | 3.10 or higher |
| **pip** | _latest version_ |

### Step-by-Step Guide

**1. Clone or download the repository**

```bash
git clone https://github.com/Obl1v/Obl1v-Tools.git
cd Obl1v-Tools
```

Or download the project manually as a ZIP and extract it.

**2. Install Python dependencies**

```bash
pip install -r requirements.txt
```

> 💡 **Tip:** It is recommended to use a virtual environment:
> ```bash
> python -m venv venv
> venv\Scripts\activate        # Windows
> source venv/bin/activate     # macOS / Linux
> pip install -r requirements.txt
> ```

**3. Launch the application**

```bash
python main.py
```

### Installed Packages

| Package | Purpose |
|:---|:---|
| `customtkinter` | Modern GUI framework |
| `requests` | HTTP requests |
| `dnspython` | DNS queries |
| `python-whois` | WHOIS lookups |
| `Pillow` | Image processing |
| `qrcode` | QR code generation |
| `bcrypt` | Password hashing |
| `psutil` | System & process info |

---

## 🚀 Quick Start / Schnellstart

Nach der Installation öffnet sich ein **1100×700 px großes Fenster** mit:

After installation, a **1100×700 px window** opens with:

- 🔍 **Suchleiste** / **Search bar** — Finde Tools schnell / Find tools quickly
- 📂 **9 Kategorien** / **9 Categories** — Übersichtliche Ordnung / Organized layout
- ⚙️ **40 Werkzeuge** / **40 Tools** — Alle auf einen Klick / All at one click
- 🌙 **Dark Mode** — Augenschonendes Design / Eye-friendly design

---

## 🛠️ Included Tools / Enthaltene Werkzeuge

<details>
<summary><b>🔐 Passwörter / Passwords</b> (5)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| Generator | Sicheren Passwort-Generator / Secure password generator |
| Stärke-Analyse / Strength | Passwort-Stärke mit Entropie-Bewertung / Password strength with entropy scoring |
| Hasher | Passwort-Hashing (MD5, SHA256, SHA512, bcrypt) / Password hashing |
| Breach Checker | HIBP k-Anonymity Datenschutzverletzungsprüfung / HIBP k-anonymity breach check |
| Passphrase | Passphrase-Generator aus eingebautem Wörterbuch / Passphrase generator from built-in wordlist |

</details>

<details>
<summary><b>🔐 Hashing</b> (5)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| Hash Calculator | Datei-Hash berechnen / Calculate file hashes |
| Base64 | Base64 Encode/Decode |
| URL Codec | URL Encode/Decode |
| Hex Codec | Hex Encode/Decode |
| Caesar Cipher | Caesar-Verschlüsselung / ROT13 / Caesar cipher / ROT13 |

</details>

<details>
<summary><b>🌐 Netzwerk / Network</b> (5)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| IP Lookup | IP-Standortbestimmung / IP geolocation |
| DNS Lookup | DNS-Einträge abfragen / DNS record queries |
| Port Scanner | TCP-Port-Scanner / TCP port scanner |
| Ping | Erreichbarkeitstest / Connectivity test |
| WHOIS | Domain-WHOIS-Informationen / Domain WHOIS info |

</details>

<details>
<summary><b>📁 Dateien / Files</b> (5)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| File Hasher | Datei-Hash berechnen / Calculate file hashes |
| Duplicate Finder | Doppelte Dateien finden / Find duplicate files |
| File Info | Datei-Metadaten anzeigen / Show file metadata |
| Bulk Renamer | Massenumbenennung / Bulk file renamer |
| File Shredder | Sicheres Löschen / Secure file shredder |

</details>

<details>
<summary><b>📝 Text</b> (5)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| Word Counter | Wörter/Zeichen zählen / Count words/characters |
| Case Converter | Groß-/Kleinschreibung / Case converter |
| Lorem Generator | Platzhaltertext generieren / Placeholder text generator |
| Regex Tester | Regex-Tester / Regex tester |
| Text Diff | Textvergleich / Side-by-side text diff |

</details>

<details>
<summary><b>🖼️ Bilder / Images</b> (3)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| Image Resizer | Bildgröße ändern / Resize images |
| Image to Base64 | Bild zu Base64 / Image to Base64 encoder |
| QR Generator | QR-Code erstellen / Generate QR codes |

</details>

<details>
<summary><b>🛡️ Sicherheit / Security</b> (4)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| Subdomain Finder | Subdomains entdecken / Discover subdomains |
| Email Header | E-Mail-Header analysieren / Analyze email headers |
| URL Scanner | URL-Sicherheitsprüfung / URL security scan |
| Service Identifier | Dienste über Port-Scanning identifizieren / Identify services via port scanning |

</details>

<details>
<summary><b>💻 System</b> (4)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| System Info | Systeminformationen / System information |
| Process List | Laufende Prozesse / Running processes |
| Disk Usage | Festplattenanalyse / Disk usage analyzer |
| Net Connections | Netzwerkverbindungen / Network connections |

</details>

<details>
<summary><b>🔧 Utility</b> (4)</summary>

| Tool | Beschreibung / Description |
|:---|:---|
| Timestamp | Unix-Zeitstempel-Umrechner / Unix timestamp converter |
| UUID Generator | UUID-Generator (v1, v4, v5) / UUID generator |
| JSON Formatter | JSON formatieren / JSON formatter |
| Color Picker | Farbwähler mit Konvertierung / Color picker with conversion |

</details>

---

## 📁 Project Structure / Projektstruktur

```
Obl1v-Tools/
├── main.py                 # Einstiegspunkt / Entry point
├── requirements.txt        # Abhängigkeiten / Dependencies
├── gui/
│   ├── app.py              # Hauptfenster / Main window
│   ├── sidebar.py          # Seitenleiste / Sidebar navigation
│   └── styles.py           # Design-Konstanten / Theme constants
└── tools/
    ├── password/           # Passwort-Werkzeuge / Password tools
    ├── hashing/            # Hashing-Werkzeuge / Hashing tools
    ├── network/            # Netzwerk-Werkzeuge / Network tools
    ├── files/              # Datei-Werkzeuge / File tools
    ├── text/               # Text-Werkzeuge / Text tools
    ├── image/              # Bild-Werkzeuge / Image tools
    ├── security/           # Sicherheits-Werkzeuge / Security tools
    ├── system/             # System-Werkzeuge / System tools
    └── utility/            # Utility-Werkzeuge / Utility tools
```

---

## 💻 Requirements / Systemanforderungen

| Komponente / Component | Minimum |
|:---|:---|
| **Betriebssystem / OS** | Windows 10+, macOS 10.15+, Linux |
| **Python** | 3.10+ |
| **RAM** | 512 MB |
| **Display** | 1280×720 Auflösung / resolution |

---

## 📄 License / Lizenz

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert.

This project is licensed under the **MIT License**.

```
MIT License — Copyright (c) 2024 Obl1v
```

---

<div align="center">

**Made with ❤️ by [Obl1v](https://github.com/Obl1v)**

</div>
