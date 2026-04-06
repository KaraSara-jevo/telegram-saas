#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Myanmar SME Bot - Local Testing (v13 Compatible)
Test your bot without deployment
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
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
        self.updater = Updater(BOT_TOKEN)
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command and callback handlers"""
        dispatcher = self.updater.dispatcher
        
        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CommandHandler("test", self.test_command))
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CallbackQueryHandler(self.button_callback))
    
    def start_command(self, update: Update, context: CallbackContext):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {user.first_name}! 👋

DR1111_bot ကိုစမ်းသုံးနေပါသည်!

Bot ကိုတိုက်ရိုက်နေပါပြီ ✅

ဘယ်လိုကူညွှန်ကြားချက်လိုအပ်ပါသလဲး?
        """
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin နဲ့ဆက်သွယ်ရန်", callback_data="contact_admin")
            ],
            [
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing"),
                InlineKeyboardButton("❓ အကူညွှန်ကြားချက်", callback_data="help_info")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    def test_command(self, update: Update, context: CallbackContext):
        """Test command to verify bot is working"""
        update.message.reply_text(
            "✅ DR1111_bot is working perfectly!\n\n"
            "Bot is running locally and responding to commands.\n"
            "✅ Commands are working\n"
            "✅ Inline keyboards are working\n"
            "✅ Myanmar text is working\n"
            "✅ Bot is connected to Telegram"
        )
    
    def help_command(self, update: Update, context: CallbackContext):
        """Help command"""
        help_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/test - ဘောက်စ်စမ်းသုံးရန်
/help - အကူညွှန်ကြားချက်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    def button_callback(self, update: Update, context: CallbackContext):
        """Handle inline button callbacks"""
        query = update.callback_query
        query.answer()
        
        if query.data == "explore_plans":
            self.explore_plans_popup(query)
        elif query.data == "contact_admin":
            self.contact_admin_popup(query)
        elif query.data == "view_pricing":
            self.pricing_popup(query)
        elif query.data == "help_info":
            self.help_popup(query)
    
    def explore_plans_popup(self, query):
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
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    def contact_admin_popup(self, query):
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
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    def pricing_popup(self, query):
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
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    def help_popup(self, query):
        """Show help information"""
        message_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/test - ဘောက်စ်စမ်းသုံးရန်
/help - အကူညွှန်ကြားချက်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
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
        print("🔗 Bot Token: 8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU")
        print("🚀 Bot is ready for testing!")
        
        self.updater.start_polling()
        self.updater.idle()

def main():
    """Main function"""
    bot = MyanmarSMETestBot()
    bot.run()

if __name__ == '__main__':
    main()
