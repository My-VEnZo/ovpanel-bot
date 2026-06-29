#!/bin/bash

echo "===== OVPanel Installer ====="

read -p "🤖 Telegram Bot Token: " BOT_TOKEN
read -p "🌐 Server IP: " SERVER_IP
read -p "👤 Server User (root): " SERVER_USER
read -s -p "🔑 Server Password: " SERVER_PASS
echo ""
read -p "🆔 Admin Telegram ID: " ADMIN_ID

echo "Installing packages..."

apt update -y
apt install python3 python3-pip -y

pip3 install python-telegram-bot==20.7 paramiko

echo "Creating env file..."

cat > .env <<EOF
BOT_TOKEN=$BOT_TOKEN
SERVER_IP=$SERVER_IP
SERVER_USER=$SERVER_USER
SERVER_PASS=$SERVER_PASS
ADMIN_ID=$ADMIN_ID
EOF

echo "Starting bot..."

export BOT_TOKEN=$BOT_TOKEN
export SERVER_IP=$SERVER_IP
export SERVER_USER=$SERVER_USER
export SERVER_PASS=$SERVER_PASS
export ADMIN_ID=$ADMIN_ID

python3 bot.py
