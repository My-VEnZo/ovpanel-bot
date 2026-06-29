import os
import paramiko
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
SERVER = os.getenv("SERVER_IP")
USER = os.getenv("SERVER_USER")
PASS = os.getenv("SERVER_PASS")


def ssh_exec(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USER, password=PASS)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    ssh.close()
    return out


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ساخت یوزر", callback_data="add")],
        [InlineKeyboardButton("❌ حذف یوزر", callback_data="del")],
        [InlineKeyboardButton("📋 لیست یوزرها", callback_data="list")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("VPN Manager 🚀", reply_markup=main_menu())


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # ➕ ساخت یوزر
    if data == "add":
        username = f"user{os.getpid()}"
        ssh_exec(f"printf '1\n{username}\n' | bash openvpn-install.sh")

        # پیدا کردن فایل
        file_name = ssh_exec(f"ls /root | grep {username} | head -n 1").strip()

        if file_name:
            path = f"/root/{file_name}"
            await query.message.reply_document(document=open(path, "rb"))
            await query.message.reply_text(f"User created: {username} ✅")

    # ❌ حذف یوزر
    elif data == "del":
        ssh_exec("printf '2\n' | bash openvpn-install.sh")
        await query.message.reply_text("User removed ❌")

    # 📋 لیست
    elif data == "list":
        res = ssh_exec("ls /root/*.ovpn 2>/dev/null")
        await query.message.reply_text(res or "No users found")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
