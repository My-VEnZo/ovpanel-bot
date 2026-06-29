#!/bin/bash

echo "🚀 Installing OVPanel Bot..."

apt update -y
apt install python3 python3-pip -y

pip3 install python-telegram-bot==20.7 python-dotenv

echo ""
read -p "🤖 Bot Token: " BOT_TOKEN
read -p "🆔 Admin Telegram ID: " ADMIN_ID

# ساخت env دائمی
cat > .env <<EOF
BOT_TOKEN=$BOT_TOKEN
ADMIN_ID=$ADMIN_ID
EOF

echo "✅ ENV file created (.env)"

echo "▶ Starting bot..."
python3 bot.py
