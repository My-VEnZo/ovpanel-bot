import os
import paramiko
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# گرفتن اطلاعات از محیط
TOKEN = os.getenv("BOT_TOKEN")
SERVER_IP = os.getenv("SERVER_IP")
SERVER_USER = os.getenv("SERVER_USER")
SERVER_PASS = os.getenv("SERVER_PASS")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID


def ssh(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS)

    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    client.close()
    return out


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ساخت یوزر", callback_data="add")],
        [InlineKeyboardButton("❌ حذف یوزر", callback_data="del")],
        [InlineKeyboardButton("📄 لیست", callback_data="list")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text("VPN Panel 🚀", reply_markup=menu())


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data

    # ➕ ساخت یوزر
    if data == "add":
        username = "user" + str(os.getpid())

        ssh(f"printf '1\n{username}\n' | bash openvpn-install.sh")

        file = ssh(f"ls /root | grep {username} | head -n 1").strip()

        if file:
            path = f"/root/{file}"
            await query.message.reply_document(document=open(path, "rb"))
            await query.message.reply_text(f"Created: {username} ✅")

    # ❌ حذف یوزر
    elif data == "del":
        ssh("printf '2\n' | bash openvpn-install.sh")
        await query.message.reply_text("Deleted ❌")

    # 📄 لیست
    elif data == "list":
        res = ssh("ls /root/*.ovpn 2>/dev/null")
        await query.message.reply_text(res or "Empty")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
