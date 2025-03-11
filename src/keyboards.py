"""
Модуль з функціями для створення клавіатур.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .texts import TEXTS
import logging

def get_os_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора ОС"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🪟 Windows"),
        KeyboardButton(text="🍎 MacOS")
    )
    return builder.as_markup(resize_keyboard=True)

def get_account_keyboard(os_type: str) -> ReplyKeyboardMarkup:
    """Клавиатура для создания учетной записи"""
    builder = ReplyKeyboardBuilder()

    if os_type == "windows":
        # Кнопки для Windows
        builder.row(
            KeyboardButton(text=TEXTS["win10_account"]),
            KeyboardButton(text=TEXTS["win11_account"]))
        builder.row(
            KeyboardButton(text=TEXTS["account_ready"])
        )
    else:
        # Кнопка для MacOS
        builder.row(KeyboardButton(text=TEXTS["mac_account"]),
                    KeyboardButton(text=TEXTS["account_ready"])
                    )

    # Кнопка подтверждения для обеих ОС
    builder.row(
        KeyboardButton(text=TEXTS["back"]),
        KeyboardButton(text=TEXTS["support"])
        # ,
        # KeyboardButton(text=TEXTS["restart"])
    )

    return builder.as_markup(resize_keyboard=True)

def get_program_install_keyboard(url: str, os_type: str) -> ReplyKeyboardMarkup:
    """Создает клавиатуру для установки программы"""
    builder = ReplyKeyboardBuilder()
    
    
    # Кнопки "Я установил" и "Поддержка" в одном ряду
    builder.row(KeyboardButton(text=TEXTS["installed"]),
                KeyboardButton(text=TEXTS["support"])
                )
    
    # Кнопки навигации
    logging.info(f"Adding navigation buttons: {TEXTS['back']}, {TEXTS['restart']}")
    builder.row(
        KeyboardButton(text=TEXTS["back"])
        # ,
        # KeyboardButton(text=TEXTS["restart"]) 
    )
    
    keyboard = builder.as_markup(resize_keyboard=True)
    logging.info(f"Created keyboard with buttons: {[btn.text for row in keyboard.keyboard for btn in row]}")
    return keyboard

def get_download_button(url: str) -> InlineKeyboardMarkup:
    """Создает инлайн кнопку для скачивания"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Скачать",
                url=url
            )
        ]]
    )

def get_instruction_keyboard(url: str) -> InlineKeyboardMarkup:
    """Создает инлайн клавиатуру для открытия инструкции"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="📝 Открыть инструкцию ⬅️",
                url=url
            )
        ]]
    )

def get_final_keyboard() -> ReplyKeyboardMarkup:
    """Создает финальную клавиатуру"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=TEXTS["request_code"])
                )
    builder.row(KeyboardButton(text=TEXTS["support"]),
                KeyboardButton(text=TEXTS["back"])
                )
    return builder.as_markup(resize_keyboard=True)

def get_rating_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для оценки работы бота"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="👍", callback_data="rate_good"),
            InlineKeyboardButton(text="👎", callback_data="rate_bad")
        ]]
    ) 