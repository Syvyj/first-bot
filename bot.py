"""
Telegram бот для допомоги з встановленням програмного забезпечення.
Основні можливості:
- Вибір операційної системи (Windows/MacOS)
- Покрокова установка програм
- Отримання посилань на завантаження
- Звернення до системного адміністратора
"""

import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command

from src import (
    BOT_TOKEN, COMMANDS,
    cmd_start, cmd_help, cmd_stats,
    handle_os_choice, handle_account_setup,
    handle_program_install, handle_rating,
    TEXTS
)

# Настройка логирования для отслеживания работы бота
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков команд
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_help, Command("help"))
dp.message.register(cmd_stats, Command("stats"))

# Регистрация обработчиков сообщений
dp.message.register(handle_os_choice, lambda message: message.text in ["🪟 Windows", "🍎 MacOS"])
dp.message.register(handle_account_setup, lambda message: message.text in [
    TEXTS["win10_account"],
    TEXTS["win11_account"],
    TEXTS["mac_account"],
    TEXTS["account_ready"],
    TEXTS["back"],
    TEXTS["restart"]
])
dp.message.register(handle_program_install, lambda message: message.text in [
    "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣",
    TEXTS["installed"],
    TEXTS["support"],
    TEXTS["back"],
    TEXTS["restart"],
    TEXTS["request_code"]
])

# Регистрация обработчика callback-кнопок
dp.callback_query.register(handle_rating, lambda c: c.data.startswith("rate_"))

async def on_startup():
    """Действия при запуске бота"""
    try:
        # Устанавливаем команды бота
        await bot.set_my_commands(COMMANDS)
        # Проверяем, что команды установлены
        bot_commands = await bot.get_my_commands()
        if not bot_commands:
            logger.warning("Commands were not set properly!")
        else:
            logger.info(f"Bot started with {len(bot_commands)} commands")
    except Exception as e:
        logger.error(f"Error setting commands: {e}")

async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("Shutting down...")
    try:
        await bot.session.close()
        logger.info("Bot session closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    finally:
        logger.info("Bye!")

def handle_signals():
    """Обработка сигналов завершения"""
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(sig=s))
        )

async def shutdown(sig: signal.Signals):
    """Graceful shutdown"""
    logger.info(f'Received signal {sig.name}...')
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f'Cancelling {len(tasks)} outstanding tasks')
    await asyncio.gather(*tasks, return_exceptions=True)
    await on_shutdown()
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    """Главная функция"""
    try:
        logger.info("Starting bot...")
        handle_signals()
        await on_startup()
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}")
    finally:
        sys.exit(0) 