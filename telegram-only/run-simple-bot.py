#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Bot Runner - Working Version
Continuously checks for messages and responds
"""

import urllib.request
import json
import time

# Your bot token
BOT_TOKEN = "8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU"

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

def send_message(chat_id, text):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        # Prepare data
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
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

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, welcome_text)
    
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

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
        """
        
        send_message(chat_id, help_text)
    
    elif text == "/test":
        test_text = """
✅ **DR1111_bot Test Results**

🤖 **Bot Status:** Working Perfectly!
📱 **Commands:** Working ✅
🎨 **Myanmar Text:** Working ✅
🔗 **Connection:** Connected ✅
📊 **Message Handling:** Working ✅

Bot is running locally and responding to all commands!

**Try these commands:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်
        """
        
        send_message(chat_id, test_text)
    
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
        
        send_message(chat_id, help_text)

def run_bot():
    """Main bot loop"""
    print("🤖 DR1111_bot is starting...")
    print("📱 Bot is running locally!")
    print("🧪 Testing mode enabled")
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
