#commands
STOP-Bot: pkill -f "python3 bot.py" && python3 bot.py
Run-bot: python3 bot.py

# Installation Helper Bot

Telegram бот для допомоги з встановленням програмного забезпечення.

## Основні можливості

- Вибір операційної системи (Windows/MacOS)
- Покрокова установка програм
- Отримання посилань на завантаження
- Звернення до системного адміністратора
- Система оцінювання роботи бота
- Статистика оцінок для адміністраторів

## Встановлення

1. Клонуйте репозиторій:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Створіть віртуальне середовище та встановіть залежності:
```bash
python3 -m venv .venv
source .venv/bin/activate  # для Linux/MacOS
# або
.venv\Scripts\activate  # для Windows
python3 -m pip install -r requirements.txt
```

3. Налаштуйте змінні оточення:
```bash
cp .env.example .env
```
Відредагуйте файл `.env` і додайте свої значення для:
- TEST_BOT_TOKEN - токен тестового бота
- TEST_BOT_NAME - ім'я тестового бота
- MAIN_BOT_TOKEN - токен основного бота
- MAIN_BOT_NAME - ім'я основного бота
- ACTIVE_BOT - який бот зараз активний (test/main)

4. Запустіть бота:
```bash
python3 bot.py
```

## Команди бота

- `/start` - Почати роботу з ботом
- `/help` - Отримати довідку
- `/stats` - Переглянути статистику оцінок (тільки для адміністраторів)

## Розробка

1. Створіть тестового бота через [@BotFather](https://t.me/BotFather)
2. Використовуйте тестового бота для розробки, встановивши `ACTIVE_BOT=test` в `.env`
3. Після тестування змініть на `ACTIVE_BOT=main` для роботи з основним ботом

## Безпека

- Не комітьте файл `.env` в репозиторій
- Використовуйте `.env.example` як шаблон для налаштування
- Зберігайте токени в безпечному місці

## Налаштування

1. Встановіть необхідні залежності:
```bash
pip install -r requirements.txt
```

2. Налаштуйте токен бота:
   - Отримайте токен у [@BotFather](https://t.me/BotFather)
   - Встановіть змінну середовища:
     ```bash
     export BOT_TOKEN='your_bot_token_here'
     ```
   - Або створіть файл `.env` з вмістом:
     ```
     BOT_TOKEN=your_bot_token_here
     ```

## Запуск бота

```bash
python bot.py
```

## Як модифікувати бота

### 1. Додавання нової програми

- Додайте опис програми в `TEXTS["programs"]`:
```python
"programs": {
    "new_program": "🆕 New Program\n\nОпис нової програми."
}
```

- Додайте URL для завантаження в `DOWNLOAD_URLS`:
```python
"new_program": {
    "windows": "https://download.link/windows",
    "mac": "https://download.link/mac"
}
```

- Додайте кнопку в функції `get_programs_keyboard()`
- За потреби, додайте нову команду в список `COMMANDS`

### 2. Зміна текстів

Всі тексти знаходяться в словнику `TEXTS`. Кожен текст має свій ключ:
- `welcome` - привітальне повідомлення
- `programs_list` - список програм
- `support_text` - текст для звернення до адміністратора
- та інші

### 3. Додавання нових кнопок

Клавіатури створюються в трьох функціях:
- `get_os_keyboard()` - клавіатура вибору ОС
- `get_programs_keyboard()` - клавіатура з програмами
- `get_navigation_keyboard()` - навігаційна клавіатура

### 4. Зміна логіки роботи

Основні обробники команд та кнопок знаходяться в функціях з декоратором `@dp.message`. Кожна функція має детальний опис своєї роботи в коментарях.

## Доступні команди

- `/start` - Запустити бота
- `/help` - Показати доступні команди
- `/chrome` - Інформація про встановлення Google Chrome
- `/anydesk` - Інформація про встановлення AnyDesk
- `/telegram` - Інформація про встановлення Telegram
- `/yaware` - Інформація про встановлення YaWare 