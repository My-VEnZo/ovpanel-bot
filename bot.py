import os
import asyncio
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ================== SECURITY ==================
def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

# ================== RUN SAFE (NO HANG CORE) ==================
async def run_cmd(cmd: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: subprocess.getoutput(cmd))

# ================== UI ==================
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
    await update.message.reply_text("🚀 VPN Panel (NO HANG VERSION)", reply_markup=menu())

# ================== BUTTONS ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer("⏳ در حال انجام...")

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data

    # ================= CREATE USER =================
    if data == "add":
        username = "user" + str(os.getpid())

        await run_cmd(f"printf '1\n{username}\n' | bash /root/openvpn-install.sh")

        file = subprocess.getoutput(f"ls /root | grep {username} | head -n 1").strip()

        if file:
            try:
                await query.message.reply_document(open(f"/root/{file}", "rb"))
                await query.message.reply_text(f"✅ Created: {username}")
            except:
                await query.message.reply_text("❌ فایل پیدا نشد")

    # ================= DELETE USER =================
    elif data == "del":
        await run_cmd("printf '2\n' | bash /root/openvpn-install.sh")
        await query.message.reply_text("❌ Deleted")

    # ================= LIST =================
    elif data == "list":
        res = subprocess.getoutput("ls /root/*.ovpn 2>/dev/null")
        await query.message.reply_text(res or "Empty")

# ================== APP ==================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
