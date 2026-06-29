import os
import concurrent.futures
import paramiko
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== ENV ==================
TOKEN = os.getenv("BOT_TOKEN")
SERVER_IP = os.getenv("SERVER_IP")
SERVER_USER = os.getenv("SERVER_USER")
SERVER_PASS = os.getenv("SERVER_PASS")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ================== THREAD POOL ==================
executor = concurrent.futures.ThreadPoolExecutor()

def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

# ================== SSH (NON-BLOCKING FIX) ==================
def ssh_exec(cmd):
    def run():
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            SERVER_IP,
            username=SERVER_USER,
            password=SERVER_PASS
        )

        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode()
        client.close()
        return output

    return executor.submit(run).result()

# ================== UI MENU ==================
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ساخت یوزر", callback_data="add")],
        [InlineKeyboardButton("❌ حذف یوزر", callback_data="del")],
        [InlineKeyboardButton("📄 لیست", callback_data="list")]
    ])

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text("🚀 VPN Panel Ready", reply_markup=menu())

# ================== BUTTON HANDLER ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data

    # ➕ CREATE USER
    if data == "add":
        username = "user" + str(os.getpid())

        # run openvpn script
        ssh_exec(f"printf '1\n{username}\n' | bash openvpn-install.sh")

        # find ovpn file
        file_name = ssh_exec(f"ls /root | grep {username} | head -n 1").strip()

        if file_name:
            file_path = f"/root/{file_name}"

            try:
                await query.message.reply_document(document=open(file_path, "rb"))
                await query.message.reply_text(f"✅ User created: {username}")
            except:
                await query.message.reply_text("❌ فایل پیدا نشد")

    # ❌ DELETE USER
    elif data == "del":
        ssh_exec("printf '2\n' | bash openvpn-install.sh")
        await query.message.reply_text("🗑 User deleted")

    # 📄 LIST USERS
    elif data == "list":
        res = ssh_exec("ls /root/*.ovpn 2>/dev/null")
        await query.message.reply_text(res or "Empty")

# ================== APP ==================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
