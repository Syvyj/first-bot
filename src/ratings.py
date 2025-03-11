"""
Модуль для роботи з оцінками бота.
"""

import csv
import os
from datetime import datetime
import logging
from typing import Dict, Tuple

# Шлях до файлу з оцінками
RATINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "ratings.csv")

# ID чату адміністраторів
ADMIN_CHAT_ID = -1002490051402

# Список адміністраторів (замініть на реальні ID)
ADMIN_IDS = [7613724879]

def ensure_ratings_file():
    """Перевіряє наявність файлу з оцінками та створює його при необхідності."""
    os.makedirs(os.path.dirname(RATINGS_FILE), exist_ok=True)
    if not os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'timestamp', 'rating'])

def save_rating(user_id: int, rating: str) -> bool:
    """Зберігає оцінку користувача."""
    try:
        ensure_ratings_file()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(RATINGS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, timestamp, rating])
        return True
    except Exception as e:
        logging.error(f"Error saving rating: {e}")
        return False

def get_stats() -> Tuple[int, int]:
    """Повертає статистику оцінок (кількість лайків і дизлайків)."""
    try:
        ensure_ratings_file()
        likes = dislikes = 0
        
        with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['rating'] == '👍':
                    likes += 1
                elif row['rating'] == '👎':
                    dislikes += 1
                    
        return likes, dislikes
    except Exception as e:
        logging.error(f"Error getting stats: {e}")
        return 0, 0

def is_admin(user_id: int) -> bool:
    """Перевіряє, чи є користувач адміністратором."""
    return user_id in ADMIN_IDS 