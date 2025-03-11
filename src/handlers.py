"""
Модуль з обробниками повідомлень бота.
"""

import logging
import os
from aiogram import types, Bot
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, CallbackQuery

from .texts import TEXTS, DOWNLOAD_URLS, ACCOUNT_URLS
from .keyboards import (
    get_os_keyboard,
    get_account_keyboard,
    get_program_install_keyboard,
    get_download_button,
    get_instruction_keyboard,
    get_final_keyboard,
    get_rating_keyboard
)
from .ratings import save_rating, get_stats, is_admin, ADMIN_CHAT_ID

# Словарь для хранения выбора ОС пользователями
user_os = {}
# Словарь для хранения текущего этапа установки
user_step = {}

# Пути к изображениям
WELCOME_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "images", "help_bot.png")
NEW_USER_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "images", "NewUser.png")

# Этапы установки
STEPS = {
    "ACCOUNT": 0,
    "CHROME": 1,
    "TELEGRAM": 2,
    "DONE": 3
}

async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    user_id = message.from_user.id
    # Очищаем данные пользователя при перезапуске
    if user_id in user_os:
        del user_os[user_id]
    if user_id in user_step:
        del user_step[user_id]
        
    try:
        # Создаем объект FSInputFile для локального файла
        image = FSInputFile(WELCOME_IMAGE_PATH)
        # Отправляем изображение с текстом
        await message.answer_photo(
            photo=image,
            caption=TEXTS["welcome"],
            parse_mode="Markdown",
            reply_markup=get_os_keyboard()
        )
    except Exception as e:
        logging.error(f"Error sending welcome image: {e}")
        # Если не удалось отправить изображение, отправляем только текст
        await message.answer(
            text=TEXTS["welcome"],
            parse_mode="Markdown",
            reply_markup=get_os_keyboard()
        )

async def cmd_help(message: types.Message):
    """Обработка команды /help"""
    await cmd_start(message)

async def handle_os_choice(message: types.Message):
    """Обработка выбора ОС"""
    user_id = message.from_user.id
    logging.info(f"Processing OS choice: {message.text}")
    
    if message.text == "🪟 Windows":
        user_os[user_id] = "windows"
        await message.answer(
            text=TEXTS["win_ok"],
            parse_mode="Markdown"
        )
    elif message.text == "🍎 MacOS":
        user_os[user_id] = "mac"
        await message.answer(
            text=TEXTS["mac_ok"],
            parse_mode="Markdown"
        )
    
    try:
        image = FSInputFile(NEW_USER_IMAGE_PATH)
        await message.answer_photo(
            photo=image,
            caption=TEXTS["account_check"],
            parse_mode="Markdown",
            reply_markup=get_account_keyboard(user_os[user_id])
        )
        user_step[user_id] = STEPS["ACCOUNT"]
        logging.info(f"User {user_id} is at step: ACCOUNT")
    except Exception as e:
        logging.error(f"Error sending NewUser image: {str(e)}")
        await message.answer(
            text=TEXTS["account_check"],
            parse_mode="Markdown",
            reply_markup=get_account_keyboard(user_os[user_id])
        )

async def handle_program_info(message: types.Message, program: str):
    """Отправка информации о программе"""
    user_id = message.from_user.id
    if user_id not in user_os:
        await cmd_start(message)
        return

    os_type = user_os[user_id]
    info = TEXTS[f"{program}_install"]
    await message.answer(
        text=info,
        parse_mode="Markdown",
        reply_markup=get_program_install_keyboard(DOWNLOAD_URLS[program][os_type], os_type)
    )
    await message.answer(
        text=f" по ссылке ниже  {program}:",
        reply_markup=get_download_button(DOWNLOAD_URLS[program][os_type])
    )

async def handle_program_button(message: types.Message):
    """Обработка нажатий на кнопки программ"""
    program_map = {
        "Google Chrome": "chrome",
        "Telegram": "telegram"
    }

    if program := program_map.get(message.text):
        await handle_program_info(message, program)

async def handle_navigation(message: types.Message):
    """Обработка навигационных кнопок"""
    if message.text == TEXTS["back"]:
        await cmd_start(message)
    # elif message.text == TEXTS["restart"]:
        await cmd_start(message)
    elif message.text == TEXTS["support"]:
        await message.answer(
            text=TEXTS["support_text"],
            parse_mode="Markdown"
        )

