#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Test Bot - Working Version
Test your bot connection immediately
"""

import urllib.request
import json
import time

# Your bot token
BOT_TOKEN = "8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU"

def test_bot_connection():
    """Test bot connection"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('ok'):
            bot_info = data['result']
            print("✅ Bot Connection Test Results:")
            print(f"🤖 Bot Name: {bot_info['first_name']}")
            print(f"🆔 Bot Username: @{bot_info['username']}")
            print(f"🆔 Bot ID: {bot_info['id']}")
            print(f"✅ Bot is active and ready!")
            return True
        else:
            print("❌ Bot Connection Failed:")
            print(f"Error: {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Network Error: {e}")
        return False

def get_updates():
    """Get updates from Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
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

def main():
    """Main test function"""
    print("🧪 DR1111_bot Test")
    print("=" * 50)
    
    # Test 1: Bot connection
    if test_bot_connection():
        print("\n✅ Bot is connected and working!")
        
        # Test 2: Check for messages
        print("\n📱 Checking for messages...")
        updates = get_updates()
        
        if updates.get('ok'):
            results = updates.get('result', [])
            if results:
                print(f"📨 Found {len(results)} messages/updates:")
                for i, update in enumerate(results):
                    message = update.get('message', {})
                    if message:
                        text = message.get('text', 'No text')
                        user = message.get('from', {})
                        chat = message.get('chat', {})
                        print(f"  {i+1}. From: {user.get('first_name', 'Unknown')} - {text}")
                        print(f"     Chat ID: {chat.get('id')}")
                        
                        # Send a test response
                        if text == '/start':
                            welcome_text = f"""
🏪 **Myanmar SME Business Management**

မင်္ဂလာပါ {user.get('first_name', 'User')}! 👋

DR1111_bot ကိုစမ်းသုံးနေပါသည်!

Bot ကိုတိုက်ရိုက်နေပါပြီ ✅

Try these commands:
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်
                            """
                            send_message(chat.get('id'), welcome_text)
                        
                        elif text == '/help':
                            help_text = """
❓ **အကူညွှန်ကြားချက်**

**အသုံးပြုနိုင်တဲ့အမိန့်များ:**
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်

**ဆက်သွယ်ရန်:**
📞 +959 123 456 789
📧 info@myanmarsme.com

✅ **DR1111_bot မှစမ်းသုံးနေပါသည်!**
                            """
                            send_message(chat.get('id'), help_text)
                        
                        elif text == '/test':
                            test_text = """
✅ **DR1111_bot Test Results**

🤖 **Bot Status:** Working Perfectly!
📱 **Commands:** Working ✅
🎨 **Myanmar Text:** Working ✅
🔗 **Connection:** Connected ✅

Bot is responding to your messages!
                            """
                            send_message(chat.get('id'), test_text)
                        
                        else:
                            # Handle unknown commands
                            help_text = f"""
🤖 Unknown command: {text}

Try these commands:
/start - စတင်ရန်
/help - အကူညွှန်ကြားချက်
/test - ဘောက်စ်စမ်းသုံးရန်
                            """
                            send_message(chat.get('id'), help_text)
            else:
                print("📨 No messages found yet.")
                print("📱 Send a message to @DR1111_bot in Telegram!")
        else:
            print("❌ Error getting updates")
        
        print("\n🎉 Test Complete!")
        print("📱 Send /start to @DR1111_bot in Telegram to test the bot!")
        
    else:
        print("\n❌ Bot connection failed!")
        print("Please check:")
        print("1. Bot token is correct")
        print("2. Internet connection is working")
        print("3. Bot is not blocked by Telegram")

if __name__ == '__main__':
    main()
