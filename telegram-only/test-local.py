#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Myanmar SME Bot - Local Testing
Test your bot without deployment
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = "8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU"

class MyanmarSMETestBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command and callback handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("test", self.test_command))
        self.app.add_handler(CommandHandler("popup", self.popup_test_command))
        self.app.add_handler(CommandHandler("webapp", self.webapp_test_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {user.first_name}! 👋

DR1111_bot ကိုစမ်းသုံးနေပါသည်!

ဘယ်လိုကူညွှန်ကြားချက်လိုအပ်ပါသလဲး?
        """
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin နဲ့ဆက်သွယ်ရန်", callback_data="contact_admin")
            ],
            [
                InlineKeyboardButton("🧪 Test Popup", callback_data="test_popup"),
                InlineKeyboardButton("🌐 Test WebApp", callback_data="test_webapp")
            ],
            [
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing"),
                InlineKeyboardButton("❓ အကူညွှန်ကြားချက်", callback_data="help_info")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test command to verify bot is working"""
        await update.message.reply_text(
            "✅ DR1111_bot is working perfectly!\n\n"
            "Bot is running locally and responding to commands.\n"
            "Try /start to see the main menu."
        )
    
    async def popup_test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test native popup functionality"""
        if hasattr(update.message, 'reply_text'):
            # Send message first, then show popup
            await update.message.reply_text("🧪 Testing native popup...")
        
        # This will work if the platform supports it
        try:
            await context.bot.answer_callback_query(
                callback_query_id="test",
                text="This is a test popup notification!",
                show_alert=True
            )
        except:
            await update.message.reply_text(
                "🧪 Popup test complete!\n\n"
                "Native popup notifications work differently on different platforms.\n"
                "Try the inline buttons below for popup-style interactions."
            )
    
    async def webapp_test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test WebApp functionality (will need deployment)"""
        webapp_url = "https://core.telegram.org/bots/webapps"
        
        keyboard = [
            [InlineKeyboardButton("🌐 Open Test WebApp", url=webapp_url)]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🧪 Testing WebApp functionality:\n\n"
            "This button will open a test WebApp. For your actual WebApp,\n"
            "you'll need to deploy the HTML files to a server.",
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "explore_plans":
            await self.explore_plans_popup(query)
        elif query.data == "contact_admin":
            await self.contact_admin_popup(query)
        elif query.data == "view_pricing":
            await self.pricing_popup(query)
        elif query.data == "help_info":
            await self.help_popup(query)
        elif query.data == "test_popup":
            await self.test_popup_interaction(query)
        elif query.data == "test_webapp":
            await self.test_webapp_interaction(query)
    
    async def explore_plans_popup(self, query):
        """Show plans in popup style"""
        message_text = """
📋 **Myanmar SME စီးပွားရေးအစီအစဉ်များ**

**ကျွန်ုပ်တို့၏ဝန်ဆောင်မှုများ:**

📊 **စီးပွားရေးခန့်မှန်းချက်များ**
• နေ့စဉ်ရောင်းရငွေခန့်မှန်းချက်
• လ/ပတ်/နှစ်ခန့်မှန်းချက်များ
• အရောင်းအဝယ်အရေအတွက်ခန့်မှန်းချက်

📦 **ကုန်ပစ္စည်းစီမံခန့်ခွဲမှု**
• ကုန်ပစ္စည်းစာရင်း
• စတော့စစ်စစ်စနစ်
• စတော့နည်းပါးသည့်အကြောင်းကြား

📱 **Telegram ထဲမှာပဲအသုံးပြု**
• Browser မသုံးပဲအလုပ်လုပ်
• Mobile အတွက်အဆင်းအသင့်
• အမြန်ဆုံးအသုံးပြုနိုင်

🔒 **လုံခြုံရေး**
• Access Code စနစ်
• ဒေတာလုံခြုံရေး
• Subscription စီမံခန့်ခွဲမှု

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing"),
                InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="contact_admin")
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
    
    async def contact_admin_popup(self, query):
        """Show contact info"""
        message_text = """
📞 **Admin နဲ့ဆက်သွယ်ရန်**

**ဆက်သွယ်နိုင်သောနည်းလမ်းများ:**

📱 **ဖုန်းနံပါတ်:** +959 123 456 789
📧 **အီးမေးလ်:** info@myanmarsme.com
⏰ **ဆက်သွယ်နိုင်သောအချိန်:** 9:00 AM - 6:00 PM

**ဆက်သွယ်ရန်အကြောင်းကြားချက်:**
• Access Code တောင်းဆိုရန်
• စနစ်အသုံးပြုရန်
• အကူညွှန်ကြားချက်ရယူရန်

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing")
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
    
    async def pricing_popup(self, query):
        """Show pricing information"""
        message_text = """
💰 **စျေးနှုန်းနှိုင်းများ**

**📅 1 လအတွက် - 15,000 Ks**
• ကုန်ပစ္စည်း 50 ခုအထိ
• နေ့စဉ်အရောင်းအဝယ် 100 ခုအထိ
• အခြေခံခန့်မှန်းချက်များ

**📅 3 လအတွက် - 40,000 Ks**
• ကုန်ပစ္စည်း 200 ခုအထိ
• နေ့စဉ်အရောင်းအဝယ် 500 ခုအထိ
• အဆင့်မြင့်ခန့်မှန်းချက်များ

**📅 1 နှစ်အတွက် - 150,000 Ks**
• ကုန်ပစ္စည်း ကန့်သတ်မရှိ
• နေ့စဉ်အရောင်းအဝယ် ကန့်သတ်မရှိ
• အပြည့်အစုံခန့်မှန်းချက်များ

**အကျိုးခံစားခွင့်များ:**
✅ 7 ရက်အခမဲ့ Trial
✅ 24/7 အထောက်အပံ့
✅ ဒေတာလုံခြုံရေး
✅ Telegram ထဲမှာပဲအသုံးပြုနိုင်

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="contact_admin")
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
    
    async def help_popup(self, query):
        """Show help information"""
        message_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/test - ဘောက်စ်စမ်းသုံးရန်
/popup - Popup စမ်းသုံးရန်
/webapp - WebApp စမ်းသုံးရန်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်
🧪 စမ်းသုံးလုပ်ငန်းများ

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing")
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
    
    async def test_popup_interaction(self, query):
        """Test popup-style interaction"""
        message_text = """
🧪 **Popup Test Results**

**✅ DR1111_bot ကိုစမ်းသုံးနေပါသည်!**

**စမ်းသုံးရလွယ်ပါသောအရာများ:**
✅ Bot commands အလုပ်နေပါသည်
✅ Inline keyboard အလုပ်နေပါသည်
✅ Message updates အလုပ်နေပါသည်
✅ Myanmar language ပါဝင်ပါသည်

**WebApp အတွက်:**
❌ Deployment လိုအပ်ပါသည်
❌ HTTPS server လိုအပ်ပါသည်

**အခုနေတာ့စမ်းသုံးနိုင်တာများ:**
📱 Inline keyboard navigation
💬 Rich text messages
🔄 Interactive buttons
📊 Information display

အောက်တွင်ရှိတဲ့ခလုတ်များကိုနှိပ်ပြီးဆက်စမ်းသုံးနိုင်ပါသည်။
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing")
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
    
    async def test_webapp_interaction(self, query):
        """Test WebApp interaction (will need deployment)"""
        message_text = """
🌐 **WebApp Test**

**DR1111_bot မှ WebApp စမ်းသုံးချက်:**

**WebApp စမ်းသုံးရန်အတွက်လိုအပ်တာများ:**
❌ HTTPS server လိုအပ်ပါသည်
❌ Domain name လိုအပ်ပါသည်
❌ SSL certificate လိုအပ်ပါသည်

**လောလောဆယ်စမ်းသုံးရန်:**
1. Local server စတင်ပါ
2. ngrok သုံးပြီး HTTPS tunnel ဖန်တီးပါ
3. WebApp URL ကို bot မှာထည့်ပါ

**အခုစမ်းသုံးနိုင်တာများ:**
✅ Bot commands
✅ Inline keyboards
✅ Message interactions
✅ Navigation flow

WebApp စမ်းသုံးချင်း deployment လိုအပ်ပါသည်။
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing")
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
    
    def run(self):
        """Start the bot"""
        print("🤖 DR1111_bot is starting...")
        print("📱 Bot is running locally!")
        print("🧪 Testing mode enabled")
        print("✅ Send /start to @DR1111_bot in Telegram")
        
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    bot = MyanmarSMETestBot()
    bot.run()

if __name__ == '__main__':
    main()
