"""
Пакет з основними модулями бота.
"""

from .config import BOT_TOKEN, COMMANDS
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
from .handlers import (
    cmd_start,
    cmd_help,
    cmd_stats,
    handle_os_choice,
    handle_account_setup,
    handle_program_install,
    handle_rating
) 