# ezosell_bot.py - Customer Bot

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from database import Session, Seller, Order
from datetime import datetime, timedelta
import requests
import re
import os

# ===== YAHAN APNA BOT TOKEN DAALO =====
BOT_TOKEN = "8764794732:AAE9hX8Mpkddso6XZGKJgq8Pbr2RjuSquuA"  # Customer bot token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    phone = str(user_id)
    
    db = Session()
    seller = db.query(Seller).filter(Seller.phone == phone).first()
    
    if not seller:
        await update.message.reply_text(
            "👋 नमस्ते! मैं EzoSell हूँ - आपका ऑनलाइन सेलिंग असिस्टेंट!\n\n"
            "📝 सबसे पहले अपना नाम बताएं:\n"
            'जैसे: "मेरा नाम रमेश है"'
        )
        context.user_data['waiting_for_name'] = True
    else:
        await show_menu(update, seller)
    db.close()

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    user_id = update.effective_user.id
    phone = str(user_id)
    
    if 'मेरा नाम' in name or 'mera naam' in name.lower():
        name = name.lower().replace('mera naam', '').replace('है', '').strip()
    
    db = Session()
    new_seller = Seller(
        name=name[:50],
        phone=phone,
        free_trial_end=datetime.now() + timedelta(days=7)
    )
    db.add(new_seller)
    db.commit()
    
    await update.message.reply_text(
        f"✅ वेलकम {name}!\n\n"
        "📋 *कमांड्स:*\n"
        "🔍 `search [प्रोडक्ट]` - प्रोडक्ट सर्च\n"
        "➕ `add [नाम] [कीमत] [स्टॉक]` - प्रोडक्ट ऐड\n"
        "📦 `orders` - ऑर्डर देखें\n"
        "💰 `profit` - प्रॉफिट देखें\n"
        "❓ `help` - सभी कमांड्स",
        parse_mode="Markdown"
    )
    context.user_data.clear()
    db.close()

async def show_menu(update, seller):
    menu = f"""
✅ *वेलकम {seller.name}!*
📊 *आपके आंकड़े:*
• कुल बिक्री: ₹{seller.total_sales:,.2f}
• फ्री ट्रायल: {max(0, (seller.free_trial_end - datetime.now()).days)} दिन बचे
"""
    await update.message.reply_text(menu, parse_mode="Markdown")

async def search_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.replace('search', '').strip()
    if not query:
        await update.message.reply_text("❌ तरीका: `search [प्रोडक्ट]`", parse_mode="Markdown")
        return
    
    await update.message.reply_text(f"🔍 *'{query}' ढूंढ रहा हूँ...*", parse_mode="Markdown")
    
    response = f"📦 *'{query}' के रिजल्ट:*\n\n"
    response += "*Flipkart:*\n  • {query} - ₹999\n"
    response += "*Meesho:*\n  • {query} - ₹799\n"
    response += "*Myntra:*\n  • {query} - ₹1,499\n"
    await update.message.reply_text(response, parse_mode="Markdown")

async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    parts = msg.replace('add', '').strip().split()
    if len(parts) < 3:
        await update.message.reply_text("❌ तरीका: `add [नाम] [कीमत] [स्टॉक]`", parse_mode="Markdown")
        return
    
    price = parts[-2]
    stock = parts[-1]
    name = ' '.join(parts[:-2])
    
    await update.message.reply_text(f"✅ *प्रोडक्ट ऐड हो गया!*\n📦 {name}\n💰 ₹{price}\n📊 स्टॉक: {stock}", parse_mode="Markdown")

async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📦 *अभी कोई ऑर्डर नहीं है*", parse_mode="Markdown")

async def show_profit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 *अभी कोई प्रॉफिट नहीं है*", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 *EzoSell हेल्प*
🔍 `search [प्रोडक्ट]` - सर्च
➕ `add [नाम] [कीमत] [स्टॉक]` - प्रोडक्ट ऐड
📦 `orders` - ऑर्डर
💰 `profit` - प्रॉफिट
❓ `help` - हेल्प
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_name'):
        await handle_name(update, context)
        return
    
    msg = update.message.text.lower()
    if msg.startswith('search'):
        await search_product(update, context)
    elif msg.startswith('add'):
        await add_product(update, context)
    elif msg in ['orders', 'order']:
        await show_orders(update, context)
    elif msg in ['profit', 'profits']:
        await show_profit(update, context)
    elif msg in ['help', 'start']:
        await help_command(update, context)
    else:
        await update.message.reply_text("❌ समझ नहीं आया। `help` टाइप करें", parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 EzoSell Customer Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()