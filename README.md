# ------------ Запуск бота --------------- #

1. Установить Python 3.10+ - https://www.python.org/downloads/
2. Установить PostgreSQL - https://www.postgresql.org/download/
3. Установить библиотеки requirements.txt - pip install -r requirements.txt или используйте poetry - poetry install
4. Настройте файл .env
5. Команда запуска - python bot


# ------------ Запуск сайта --------------- #

1. Установить Python 3.10+ - https://www.python.org/downloads/
2. Установить PostgreSQL - https://www.postgresql.org/download/
3. Установить библиотеки requirements.txt - pip install -r requirements.txt или используйте poetry - poetry install
4. Настройте файл .env
5. Команда запуска - python webadmin


# ------------ Запуск через докер --------------- #

1. Установить Docker/docker compose
2. Команда запуска docker compose up -d


# -------------- Настройка ------------- #

1. Откройте файл .env
2. Поле BOT_TOKEN - вставьте токен вашего бота
3. Поля DB_HOST, DB_PASS, DB_NAME, DB_LOG - введите данные от базы данных
4. Настройте время жизни сессии и ключ для декодирования сессий

