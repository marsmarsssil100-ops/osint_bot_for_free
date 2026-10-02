# Minimalist OSINT Intelligence Telegram Bot

An asynchronous, lightweight OSINT Telegram bot built with **Python 3.11** and **aiogram 3.x**. Designed for quick reconnaissance, account discovery, and metadata analysis with a clean, non-intrusive interactive UI.

---

## Technical Overview

Unlike aggressive tools relying on illegal leaked databases, this bot operates strictly through **open-source methods**:
- Live endpoint parsing and metadata extractions.
- Strict error-string verification to eliminate false-positive URL results.
- Fully asynchronous architecture for fast concurrent query processing.

---

## Features

### 1. Multi-Platform Username Enumeration
- Asynchronously checks over 17 public platforms (GitHub, Steam, Reddit, VK, Habr, Pinterest, SoundCloud, and more).
- Uses response content evaluation to filter out "User Not Found" pages returning HTTP 200 statuses.

### 2. IP Geolocation & ASN Lookup
- Query integration via `ip-api`.
- Fetches country, region, city, ISP, organization, and ASN parameters.

### 3. Telecom & Phone Metadata
- Parses phone numbers globally using `phonenumbers`.
- Extracts carrier name, country, region, line type (Mobile / Fixed Line), and timezone details.

### 4. Email Discovery
- Public Gravatar profile verification via MD5 hashing.

### 5. Telegram Forwarded Message Analysis
- Extracts target User ID, display name, and username.
- Estimates Telegram registration timeframe based on User ID ranges.
- Links directly to profile entity trackers (SangMata history).

---

## Tech Stack

- **Framework:** `aiogram 3.x`
- **Network / HTTP:** `aiohttp`
- **Parsing & Metadata:** `phonenumbers`
- **Language:** Python 3.11

---

## Project Structure

```text
.
├── main.py                # Main dispatcher, input regex router, and handlers
├── config.py              # Environment configuration & bot token
├── modules/               # Core lookup modules
│   ├── username.py        # Asynchronous site scraper
│   ├── ip_lookup.py       # IP geolocation parser
│   ├── phone_lookup.py    # Telecom validation module
│   └── email_lookup.py    # Email profile checker
├── .gitignore             # Cache and environment file exclusions
└── README.md              # Documentation

Getting Started
Prerequisites

    Python 3.11 or higher

    Telegram Bot Token from @BotFather

Installation

    Clone the repository:
    Bash

    git clone [https://github.com/marsmarsssil100-ops/osint_bot_for_free.git](https://github.com/marsmarsssil100-ops/osint_bot_for_free.git)
    cd osint_bot_for_free

    Install required dependencies:
    Bash

    pip install aiogram aiohttp phonenumbers

    Configure API Token:
    Create or edit config.py in the root directory:
    Python

    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

    Launch the bot:
    Bash

    python main.py