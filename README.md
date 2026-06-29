from pathlib import Path

content = """# 📌 OVPanel Bot

Telegram bot for managing OpenVPN users (create, delete, and download `.ovpn` config files directly from Telegram).

---

# 🚀 Features

- ➕ Create OpenVPN users from Telegram
- ❌ Delete VPN users
- 📄 List all VPN config files
- 📥 Send `.ovpn` file directly in Telegram
- 🔐 Admin-only access (Telegram ID restriction)
- ⚡ Easy install with one script
- 🖥️ Works on Ubuntu VPS

---

# ⚠️ IMPORTANT: Install OpenVPN First

Before installing this bot, you MUST install OpenVPN on your server.

👉 Run this command:

wget https://git.io/vpn -O openvpn-install.sh && bash openvpn-install.sh

✔ During installation:
- Choose UDP or TCP
- Use default port (recommended)
- Create at least one client (optional)

---

# 🖥️ Installation Guide

## 1. Update server & install git

apt update -y
apt install git -y

---

## 2. Clone the repository

git clone https://github.com/My-VEnZo/ovpanel-bot
cd ovpanel-bot

---

## 3. Run installer

chmod +x install.sh
./install.sh

---

## 4. Setup configuration

Bot Token:
Server IP:
Server User (root):
Server Password:
Admin Telegram ID:

---

# 📲 Bot Usage

/start

Buttons:
➕ Create VPN User
❌ Delete User
📄 List Users

---

# 📥 Output Example

✔ .ovpn file sent to Telegram
✔ Ready for OpenVPN apps

---

# 🧠 How It Works

Telegram Bot
→ SSH to VPS
→ run openvpn-install.sh
→ manage users
→ send config file

---

# 🔐 Security Notes

- Only admin can use bot
- Do NOT expose SSH credentials
- Prefer SSH key instead of password

---

# ⚡ Requirements

- Ubuntu VPS 20/22/24
- Python 3
- OpenVPN installed
- Root access

---

# 📌 Install OpenVPN

wget https://git.io/vpn -O openvpn-install.sh && bash openvpn-install.sh

---

# 💡 Author

Telegram OpenVPN management bot
"""

file_path = Path("/mnt/data/README.md")
file_path.write_text(content)

file_path.name
