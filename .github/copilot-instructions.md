# GitHub Copilot Instructions for MAX Messenger API Client

## Project Overview
Python library and console application for MAX Messenger API.
- Python 3.8+
- Main module: `max_api/`
- Examples: `examples/`
- Console app: `console_app/`

## ⚠️ Critical MAX API Rules

### 1. Sending Messages
**ALWAYS** use `user_id` as query parameter in URL:
```python
# CORRECT ✅
POST /messages?user_id=12374848
Body: {"text": "Hello"}

# WRONG ❌
POST /messages
Body: {"recipient": {"chat_id": 12374848}, "text": "Hello"}
```

### 2. Getting chat_id from Updates
**ALWAYS** use `sender.user_id` for replies:
```python
# CORRECT ✅
chat_id = message['sender']['user_id']

# WRONG ❌
chat_id = message['recipient']['chat_id']
```

### 3. Long Polling Timeout
Timeout is **NORMAL** behavior, not an error!
```python
# CORRECT ✅
try:
    updates = client.get_updates(timeout=30)
except Exception as e:
    if "timeout" in str(e).lower():
        continue  # Just continue the loop
    else:
        print(f"Real error: {e}")
```

### 4. Authentication
- Token via `Authorization: {token}` header
- **NO** "Bearer" prefix
- Token stored in `.env` as `MAX_BOT_TOKEN`

## MAXClient Methods

```python
from max_api import MAXClient

client = MAXClient(token="your_token")

# Get bot info
bot_info = client.get_me()

# Send message (user_id in query!)
client.send_message(
    chat_id=12374848,           # REQUIRED: recipient's user_id
    text="Hello *world*",       # REQUIRED: message text
    format="markdown",          # Optional: "markdown" or "html"
    attachments=[...]           # Optional: files, images
)

# Get updates (Long Polling)
updates = client.get_updates(timeout=30, marker=last_marker)

# Create webhook (Production)
client.create_subscription(url="https://your-server.com/webhook")
```

## Bot Template

```python
import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from max_api import MAXClient
from dotenv import load_dotenv

load_dotenv()

def main():
    token = os.getenv('MAX_BOT_TOKEN')
    if not token:
        print("Error: token not found")
        return
    
    client = MAXClient(token=token)
    bot_info = client.get_me()
    print(f"Bot '{bot_info['name']}' started!")
    
    last_marker = None
    
    try:
        while True:
            try:
                updates = client.get_updates(timeout=30, marker=last_marker)
            except Exception as e:
                if "timeout" in str(e).lower():
                    continue  # Normal timeout
                print(f"Error: {e}")
                time.sleep(5)
                continue
            
            for update in updates:
                if update.get('update_type') == 'message_created':
                    message = update['message']
                    chat_id = message['sender']['user_id']
                    text = message.get('body', {}).get('text', '')
                    
                    # Your logic here
                    client.send_message(chat_id=chat_id, text="Reply")
                
                if 'marker' in update:
                    last_marker = update['marker']
    
    except KeyboardInterrupt:
        print("\nBot stopped")
    finally:
        client.close()

if __name__ == "__main__":
    main()
```

## Exception Hierarchy

```python
from max_api.exceptions import (
    MAXAPIException,           # Base exception
    AuthenticationError,       # 401 - Invalid token
    BadRequestError,           # 400 - Bad request
    NotFoundError,            # 404 - Not found
    RateLimitError,           # 429 - Rate limit exceeded
    ServiceUnavailableError   # 503 - Service unavailable
)
```

## Common Errors

### ❌ "Unknown recipient"
**Cause**: sending chat_id in body instead of query
**Fix**: use `?user_id={chat_id}` in URL

### ❌ TimeoutError during Long Polling
**Cause**: thinking it's an error
**Fix**: it's normal! Just `continue` in the loop

### ❌ "command not found: python"
**Cause**: venv not activated
**Fix**: `source venv/bin/activate`

## Installation (Linux)

```bash
# ALWAYS use venv on Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Useful Commands

```bash
# Get bot info
python quick_bot_info.py

# Get user's chat_id
python examples/get_chat_id_bot.py

# Run echo bot
python examples/echo_bot.py

# Run bot with commands
python examples/simple_bot.py

# Console app
python -m console_app.main

# Tests
pytest tests/ -v
```

## MAX API Base Info

- **Base URL**: `https://platform-api.max.ru`
- **Rate Limit**: 30 RPS
- **Auth**: Authorization header (no Bearer prefix)
- **Long Polling**: timeout 30 seconds (normal behavior)
- **Production**: use Webhooks instead of Long Polling

## Update Types

- `message_created` - new message
- `message_updated` - message edited
- `message_deleted` - message deleted
- `callback_query` - inline button pressed

## Pre-commit Checklist

- [ ] Token not committed (in `.gitignore`)
- [ ] All examples work
- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Documentation updated
- [ ] Long Polling timeout handled correctly
- [ ] chat_id = sender.user_id (not recipient.chat_id!)
- [ ] user_id in query parameters when sending

## 🎯 Main Rule

**When in doubt - read source code in `max_api/client.py` and examples in `examples/`!**

All fixes documented in `ALL_FIXES.md`.
