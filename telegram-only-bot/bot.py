#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Myanmar SME Telegram-Only Bot
Complete user engagement inside Telegram
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
import requests

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
BASE_URL = os.getenv('BASE_URL', 'https://your-domain.com')
PUBLIC_VIEW_URL = f"{BASE_URL}/telegram-only/public/index.html"
USER_DASHBOARD_URL = f"{BASE_URL}/telegram-only/dashboard/index.html"

class MyanmarSMEOnlyBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command and callback handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("dashboard", self.dashboard_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - Main entry point"""
        user = update.effective_user
        
        # Create welcome message with main choices
        welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {user.first_name}! 👋

Myanmar SME စီးပွားရေးစီမံခန့်ခွဲမှုစနစ်သို့ကြိုဆိုပါသည်!

ဘယ်လိုကူညွှန်ကြားချက်လိုအပ်ပါသလဲး?
        """
        
        # Create main choice buttons
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin နဲ့ဆက်သွယ်ရန်", callback_data="contact_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Myanmar SME Bot Help**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**

/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/dashboard - သင့်စီးပွားရေးဒက်ရှ်ဘုတ်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
📞 Admin နဲ့ဆက်သွယ်ရန်
📱 ဒက်ရှ်ဘုတ်အသုံးပြုရန်
💰 စျေးနှုန်းနှိုင်းများ

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com
        """
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /dashboard command - Direct access to user dashboard"""
        user = update.effective_user
        
        # Check if user has active subscription (you'd need to implement this check)
        has_subscription = await self.check_user_subscription(user.id)
        
        if not has_subscription:
            await self.show_subscription_required(update)
            return
        
        # Open user dashboard in Telegram
        await self.open_user_dashboard(update, user)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "explore_plans":
            await self.handle_explore_plans(query)
        elif query.data == "contact_admin":
            await self.handle_contact_admin(query)
        elif query.data == "view_pricing":
            await self.handle_view_pricing(query)
        elif query.data == "request_access":
            await self.handle_request_access(query)
        elif query.data == "start_trial":
            await self.handle_start_trial(query)
        elif query.data == "back_to_main":
            await self.back_to_main_menu(query)
    
    async def handle_explore_plans(self, query):
        """Handle 'Explore Plans' choice"""
        message_text = """
📋 **Myanmar SME စီးပွားရေးအစီအစဉ်များ**

ကျွန်ုပ်တို့၏စီးပွားရေးစီမံခန့်ခွဲမှုစနစ်များကိုကြည့်ရှုရန်:

🌐 **Public View ကိုဖွင့်ပါ**
• ကုမ္ပဏီအကြောင်းကိုယ်ရေး
• ဝန်ဆောင်မှုစာရင်း
• စျေးနှုန်းနှိုင်းများ
• ဆက်သွယ်ရန်ပုံစံ

အောက်တွင်ရှိတဲ့ခလုတ်ကိုနှိပ်ပြီး Public View ကိုကြည့်ရှုနိုင်ပါသည်။
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🌐 Public View ဖွင့်ရန်", web_app=WebAppInfo(url=PUBLIC_VIEW_URL))
            ],
            [
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing"),
                InlineKeyboardButton("🔑 Access တောင်းဆိုရန်", callback_data="request_access")
            ],
            [
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_contact_admin(self, query):
        """Handle 'Contact Admin' choice"""
        message_text = """
📞 **Admin နဲ့ဆက်သွယ်ရန်**

Admin နဲ့ဆက်သွယ်ရန်အတွက်:

📱 **ဖုန်းနံပါတ်:**
+959 123 456 789

📧 **အီးမေးလ်:**
info@myanmarsme.com

⏰ **ဆက်သွယ်နိုင်သောအချိန်:**
• တနင်္လာ - သောကြာ: 9:00 AM - 6:00 PM
• စနေ: 9:00 AM - 1:00 PM

**ဆက်သွယ်ရန်အကြောင်းကြားချက်:**
• Access Code တောင်းဆိုရန်
• စနစ်အသုံးပြုရန်
• အကူညွှန်ကြားချက်ရယူရန်
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔑 Access Code တောင်းဆိုရန်", callback_data="request_access"),
                InlineKeyboardButton("🌐 Public View ကြည့်ရန်", callback_data="explore_plans")
            ],
            [
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_view_pricing(self, query):
        """Handle pricing view"""
        message_text = """
💰 **စျေးနှုန်းနှိုင်းများ**

**စားသုံးသူစနစ်များ:**

📅 **1 လအတွက်**
• စျေးနှုန်း: 15,000 Ks
• အင်္ဂါရပ်: အခြေခံစီမံခန့်ခွဲမှု
• ကုန်ပစ္စည်း: 50 ခုအထိ
• အရောင်းအဝယ်: နေ့စဉ် 100 ခုအထိ

📅 **3 လအတွက်**
• စျေးနှုန်း: 40,000 Ks
• အင်္ဂါရပ်: အဆင့်မြင့်စီမံခန့်ခွဲမှု
• ကုန်ပစ္စည်း: 200 ခုအထိ
• အရောင်းအဝယ်: နေ့စဉ် 500 ခုအထိ

📅 **1 နှစ်အတွက်**
• စျေးနှုန်း: 150,000 Ks
• အင်္ဂါရပ်: အပြည့်အစုံစီမံခန့်ခွဲမှု
• ကုန်ပစ္စည်း: ကန့်သတ်မရှိ
• အရောင်းအဝယ်: ကန့်သတ်မရှိ

**အကျိုးခံစားခွင့်များ:**
• စီးပွားရေးခန့်မှန်းချက်များ
• ကုန်ပစ္စည်းစီမံခန့်ခွဲမှု
• အရောင်းအဝယ်မှတ်တမ်းများ
• Telegram ထဲမှာပဲအသုံးပြုနိုင်
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔰 Trial စမ်းသုံးရန်", callback_data="start_trial"),
                InlineKeyboardButton("🔑 Access Code တောင်းဆိုရန်", callback_data="request_access")
            ],
            [
                InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="contact_admin"),
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_request_access(self, query):
        """Handle access request"""
        message_text = """
🔑 **Access Code တောင်းဆိုရန်**

Access Code ရယူရန်အတွက်အဆင့်များ:

1️⃣ **စီးပွားရေးအစီအစဉ်များကြည့်ပါ**
   • Public View မှာဝန်ဆောင်မှုများကြည့်ရှု

2️⃣ **Contact Form ဖြည့်စွက်ပါ**
   • သင့်စီးပွားရေးလိုအပ်ချက်များဖော်ပြ

3️⃣ **Admin ဆက်သွယ်ပါ**
   • ဖုန်းဖြင့်ဆက်သွယ်ပြီးအကြောင်းကြား

4️⃣ **Access Code ရယူပါ**
   • Admin မှ Access Code ထုတ်ပေးမည်

5️⃣ **စနစ်အတွင်းဝင်ပါ**
   • Code ဖြင့် Dashboard အသုံးပြုနိုင်

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🌐 Public View ဖွင့်ရန်", web_app=WebAppInfo(url=PUBLIC_VIEW_URL))
            ],
            [
                InlineKeyboardButton("📞 Admin ခေါ်ဆိုရန်", callback_data="contact_admin"),
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_start_trial(self, query):
        """Handle trial start"""
        message_text = """
🔰 **Trial စမ်းသုံးရန်**

Trial စမ်းသုံးရန်အတွက်:

✅ **7 ရက်အခမဲ့ Trial**
• အခြေခံအင်္ဂါရပ်များအားလုံး
• ကုန်ပစ္စည်း 10 ခုအထိ
• အရောင်းအဝယ် နေ့စဉ် 20 ခုအထိ

**Trial စတင်ရန်:**
1. အောက်တွင်ရှိတဲ့ "Trial စတင်ရန်" နှိပ်ပါ
2. သင့်အချက်အလက်များဖြည့်စွက်ပါ
3. Trial စတင်ပြီး Dashboard အသုံးပြုနိုင်

**သတိပြုရန်:**
• Trial ကာလကုန်ဆုံးပါက စားသုံးခလုတ်ပေးရပါမည်
• ဒေတာများမပျက်စီးပါ
• မည်သည့်ကတ်မှားမျှမလိုအပ်ပါ
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🚀 Trial စတင်ရန်", web_app=WebAppInfo(url=f"{PUBLIC_VIEW_URL}?trial=true"))
            ],
            [
                InlineKeyboardButton("💰 စားသုံးခလုတ်ပေးရန်", callback_data="view_pricing"),
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def back_to_main_menu(self, query):
        """Return to main menu"""
        user = query.from_user
        
        welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {user.first_name}! 👋

ဘယ်လိုကူညွှန်ကြားချက်လိုအပ်ပါသလဲး?
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin နဲ့ဆက်သွယ်ရန်", callback_data="contact_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def open_user_dashboard(self, update, user):
        """Open user dashboard in Telegram"""
        dashboard_url = f"{USER_DASHBOARD_URL}?user_id={user.id}"
        
        message_text = f"""
📱 **{user.first_name} ၏ စီးပွားရေးဒက်ရှ်ဘုတ်**

သင့်စီးပွားရေးဒက်ရှ်ဘုတ်ကိုဖွင့်ရန်:

အောက်တွင်ရှိတဲ့ "ဒက်ရှ်ဘုတ်ဖွင့်ရန်" ခလုတ်ကိုနှိပ်ပါ
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📱 ဒက်ရှ်ဘုတ်ဖွင့်ရန်", web_app=WebAppInfo(url=dashboard_url))
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_subscription_required(self, update):
        """Show subscription required message"""
        message_text = """
🔒 **Subscription လိုအပ်ပါသည်**

ဒက်ရှ်ဘုတ်အသုံးပြုရန်အတွက် active subscription လိုအပ်ပါသည်။

**Subscription ရယူရန်:**
1. စီးပွားရေးအစီအစဉ်များကြည့်ရန်
2. Admin နဲ့ဆက်သွယ်ပါ
3. Access Code ရယူပါ
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin နဲ့ဆက်သွယ်ရန်", callback_data="contact_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def check_user_subscription(self, telegram_user_id):
        """Check if user has active subscription"""
        # This would connect to your user service API
        # For now, return False (no subscription)
        # In production, you'd make an API call to your user service
        return False
    
    def run(self):
        """Start the bot"""
        print("🤖 Myanmar SME Telegram-Only Bot is starting...")
        print(f"🌐 Public View URL: {PUBLIC_VIEW_URL}")
        print(f"📱 Dashboard URL: {USER_DASHBOARD_URL}")
        
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    bot = MyanmarSMEOnlyBot()
    bot.run()

if __name__ == '__main__':
    main()