async def handle_account_setup(message: types.Message):
    """Обработка действий с учетной записью"""
    user_id = message.from_user.id
    
    if user_id not in user_os:
        await cmd_start(message)
        return
        
    # if message.text == TEXTS["restart"]:
    #     await cmd_start(message)
    #     return
        
    if message.text == TEXTS["back"]:
        await cmd_start(message)
        return
        
    if message.text == TEXTS["account_ready"]:
        user_step[user_id] = STEPS["CHROME"]
        os_type = user_os[user_id]
        url = DOWNLOAD_URLS["chrome"][os_type]
        
        await message.answer(
            text=TEXTS["chrome_install"],
            parse_mode="Markdown",
            reply_markup=get_program_install_keyboard(url, os_type)
        )
        await message.answer(
            text="⬇️     ⬇️     ⬇️",
            reply_markup=get_download_button(url)
        )
        return
        
    url = None
    if message.text == TEXTS["mac_account"]:
        url = ACCOUNT_URLS["mac"]
        logging.info(f"User {user_id} requested Mac OS account setup")
    elif message.text == TEXTS["win10_account"]:
        url = ACCOUNT_URLS["win10"]
    elif message.text == TEXTS["win11_account"]:
        url = ACCOUNT_URLS["win11"]
        
    if url:
        keyboard = get_instruction_keyboard(url)
        instruction_text = (
            "*📝 Инструкция по созданию учетной записи*\n\n"
            "ℹ️ Моя инструкция содержит все необходимые шаги для создания учетной записи.\n\n"
            "✅ Если все понятно - нажми на кнопку ниже и перейди по ссылке."
        )
        
        await message.answer(
            text=instruction_text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

async def handle_program_install(message: types.Message):
    """Обработка установки программ"""
    user_id = message.from_user.id
    logging.info(f"Handling program install message: {message.text}")
    
    if user_id not in user_os or user_id not in user_step:
        await cmd_start(message)
        return
        
    # if message.text == TEXTS["restart"]:
    #     logging.info("User clicked restart button")
    #     await cmd_start(message)
    #     return
        
    if message.text == TEXTS["back"]:
        logging.info("User clicked back button")
        current_step = user_step[user_id]
        os_type = user_os[user_id]
        logging.info(f"Current step: {current_step}, OS: {os_type}")
        
        if current_step == STEPS["CHROME"]:
            # Возврат к выбору учетной записи
            try:
                image = FSInputFile(NEW_USER_IMAGE_PATH)
                await message.answer_photo(
                    photo=image,
                    caption=TEXTS["account_check"],
                    parse_mode="Markdown",
                    reply_markup=get_account_keyboard(user_os[user_id])
                )
                user_step[user_id] = STEPS["ACCOUNT"]
                logging.info("Returned to account setup")
            except Exception as e:
                logging.error(f"Error sending NewUser image: {str(e)}")
                await message.answer(
                    text=TEXTS["account_check"],
                    parse_mode="Markdown",
                    reply_markup=get_account_keyboard(user_os[user_id])
                )
                
        elif current_step == STEPS["TELEGRAM"]:
            # Возврат к Chrome
            url = DOWNLOAD_URLS["chrome"][os_type]
            user_step[user_id] = STEPS["CHROME"]
            logging.info("Returning to Chrome installation")
            await message.answer(
                text=TEXTS["chrome_install"],
                parse_mode="Markdown",
                reply_markup=get_program_install_keyboard(url, os_type)
            )
            await message.answer(
                text="⬇️     ⬇️     ⬇️",
                reply_markup=get_download_button(url)
            )
        return
        
    if message.text == TEXTS["installed"]:
        current_step = user_step[user_id]
        os_type = user_os[user_id]
        
        if current_step == STEPS["CHROME"]:
            user_step[user_id] = STEPS["TELEGRAM"]
            url = DOWNLOAD_URLS["telegram"][os_type]
            await message.answer(
                text=TEXTS["telegram_install"],
                parse_mode="Markdown",
                reply_markup=get_program_install_keyboard(url, os_type)
            )
            await message.answer(
                text="⬇️     ⬇️     ⬇️",
                reply_markup=get_download_button(url)
            )
            
        elif current_step == STEPS["TELEGRAM"]:
            user_step[user_id] = STEPS["DONE"]
            await message.answer(
                text=TEXTS["all_done"],
                parse_mode="Markdown",
                reply_markup=get_final_keyboard()
            )
            
    elif message.text == TEXTS["support"]:
        await message.answer(
            text=TEXTS["support_text"],
            parse_mode="Markdown"
        )
        
    elif message.text == TEXTS["request_code"]:
        # Отримуємо інформацію про користувача
        user = message.from_user
            
        # Отримуємо username або використовуємо ID якщо username відсутній
        username = f"@{user.username}" if user.username else f"id{user.id}"
            
        # Формуємо повідомлення для адміністраторів
        admin_message = TEXTS["admin_message"].format(
            username=username
        )
        
        try:
            # Надсилаємо повідомлення в чат адміністраторів
            bot = message.bot
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_message
            )
            
            # Повідомляємо користувача про успішну відправку запиту
            await message.answer(
                text=TEXTS["code_requested"],
                parse_mode="Markdown",
                reply_markup=get_rating_keyboard()
            )
            
        except Exception as e:
            logging.error(f"Error sending message to admin chat: {e}")
            await message.answer(
                text="Произошла ошибка при отправке запроса. Пожалуйста, обратитесь в поддержку.",
                parse_mode="Markdown"
            )

async def cmd_stats(message: types.Message):
    """Обработка команды /stats"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer(TEXTS["admin_only"])
        return
        
    likes, dislikes = get_stats()
    await message.answer(
        TEXTS["stats_message"].format(
            likes=likes,
            dislikes=dislikes
        )
    )

async def handle_rating(callback: CallbackQuery):
    """Обработка оценки от пользователя"""
    user_id = callback.from_user.id
    username = f"@{callback.from_user.username}" if callback.from_user.username else f"id{user_id}"
    
    rating = "👍" if callback.data == "rate_good" else "👎"
    
    if save_rating(user_id, rating):
        await callback.message.edit_text(
            TEXTS["rating_thanks"],
            reply_markup=None
        )
    else:
        # Повідомляємо адміністратора про помилку
        bot = callback.bot
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=TEXTS["rating_error"].format(
                username=username,
                error="Не удалось сохранить оценку в файл"
            )
        )
    
    await callback.answer() 