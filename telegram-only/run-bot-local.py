#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot Runner with Local WebApp Support
Shows Public View as Telegram Mini App from local server
"""

import urllib.request
import json
import time

# Your bot token
BOT_TOKEN = "8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU"

# Local WebApp URL (change to your local server)
WEBAPP_URL = "http://localhost:8080/public-view.html"

def get_updates(offset=None):
    """Get updates from Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        if offset:
            url += f"?offset={offset}"
        
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
        return {"ok": False, "result": []}

def send_message(chat_id, text, reply_markup=None):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        # Prepare data
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        # Convert to JSON
        json_data = json.dumps(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Send request
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        if result.get('ok'):
            print(f"✅ Message sent to chat {chat_id}")
            return True
        else:
            print(f"❌ Error sending message: {result.get('description')}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def create_start_keyboard():
    """Create inline keyboard with WebApp button"""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်", "web_app": {"url": WEBAPP_URL}},
                {"text": "📞 Admin နဲ့ဆက်သွယ်ရန်", "callback_data": "contact_admin"}
            ],
            [
                {"text": "💰 စျေးနှုန်းနှိုင်းများ", "callback_data": "view_pricing"},
                {"text": "❓ အကူညွှန်ကြားချက်", "callback_data": "help_info"}
            ]
        ]
    }
    return json.dumps(keyboard)

def create_explore_keyboard():
    """Create keyboard for explore plans with WebApp"""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🌐 Public View ဖွင့်ရန်", "web_app": {"url": WEBAPP_URL}},
                {"text": "💰 စျေးနှုန်းနှိုင်းများ", "callback_data": "view_pricing"}
            ],
            [
                {"text": "📞 Admin ဆက်သွယ်ရန်", "callback_data": "contact_admin"},
                {"text": "🔙 ပင်မမီနူးသို့", "callback_data": "back_to_main"}
            ]
        ]
    }
    return json.dumps(keyboard)

def create_simple_keyboard():
    """Create simple keyboard without WebApp"""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📋 စီးပွားရေးအစီအစဉ်များ", "callback_data": "explore_plans"},
                {"text": "📞 Admin နဲ့ဆက်သွယ်ရန်", "callback_data": "contact_admin"}
            ],
            [
                {"text": "💰 စျေးနှုန်းနှိုင်းများ", "callback_data": "view_pricing"},
                {"text": "❓ အကူညွှန်ကြားချက်", "callback_data": "help_info"}
            ]
        ]
    }
    return json.dumps(keyboard)

def handle_message(update):
    """Handle incoming message"""
    message = update.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")
    user = message.get("from", {})
    first_name = user.get("first_name", "User")
    
    print(f"📨 Received message from {first_name}: {text}")
    
    if text == "/start":
        welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {first_name}! 👋

DR1111_bot ကိုစမ်းသုံးနေပါသည်!

Bot ကိုတိုက်ရိုက်နေပါပြီ ✅

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်

**WebApp Features:**
🌐 Public View ကို Telegram Mini App အဖြစ်ကြည့်ရန်
📱 Mobile-optimized interface
🎨 Rich UI with forms and interactions

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, welcome_text, create_start_keyboard())
    
    elif text == "/help":
        help_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်

**WebApp Features:**
🌐 Public View ကို Mini App အဖြစ်ကြည့်ရန်
📱 Mobile-optimized interface
🎨 Rich UI with forms and interactions

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, help_text, create_start_keyboard())
    
    elif text == "/test":
        test_text = f"""
✅ **DR1111_bot Test Results**

🤖 **Bot Status:** Working Perfectly!
📱 **Commands:** Working ✅
🎨 **Myanmar Text:** Working ✅
🔗 **Connection:** Connected ✅
📊 **Message Handling:** Working ✅
🌐 **WebApp Support:** Ready ✅

**WebApp URL:** {WEBAPP_URL}

Bot is running locally and responding to all commands!

**WebApp Features:**
🌐 Public View ကို Mini App အဖြစ်ကြည့်ရန်
📱 Mobile-optimized interface
🎨 Rich UI with forms
🔗 Direct integration

**Try these commands:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်
        """
        
        send_message(chat_id, test_text, create_start_keyboard())
    
    else:
        # Handle unknown commands
        help_text = f"""
🤖 Unknown command: {text}

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်

အခုပဲ /start လိုက်ကြည့်ပါ။
        """
        
        send_message(chat_id, help_text, create_start_keyboard())

