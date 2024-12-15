from app import create_app  # Імпортуємо функцію create_app
from app.extensions import get_db_connection  # Функція для підключення до бази даних


app = create_app()

# Створюємо підключення до бази даних на старті
with app.app_context():
    pass

if __name__ == '__main__':
    app.run(debug=True)
