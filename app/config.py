class Config:
    """Клас для зберігання налаштувань конфігурації додатку"""

    # Налаштування для бази даних
    SQLALCHEMY_DATABASE_URI = (
        'postgres://avnadmin:AVNS_qjso-d21rHdvVuFmVz1@pg-1eb05510-istu-e39f.l.aivencloud.com:27525/defaultdb?sslmode=require'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаємо модифікацію трекінгу

    # Налаштування для JWT
    JWT_SECRET_KEY = 'your-secret-key'  # Замість 'your-secret-key' використовуйте ваш секретний ключ
    JWT_ACCESS_TOKEN_EXPIRES = 30  # Термін дії токену - 30 днів

    # Логування
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
