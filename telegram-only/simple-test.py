#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Telegram Bot Test
Test your bot connection without complex features
"""

import requests
import json

# Your bot token
BOT_TOKEN = "8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU"

def test_bot_connection():
    """Test if bot token is valid"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        data = response.json()
        
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

def send_test_message():
    """Send a test message to verify bot works"""
    # You need to get your chat ID first
    # This is just a template - you need to replace YOUR_CHAT_ID
    
    # To get your chat ID, send /start to your bot and check the webhook
    # Or use: https://api.telegram.org/bot<TOKEN>/getUpdates
    
    print("\n📱 To test sending messages:")
    print("1. Send /start to @DR1111_bot in Telegram")
    print("2. Then run this script again to see updates")
    print("3. Or check: https://api.telegram.org/bot8776084655:AAEXMldu8z-BSigoltwStm0UBIUEq9uanLU/getUpdates")

def get_bot_info():
    """Get detailed bot information"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print("\n🤖 Detailed Bot Information:")
            print(f"📛 Name: {bot_info['first_name']}")
            print(f"🆔 Username: @{bot_info['username']}")
            print(f"🆔 ID: {bot_info['id']}")
            print(f"🤖 Can receive messages: {bot_info['can_read_all_group_messages']}")
            print(f"🤖 Supports inline queries: {bot_info['supports_inline_queries']}")
            print(f"🤖 Can join groups: {bot_info['can_join_groups']}")
            return bot_info
        else:
            print(f"❌ Error getting bot info: {data.get('description')}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_webhook():
    """Check webhook status"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('ok'):
            webhook_info = data['result']
            print("\n🔗 Webhook Information:")
            print(f"🔗 URL: {webhook_info['url'] or 'Not set'}")
            print(f"📝 Has custom certificate: {webhook_info['has_custom_certificate']}")
            print(f"👥 Pending update count: {webhook_info['pending_update_count']}")
            print(f"📅 Last error date: {webhook_info.get('last_error_date', 'None')}")
            return webhook_info
        else:
            print(f"❌ Error getting webhook info: {data.get('description')}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 DR1111_bot Connection Test")
    print("=" * 50)
    
    # Test 1: Basic connection
    if test_bot_connection():
        print("\n✅ Bot is connected and working!")
        
        # Test 2: Get detailed info
        get_bot_info()
        
        # Test 3: Check webhook
        check_webhook()
        
        # Test 4: Instructions for testing
        send_test_message()
        
        print("\n🎉 Bot is ready for testing!")
        print("\n📱 Next Steps:")
        print("1. Open Telegram")
        print("2. Search for @DR1111_bot")
        print("3. Send /start")
        print("4. Try the commands and buttons")
        
        print("\n🔧 For full testing, you can:")
        print("- Run the full bot script (when Python issues are resolved)")
        print("- Use Telegram Bot API directly")
        print("- Test with Telegram BotFather commands")
        
    else:
        print("\n❌ Bot connection failed!")
        print("Please check:")
        print("1. Bot token is correct")
        print("2. Internet connection is working")
        print("3. Bot is not blocked by Telegram")

if __name__ == '__main__':
    main()