def handle_callback_query(update):
    """Handle callback query from inline keyboards"""
    callback_query = update.get("callback_query", {})
    callback_data = callback_query.get("data", "")
    message = callback_query.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    
    print(f"🔘 Button clicked: {callback_data}")
    
    if callback_data == "explore_plans":
        explore_text = f"""
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

📱 **Telegram Mini App**
• Public View ကို Mini App အဖြစ်ကြည့်ရန်
• Mobile-optimized interface
• Rich UI with forms
• Direct Telegram integration

**WebApp URL:** {WEBAPP_URL}

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, explore_text, create_explore_keyboard())
    
    elif callback_data == "contact_admin":
        contact_text = """
📞 **Admin နဲ့ဆက်သွယ်ရန်**

**ဆက်သွယ်နိုင်းသောနည်းလမ်းများ:**

📱 **ဖုန်းနံပါတ်:** +959 123 456 789
📧 **အီးမေးလ်:** info@myanmarsme.com
⏰ **ဆက်သွယ်နိုင်းသောအချိန်:** 9:00 AM - 6:00 PM

**ဆက်သွယ်ရန်အကြောင်းကြားချက်:**
• Access Code တောင်းဆိုရန်
• စနစ်အသုံးပြုရန်
• အကူညွှန်ကြားချက်ရယူရန်

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, contact_text, create_simple_keyboard())
    
    elif callback_data == "view_pricing":
        pricing_text = """
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
✅ Telegram Mini App အသုံးပြုနိုင်

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, pricing_text, create_simple_keyboard())
    
    elif callback_data == "help_info":
        help_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်

**လုပ်ငန်းစဉ်များ:**
📋 စီးပွားရေးအစီအစဉ်များကြည့်ရန်
💰 စျေးနှုန်းနှိုင်းများကြည့်ရန်
📞 Admin ဆက်သွယ်ရန်

**WebApp Features:**
🌐 Public View ကို Mini App အဖြစ်ကြည့်ရန်
📱 Mobile-optimized interface
🎨 Rich UI with forms and interactions

**WebApp URL:** {WEBAPP_URL}

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, help_text, create_simple_keyboard())
    
    elif callback_data == "back_to_main":
        welcome_text = """
🏪 **Myanmar SME Business Management**

ပင်မမီနူးသို့ပြန်လာပါသည်။

ဘယ်လိုကူညွှန်ကြားချက်လိုအပ်ပါသလဲး?
        """
        
        send_message(chat_id, welcome_text, create_start_keyboard())

def answer_callback_query(callback_query_id):
    """Answer callback query to remove loading state"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {"callback_query_id": callback_query_id}
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"❌ Error answering callback query: {e}")

def run_bot():
    """Main bot loop"""
    print("🤖 DR1111_bot with Local WebApp Support is starting...")
    print("📱 Bot is running locally!")
    print("🌐 Local WebApp support enabled")
    print(f"🔗 WebApp URL: {WEBAPP_URL}")
    print("✅ Send /start to @DR1111_bot in Telegram")
    print("🔗 Bot Token: 8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU")
    print("🚀 Bot is ready and waiting for messages!")
    print("=" * 50)
    print("📱 OPEN TELEGRAM NOW AND SEND /start TO @DR1111_bot")
    print("📱 OPEN TELEGRAM NOW AND SEND /start TO @DR1111_bot")
    print("📱 OPEN TELEGRAM NOW AND SEND /start TO @DR1111_bot")
    print("=" * 50)
    
    offset = None
    
    try:
        while True:
            # Get updates
            updates = get_updates(offset)
            
            if updates.get("ok"):
                results = updates.get("result", [])
                
                for update in results:
                    # Handle messages
                    if "message" in update:
                        handle_message(update)
                    
                    # Handle callback queries
                    elif "callback_query" in update:
                        callback_query = update["callback_query"]
                        callback_data = callback_query.get("data", "")
                        callback_query_id = callback_query.get("id")
                        
                        # Answer the callback query
                        answer_callback_query(callback_query_id)
                        
                        # Handle the callback
                        handle_callback_query(update)
                    
                    # Update offset
                    offset = update["update_id"] + 1
            
            # Small delay to avoid rate limiting
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    run_bot()
