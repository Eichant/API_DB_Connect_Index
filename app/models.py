from app.extensions import get_db_connection  # Функція для підключення до БД

class ItemModel:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        """Метод для повернення зручного представлення об'єкта"""
        return f"Item(name={self.name}, price={self.price}, description={self.description})"

    def json(self):
        """Метод для повернення JSON-подібної відповіді"""
        return {'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        """Знайти елемент за назвою"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE name = %s", (name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return cls(*result)  # Створення об'єкта на основі отриманих даних
        return None

    @classmethod
    def find_by_id(cls, item_id):
        """Знайти елемент за ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return cls(*result)  # Створення об'єкта на основі отриманих даних
        return None

    def save_to_db(self):
        """Зберегти елемент до бази даних"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description, price) VALUES (%s, %s, %s) RETURNING id",
            (self.name, self.description, self.price)
        )
        self.id = cursor.fetchone()[0]  # Отримуємо ID вставленого елемента
        conn.commit()
        cursor.close()
        conn.close()

    def delete_from_db(self):
        """Видалити елемент з бази даних"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (self.id,))
        conn.commit()
        cursor.close()
        conn.close()
