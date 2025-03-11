"""
Модуль з конфігурацією бота.
"""

import os
from dotenv import load_dotenv
from aiogram import types

# Завантаження змінних середовища
load_dotenv()

# Визначення активного бота
ACTIVE_BOT = os.getenv("ACTIVE_BOT", "test")

# Токен бота
if ACTIVE_BOT == "test":
    BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")
    BOT_NAME = os.getenv("TEST_BOT_NAME")
else:
    BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
    BOT_NAME = os.getenv("MAIN_BOT_NAME")

# Опис команд бота
COMMANDS = [
    types.BotCommand(command="start", description="Запустить бота"),
    types.BotCommand(command="help", description="Показать помощь"),
]

# Додаємо команди для програм
PROGRAM_COMMANDS = {
    "chrome": "Google Chrome",
    "anydesk": "AnyDesk",
    "telegram": "Telegram",
    "yaware": "YaWare"
}

for program_id, program_name in PROGRAM_COMMANDS.items():
    COMMANDS.append(
        types.BotCommand(
            command=program_id,
            description=f"Установить {program_name}"
        )
    ) 