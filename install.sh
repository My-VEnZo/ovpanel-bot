#!/bin/bash

echo "Installing OVPanel Bot..."

apt update -y
apt install python3 python3-pip -y

pip3 install -r requirements.txt

echo ""
read -p "🤖 Bot Token: " BOT_TOKEN
read -p "🆔 Admin Telegram ID: " ADMIN_ID

cat > .env <<EOF
BOT_TOKEN=$BOT_TOKEN
ADMIN_ID=$ADMIN_ID
EOF

export BOT_TOKEN=$BOT_TOKEN
export ADMIN_ID=$ADMIN_ID

echo "Starting bot..."
python3 bot.py
