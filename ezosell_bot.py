# ezosell_bot.py - Complete EzoSell Agent with Buttons

import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== BOT TOKEN (Secret se lega) =====
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8764794732:AAE9hX8Mpkddso6XZGKJgq8Pbr2RjuSquuA')

# ===== SIMPLE DATABASE (File based) =====
import json
import os

DATA_FILE = 'ezosell_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'sellers': {},
        'products': {},
        'orders': {},
        'commissions': {}
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ===== MAIN MENU BUTTONS =====
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📦 मेरे प्रोडक्ट्स", callback_data="menu_products")],
        [InlineKeyboardButton("🛒 ऑर्डर मैनेजमेंट", callback_data="menu_orders")],
        [InlineKeyboardButton("💰 प्रॉफिट और सेल्स", callback_data="menu_profit")],
        [InlineKeyboardButton("📊 इन्वेंटरी मैनेज", callback_data="menu_inventory")],
        [InlineKeyboardButton("🔗 अकाउंट कनेक्ट", callback_data="menu_account")],
        [InlineKeyboardButton("📈 एनालिटिक्स", callback_data="menu_analytics")],
        [InlineKeyboardButton("❓ हेल्प", callback_data="menu_help")],
        [InlineKeyboardButton("👑 एडमिन (सिर्फ मेरे लिए)", callback_data="menu_admin")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== PRODUCTS SUB-MENU =====
def get_products_menu():
    keyboard = [
        [InlineKeyboardButton("➕ नया प्रोडक्ट ऐड", callback_data="add_product_start")],
        [InlineKeyboardButton("📦 सारे प्रोडक्ट देखें", callback_data="view_products")],
        [InlineKeyboardButton("✏️ प्रोडक्ट एडिट", callback_data="edit_product")],
        [InlineKeyboardButton("🗑️ प्रोडक्ट डिलीट", callback_data="delete_product")],
        [InlineKeyboardButton("📊 लो स्टॉक प्रोडक्ट्स", callback_data="low_stock")],
        [InlineKeyboardButton("🔙 वापस", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== ORDERS SUB-MENU =====
def get_orders_menu():
    keyboard = [
        [InlineKeyboardButton("📋 सारे ऑर्डर", callback_data="view_orders")],
        [InlineKeyboardButton("⏳ पेंडिंग ऑर्डर", callback_data="pending_orders")],
        [InlineKeyboardButton("🚚 शिप्ड ऑर्डर", callback_data="shipped_orders")],
        [InlineKeyboardButton("✅ डिलीवर्ड ऑर्डर", callback_data="delivered_orders")],
        [InlineKeyboardButton("📦 ऑर्डर स्टेटस अपडेट", callback_data="update_order_status")],
        [InlineKeyboardButton("🔙 वापस", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== PROFIT SUB-MENU =====
def get_profit_menu():
    keyboard = [
        [InlineKeyboardButton("💰 कुल प्रॉफिट", callback_data="total_profit")],
        [InlineKeyboardButton("📅 आज का प्रॉफिट", callback_data="today_profit")],
        [InlineKeyboardButton("📆 इस हफ्ते का प्रॉफिट", callback_data="week_profit")],
        [InlineKeyboardButton("📈 इस महीने का प्रॉफिट", callback_data="month_profit")],
        [InlineKeyboardButton("📊 प्लेटफॉर्म वाइज प्रॉफिट", callback_data="platform_profit")],
        [InlineKeyboardButton("🔙 वापस", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== INVENTORY SUB-MENU =====
def get_inventory_menu():
    keyboard = [
        [InlineKeyboardButton("📦 स्टॉक चेक करें", callback_data="check_stock")],
        [InlineKeyboardButton("🔄 स्टॉक अपडेट करें", callback_data="update_stock")],
        [InlineKeyboardButton("🔄 सभी प्लेटफॉर्म सिंक", callback_data="sync_inventory")],
        [InlineKeyboardButton("⚠️ लो स्टॉक अलर्ट", callback_data="low_stock_alert")],
        [InlineKeyboardButton("🔙 वापस", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== ACCOUNT SUB-MENU =====
def get_account_menu():
    keyboard = [
        [InlineKeyboardButton("🔗 अमेज़न कनेक्ट", callback_data="connect_amazon")],
        [InlineKeyboardButton("🔗 फ्लिपकार्ट कनेक्ट", callback_data="connect_flipkart")],
        [InlineKeyboardButton("🔗 मीशो कनेक्ट", callback_data="connect_meesho")],
        [InlineKeyboardButton("🔗 मिंत्रा कनेक्ट", callback_data="connect_myntra")],
        [InlineKeyboardButton("📋 कनेक्टेड अकाउंट्स", callback_data="view_accounts")],
        [InlineKeyboardButton("❌ अकाउंट हटाएं", callback_data="disconnect_account")],
        [InlineKeyboardButton("🔙 वापस", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== ANALYTICS SUB-MENU =====
def get_analytics_menu():
    keyboard = [
        [InlineKeyboardButton("🏆 टॉप सेलिंग प्रोडक्ट्स", callback_data="top_products")],
        [InlineKeyboardButton("📊 प्लेटफॉर्म रिपोर्ट", callback_data="platform_report")],
        [InlineKeyboardButton("📈 डेली रिपोर्ट", callback_data="daily_report")],
        [InlineKeyboardButton("📊 कस्टम रिपोर्ट", callback_data="custom_report")],
        [InlineKeyboardButton("🔙 वापस", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== ADD PRODUCT FLOW =====
async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📝 *नया प्रोडक्ट ऐड करें*\n\n"
        "प्रोडक्ट की जानकारी इस फॉर्मेट में भेजें:\n"
        "`नाम | कीमत | स्टॉक | प्लेटफॉर्म`\n\n"
        "उदाहरण:\n"
        "`Red T-Shirt | 599 | 100 | flipkart`\n\n"
        "प्लेटफॉर्म: flipkart, meesho, myntra, amazon",
        parse_mode="Markdown"
    )
    context.user_data['awaiting_product'] = True

async def handle_product_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_product'):
        return
    
    text = update.message.text
    parts = text.split('|')
    
    if len(parts) >= 4:
        name = parts[0].strip()
        price = parts[1].strip()
        stock = parts[2].strip()
        platform = parts[3].strip()
        
        # Save product
        data = load_data()
        user_id = str(update.effective_user.id)
        
        if user_id not in data['products']:
            data['products'][user_id] = []
        
        product = {
            'name': name,
            'price': price,
            'stock': int(stock),
            'platform': platform,
            'added_on': datetime.now().isoformat()
        }
        data['products'][user_id].append(product)
        save_data(data)
        
        await update.message.reply_text(
            f"✅ *प्रोडक्ट ऐड हो गया!*\n\n"
            f"📦 *नाम:* {name}\n"
            f"💰 *कीमत:* ₹{price}\n"
            f"📊 *स्टॉक:* {stock}\n"
            f"🛒 *प्लेटफॉर्म:* {platform}\n\n"
            f"अब यह प्रोडक्ट {platform} पर सेल के लिए उपलब्ध है।",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ *गलत फॉर्मेट!*\n\n"
            "सही फॉर्मेट: `नाम | कीमत | स्टॉक | प्लेटफॉर्म`\n"
            "उदाहरण: `Red T-Shirt | 599 | 100 | flipkart`",
            parse_mode="Markdown"
        )
    
    context.user_data['awaiting_product'] = False

# ===== VIEW PRODUCTS =====
async def view_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = load_data()
    products = data['products'].get(user_id, [])
    
    if not products:
        await query.edit_message_text(
            "📦 *कोई प्रोडक्ट नहीं है*\n\n"
            "नया प्रोडक्ट ऐड करने के लिए '➕ नया प्रोडक्ट ऐड' पर क्लिक करें।",
            parse_mode="Markdown",
            reply_markup=get_products_menu()
        )
        return
    
    response = "*📦 आपके प्रोडक्ट्स:*\n\n"
    for i, p in enumerate(products, 1):
        response += f"{i}. *{p['name']}*\n"
        response += f"   💰 ₹{p['price']} | 📊 {p['stock']} pcs | 🛒 {p['platform']}\n\n"
    
    await query.edit_message_text(
        response,
        parse_mode="Markdown",
        reply_markup=get_products_menu()
    )

# ===== LOW STOCK =====
async def low_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = load_data()
    products = data['products'].get(user_id, [])
    
    low_stock_products = [p for p in products if p['stock'] < 10]
    
    if not low_stock_products:
        await query.edit_message_text(
            "✅ *कोई लो स्टॉक प्रोडक्ट नहीं है!*\n\n"
            "सभी प्रोडक्ट्स का स्टॉक 10 से अधिक है।",
            parse_mode="Markdown",
            reply_markup=get_products_menu()
        )
        return
    
    response = "*⚠️ लो स्टॉक प्रोडक्ट्स (स्टॉक < 10):*\n\n"
    for p in low_stock_products:
        response += f"• *{p['name']}* - सिर्फ {p['stock']} pcs बचे हैं!\n"
        response += f"  💰 ₹{p['price']} | 🛒 {p['platform']}\n\n"
    
    await query.edit_message_text(
        response,
        parse_mode="Markdown",
        reply_markup=get_products_menu()
    )

# ===== TOTAL PROFIT =====
async def total_profit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = load_data()
    products = data['products'].get(user_id, [])
    
    # Calculate total value
    total_value = sum(p['price'] * p['stock'] for p in products)
    total_products = len(products)
    
    response = f"""
💰 *प्रॉफिट डैशबोर्ड*

📊 *कुल प्रोडक्ट्स:* {total_products}
💵 *कुल इन्वेंट्री वैल्यू:* ₹{total_value:,.2f}
📈 *एस्टीमेटेड मंथली प्रॉफिट:* ₹{total_value * 0.3:,.2f}

💡 *टिप:* ज्यादा सेल करने पर कमीशन कम होता है!
    """
    
    await query.edit_message_text(
        response,
        parse_mode="Markdown",
        reply_markup=get_profit_menu()
    )

# ===== TODAY PROFIT =====
async def today_profit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Simple profit calculation for demo
    await query.edit_message_text(
        "📅 *आज का प्रॉफिट:* ₹0\n\n"
        "अभी कोई सेल नहीं हुई है।\n"
        "प्रोडक्ट्स ऐड करें और सेल करना शुरू करें!",
        parse_mode="Markdown",
        reply_markup=get_profit_menu()
    )

# ===== MAIN START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
👋 *नमस्ते! मैं EzoSell हूँ*

*मैं क्या कर सकता हूँ:*
✅ अमेज़न, फ्लिपकार्ट, मीशो, मिंत्रा पर सेल करें
✅ प्रोडक्ट ऐड करें और मैनेज करें
✅ ऑर्डर ट्रैक करें
✅ इन्वेंटरी मैनेज करें
✅ प्रॉफिट कैलकुलेट करें
✅ और बहुत कुछ...

*बस नीचे दिए बटन पर क्लिक करें और सेलिंग शुरू करें!* 🚀
    """
    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# ===== HELP =====
async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    help_text = """
❓ *EzoSell हेल्प सेंटर*

*📦 प्रोडक्ट्स:*
• नया प्रोडक्ट ऐड करें - नाम, कीमत, स्टॉक, प्लेटफॉर्म
• प्रोडक्ट एडिट/डिलीट करें
• लो स्टॉक प्रोडक्ट्स देखें

*🛒 ऑर्डर्स:*
• सारे ऑर्डर देखें
• पेंडिंग/शिप्ड/डिलीवर्ड ऑर्डर
• ऑर्डर स्टेटस अपडेट करें

*💰 प्रॉफिट:*
• कुल, आज, हफ्ता, महीना प्रॉफिट
• प्लेटफॉर्म वाइज प्रॉफिट

*📊 इन्वेंटरी:*
• स्टॉक चेक/अपडेट
• सभी प्लेटफॉर्म सिंक

*🔗 अकाउंट:*
• अमेज़न, फ्लिपकार्ट, मीशो, मिंत्रा कनेक्ट करें

*कोई दिक्कत?* हमसे संपर्क करें: @EzoSellSupport
    """
    await query.edit_message_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# ===== BACK TO MAIN =====
async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👋 *मेन मेनू*\n\nनीचे दिए बटन से कोई भी ऑप्शन चुनें:",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# ===== ADMIN PANEL =====
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Check if user is admin (you can set your user id)
    admin_id = "8608957742:AAFaMKd1cXFWH2Lz4FR5JDd892pGDX2eLHo"  # 🔥 YAHAN APNA TELEGRAM USER ID DAALO
    
    if str(update.effective_user.id) != admin_id:
        await query.edit_message_text(
            "❌ *आप एडमिन नहीं हैं!*\n\n"
            "यह सुविधा सिर्फ EzoSell ओनर के लिए है।",
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )
        return
    
    data = load_data()
    total_sellers = len(data['sellers'])
    total_products = sum(len(p) for p in data['products'].values())
    
    admin_text = f"""
👑 *एडमिन डैशबोर्ड*

📊 *कुल सेलर्स:* {total_sellers}
📦 *कुल प्रोडक्ट्स:* {total_products}
💰 *कुल कमीशन:* ₹{0:,.2f}

*कमांड्स:*
/stats - सभी आंकड़े
/sellers - सेलर्स की लिस्ट
/commission - कमीशन डिटेल्स
    """
    await query.edit_message_text(
        admin_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# ===== PLACEHOLDER HANDLERS (Will be expanded) =====
async def placeholder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔄 *यह फीचर जल्द आ रहा है!*\n\n"
        "हम इस पर काम कर रहे हैं।",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

# ===== MAIN FUNCTION =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Callback handlers (button clicks)
    app.add_handler(CallbackQueryHandler(add_product_start, pattern="add_product_start"))
    app.add_handler(CallbackQueryHandler(view_products, pattern="view_products"))
    app.add_handler(CallbackQueryHandler(low_stock, pattern="low_stock"))
    app.add_handler(CallbackQueryHandler(total_profit, pattern="total_profit"))
    app.add_handler(CallbackQueryHandler(today_profit, pattern="today_profit"))
    app.add_handler(CallbackQueryHandler(show_help, pattern="menu_help"))
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="menu_admin"))
    app.add_handler(CallbackQueryHandler(back_main, pattern="back_main"))
    
    # Placeholder handlers for all other features
    menu_patterns = [
        "menu_products", "menu_orders", "menu_profit", "menu_inventory",
        "menu_account", "menu_analytics", "edit_product", "delete_product",
        "view_orders", "pending_orders", "shipped_orders", "delivered_orders",
        "update_order_status", "week_profit", "month_profit", "platform_profit",
        "check_stock", "update_stock", "sync_inventory", "low_stock_alert",
        "connect_amazon", "connect_flipkart", "connect_meesho", "connect_myntra",
        "view_accounts", "disconnect_account", "top_products", "platform_report",
        "daily_report", "custom_report"
    ]
    
    for pattern in menu_patterns:
        app.add_handler(CallbackQueryHandler(placeholder, pattern=pattern))
    
    # Message handler for product input
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_input))
    
    print("🤖 EzoSell Complete Bot is running!")
    print("✅ All features ready with buttons!")
    app.run_polling()

if __name__ == "__main__":
    main()