import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================= ENV =================
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ================= CHECK ADMIN =================
def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

# ================= RUN CMD =================
def run(cmd):
    return subprocess.getoutput(cmd)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    await update.message.reply_text(
        "🚀 VPN Bot Ready\n\nCommands:\n/add name\n/delete name\n/list"
    )

# ================= ADD USER =================
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /add username")
        return

    username = context.args[0]

    await update.message.reply_text(f"⏳ Creating {username} ...")

    # ساخت یوزر
    run(f"printf '1\n{username}\n' | bash /root/openvpn-install.sh")

    # پیدا کردن فایل ovpn
    file = run(f"ls /root | grep {username} | head -n 1").strip()

    if file:
        try:
            await update.message.reply_document(open(f"/root/{file}", "rb"))
            await update.message.reply_text(f"✅ Created: {username}")
        except:
            await update.message.reply_text("❌ File not found")
    else:
        await update.message.reply_text("❌ Failed to create user")

# ================= DELETE USER =================
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /delete username")
        return

    username = context.args[0]

    await update.message.reply_text(f"⏳ Deleting {username} ...")

    run("printf '2\n' | bash /root/openvpn-install.sh")

    await update.message.reply_text(f"❌ Deleted: {username}")

# ================= LIST USERS =================
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    res = run("ls /root/*.ovpn 2>/dev/null")
    await update.message.reply_text(res or "Empty")

# ================= APP =================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("delete", delete))
app.add_handler(CommandHandler("list", list_users))

app.run_polling()
