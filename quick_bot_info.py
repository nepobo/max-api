"""
Быстрое получение информации о боте - однострочная команда
"""

from max_api import MAXClient
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('MAX_BOT_TOKEN')
if not token:
    print("❌ Токен не найден в .env")
    exit(1)

try:
    bot = MAXClient(token).get_me()
    print(f"\n✅ Бот: {bot['name']}")
    print(f"📝 Username: @{bot['username']}")
    print(f"🆔 ID: {bot['user_id']}")
    print(f"🔗 Ссылка: https://max.ru/{bot['username']}\n")
except Exception as e:
    print(f"❌ Ошибка: {e}")
