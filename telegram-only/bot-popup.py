#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Myanmar SME Telegram Bot with Native Popups
All interactions happen in Telegram popup dialogs
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

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

class MyanmarSMEPopupBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command and callback handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("pricing", self.pricing_command))
        self.app.add_handler(CommandHandler("contact", self.contact_command))
        self.app.add_handler(CommandHandler("register", self.register_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with popup"""
        user = update.effective_user
        
        # Create welcome message with inline keyboard
        welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {user.first_name}! 👋

Myanmar SME စီးပွားရေးစီမံခန့်ခွဲမှုစနစ်သို့ကြိုဆိုပါသည်!

ဘယ်လိုကူညွှန်ကြားချက်လိုအပ်ပါသလဲး?
        """
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်", callback_data="explore_plans"),
                InlineKeyboardButton("📞 Admin နဲ့ဆက်သွယ်ရန်", callback_data="contact_admin")
            ],
            [
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing"),
                InlineKeyboardButton("🔰 Trial စမ်းသုံးရန်", callback_data="start_trial")
            ],
            [
                InlineKeyboardButton("📝 စာရင်းသွင်းရန်", callback_data="register"),
                InlineKeyboardButton("❓ အကူညွှန်ကြားချက်", callback_data="help_info")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def pricing_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show pricing in popup"""
        await self.show_pricing_popup(update)
    
    async def contact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show contact info in popup"""
        await self.show_contact_popup(update)
    
    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start registration process"""
        await self.start_registration(update)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "explore_plans":
            await self.explore_plans_popup(query)
        elif query.data == "contact_admin":
            await self.contact_admin_popup(query)
        elif query.data == "view_pricing":
            await self.show_pricing_popup(query)
        elif query.data == "start_trial":
            await self.start_trial_popup(query)
        elif query.data == "register":
            await self.start_registration(query)
        elif query.data == "help_info":
            await self.help_info_popup(query)
        elif query.data == "request_basic":
            await self.request_plan_popup(query, "basic")
        elif query.data == "request_premium":
            await self.request_plan_popup(query, "premium")
        elif query.data == "request_enterprise":
            await self.request_plan_popup(query, "enterprise")
        elif query.data == "call_admin":
            await self.call_admin_popup(query)
        elif query.data == "email_admin":
            await self.email_admin_popup(query)
    
    async def explore_plans_popup(self, query):
        """Show plans overview in popup"""
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

အောက်တွင်ရှိတဲ့ခလုတ်များကိုနှိပ်ပြီးဆက်လက်လုပ်ဆောင်နိုင်ပါသည်။
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing"),
                InlineKeyboardButton("📝 စာရင်းသွင်းရန်", callback_data="register")
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
    
    async def show_pricing_popup(self, update_or_query):
        """Show pricing in popup"""
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
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔰 7 ရက် Trial စမ်းသုံးရန်", callback_data="start_trial"),
                InlineKeyboardButton("📝 စာရင်းသွင်းရန်", callback_data="register")
            ],
            [
                InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="contact_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if hasattr(update_or_query, 'edit_message_text'):
            # It's a callback query
            await update_or_query.edit_message_text(
                message_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            # It's a command
            await update_or_query.message.reply_text(
                message_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def contact_admin_popup(self, query):
        """Show contact info in popup"""
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
• ပြဿနာများဖြေရှင်းရန်

အောက်တွင်ရှိတဲ့ခလုတ်များကိုနှိပ်ပြီးဆက်သွယ်နိုင်ပါသည်။
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📞 ဖုန်းခေါ်ဆိုရန်", callback_data="call_admin"),
                InlineKeyboardButton("📧 အီးမေးလ်ပို့ရန်", callback_data="email_admin")
            ],
            [
                InlineKeyboardButton("📝 စာရင်းသွင်းရန်", callback_data="register"),
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def start_trial_popup(self, query):
        """Start trial process in popup"""
        message_text = """
🔰 **7 ရက်အခမဲ့ Trial**

**Trial အကျိုးခံစားခွင့်များ:**
✅ အခြေခံအင်္ဂါရပ်များအားလုံး
✅ ကုန်ပစ္စည်း 10 ခုအထိ
✅ နေ့စဉ်အရောင်းအဝယ် 20 ခုအထိ
✅ အခမဲ့စမ်းသုံးခ

**Trial စတင်ရန်အဆင့်များ:**
1️⃣ သင့်အမည်နဲ့ဆက်သွယ်ရန်
2️⃣ ဖုန်းနံပါတ်ပေးရန်
3️⃣ အီးမေးလ်ပေးရန်
4️⃣ Trial Code ရယူရန်

အောက်တွင်ရှိတဲ့ "Trial စတင်ရန်" ကိုနှိပ်ပြီးစတင်လို့ရပါသည်။
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🚀 Trial စတင်ရန်", callback_data="register"),
                InlineKeyboardButton("💰 စားသုံးခလုတ်ပေးရန်", callback_data="view_pricing")
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
    
    async def start_registration(self, update_or_query):
        """Start registration process"""
        message_text = """
📝 **စာရင်းသွင်းရန်**

**စာရင်းသွင်းရန်အတွက်လိုအပ်တဲ့အချက်အလက်များ:**

👤 **အခြေခံအချက်အလက်များ:**
• အမည်
• ဖုန်းနံပါတ်
• အီးမေးလ်

🏪 **စီးပွားရေးအချက်အလက်များ:**
• ဆိုင်/ဆိုင်းအမည်
• လိုအပ်တဲ့စီးပွားရေးအစီအစဉ်
• စတင်လိုသောစားသုံးခလုတ်

**စာရင်းသွင်းပြီးပါက:**
✅ Access Code ရယူနိုင်ပါသည်
✅ 7 ရက် Trial စမ်းသုံးနိုင်ပါသည်
✅ Dashboard အသုံးပြုနိုင်ပါသည်

**ဆက်လုပ်ရန်:**
Admin ကိုဆက်သွယ်ပြီးစာရင်းသွင်းပါ
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="call_admin"),
                InlineKeyboardButton("📧 အီးမေးလ်ပို့ရန်", callback_data="email_admin")
            ],
            [
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if hasattr(update_or_query, 'edit_message_text'):
            await update_or_query.edit_message_text(
                message_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update_or_query.message.reply_text(
                message_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    async def help_info_popup(self, query):
        """Show help information in popup"""
        message_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/pricing - စျေးနှုန်းနှိုင်းများ
/contact - ဆက်သွယ်ရန်
/register - စာရင်းသွင်းရန်
/help - အကူညွှန်ကြားချက်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်
📝 စာရင်းသွင်းရန်
🔰 Trial စမ်းသုံးရန်

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

**အချိန်နာရီ:**
တနင်္လာ-သောကြာ: 9:00 AM - 6:00 PM
စနေ: 9:00 AM - 1:00 PM
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📋 စီးပွားရေးအစီအစဉ်များ", callback_data="explore_plans"),
                InlineKeyboardButton("💰 စျေးနှုန်းနှိုင်းများ", callback_data="view_pricing")
            ],
            [
                InlineKeyboardButton("📝 စာရင်းသွင်းရန်", callback_data="register")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def request_plan_popup(self, query, plan_type):
        """Handle plan request in popup"""
        plan_info = {
            "basic": {"name": "အခြေခံ", "price": "15,000 Ks", "duration": "1 လ"},
            "premium": {"name": "အဆင့်မြင့်", "price": "40,000 Ks", "duration": "3 လ"},
            "enterprise": {"name": "အပြည့်အစုံ", "price": "150,000 Ks", "duration": "1 နှစ်"}
        }
        
        plan = plan_info[plan_type]
        
        message_text = f"""
📋 **{plan['name']} စားသုံးခလုတ်**

**စားသုံးခလုတ်အသေးစိတ်:**
💰 စျေးနှုန်း: {plan['price']}
⏰ ကာလ: {plan['duration']}

**စာရင်းသွင်းရန်အဆင့်များ:**
1️⃣ သင့်အချက်အလက်များပေးပါ
2️⃣ Admin ကိုဆက်သွယ်ပါ
3️⃣ စားသုံးခလုတ်ပေးပါ
4️⃣ Access Code ရယူပါ

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="call_admin"),
                InlineKeyboardButton("📧 အီးမေးလ်ပို့ရန်", callback_data="email_admin")
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
    
    async def call_admin_popup(self, query):
        """Show call admin popup"""
        message_text = """
📞 **Admin ဖုန်းခေါ်ဆိုရန်**

**ဆက်သွယ်ရန်ဖုန်းနံပါတ်:**
+959 123 456 789

**ဆက်သွယ်နိုင်သောအချိန်:**
• တနင်္လာ - သောကြာ: 9:00 AM - 6:00 PM
• စနေ: 9:00 AM - 1:00 PM

**ဆက်သွယ်ရန်အကြောင်းကြားချက်:**
• "Myanmar SME Bot မှဖုန်းခေါ်ပါသည်"
• "Access Code တောင်းဆိုလိုပါသည်"
• "စားသုံးခလုတ်ပေးလိုပါသည်"
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📝 စာရင်းသွင်းရန်", callback_data="register"),
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def email_admin_popup(self, query):
        """Show email admin popup"""
        message_text = """
📧 **Admin အီးမေးလ်ပို့ရန်**

**အီးမေးလ်လိပ်စာ:**
info@myanmarsme.com

**အီးမေးလ်ပို့ရန်အကြောင်းကြားချက်:**
• အကြောင်းကြားချက်: Myanmar SME Bot မှဆက်သွယ်ပါသည်
• သင့်ဖုန်းနံပါတ်
• လိုအပ်တဲ့ဝန်ဆောင်မှု
• Access Code တောင်းဆိုချက်

**ဥပမာအီးမေးလ်:**
အကြောင်းကြားချက်: Myanmar SME Bot မှဆက်သွယ်ပါသည်
ဖုန်း: +959 123 456 789
လိုအပ်ချက်: Basic Plan အတွက် Access Code တောင်းဆိုလိုပါသည်
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📞 ဖုန်းခေါ်ဆိုရန်", callback_data="call_admin"),
                InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await self.help_info_popup(update)
    
    def run(self):
        """Start the bot"""
        print("🤖 Myanmar SME Telegram Popup Bot is starting...")
        print("📱 All interactions happen in Telegram popups!")
        
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    bot = MyanmarSMEPopupBot()
    bot.run()

if __name__ == '__main__':
    main()
