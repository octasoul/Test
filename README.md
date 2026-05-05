# 🤖 Telegram Background Remover Bot

A **100% free**, 24/7 Telegram bot that removes image backgrounds using `rembg` — no paid APIs, no limits!

---

## ✅ Features

- Removes background from any photo instantly
- Supports sending as photo or document (document = better quality)
- Returns PNG with transparent background
- Fully local processing — no third-party API needed
- Free forever

---

## 🚀 Setup Guide

### 1. Get Your Bot Token
1. Open Telegram → message **@BotFather**
2. Send `/newbot`
3. Follow steps → copy your **token**

---

### 2. Run Locally (for testing)

```bash
# Clone or download this folder
cd tg-bg-remover

# Install dependencies
pip install -r requirements.txt

# Set your token and run
export BOT_TOKEN="your_token_here"
python bot.py
```

---

### 3. Deploy Free 24/7 on Railway

**Railway** gives you free hours (enough for a bot).

1. Go to https://railway.app → sign up (free)
2. Click **New Project** → **Deploy from GitHub repo**
   - Push this folder to a GitHub repo first
3. In Railway dashboard → **Variables** tab:
   - Add `BOT_TOKEN` = your Telegram token
4. Deploy! Railway auto-detects Python and runs `python bot.py`

---

### 4. Alternative: Deploy on Render (also free)

1. Go to https://render.com → sign up
2. New → **Background Worker** (not Web Service!)
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `python bot.py`
6. Add env var: `BOT_TOKEN` = your token
7. Deploy!

> ⚠️ Use **Background Worker** on Render, NOT Web Service — bots don't need HTTP ports.

---

## 📁 File Structure

```
tg-bg-remover/
├── bot.py            # Main bot code
├── requirements.txt  # Python dependencies
├── Procfile          # For Railway/Heroku
├── railway.toml      # Railway config
└── README.md         # This file
```

---

## 🛠 How It Works

1. User sends a photo to the bot
2. Bot downloads the image
3. `rembg` library runs a local AI model (U2Net) to detect and remove background
4. Bot sends back a PNG with transparent background

No API keys. No rate limits. No cost.

---

## ⚡ First Run Note

On the very first run, `rembg` will **auto-download the AI model** (~170MB). This only happens once and is cached automatically.
