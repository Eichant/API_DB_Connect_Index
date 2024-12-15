from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from app.extensions import get_db_connection

# Blueprint для операцій з елементами
blp = Blueprint('items', __name__, url_prefix='/items', description='Operations on items')


@blp.route('/', methods=['GET', 'POST'])
@jwt_required()
def items():
    if request.method == 'GET':
        """Отримати список усіх елементів"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items;")
        items = cursor.fetchall()
        connection.close()
        return jsonify(items)

    elif request.method == 'POST':
        """Створити новий елемент"""
        new_item = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO items (name, description, price) VALUES (%s, %s, %s) RETURNING id;",
            (new_item['name'], new_item['description'], new_item['price'])
        )
        item_id = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return jsonify({"id": item_id}), 201


@blp.route('/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def item(item_id):
    if request.method == 'GET':
        """Отримати елемент за ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
        item = cursor.fetchone()
        connection.close()

        if not item:
            return jsonify({"message": "Item not found"}), 404
        return jsonify(item)

    elif request.method == 'PUT':
        """Оновити елемент за ID"""
        updated_data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE items SET name = %s, description = %s, price = %s WHERE id = %s;",
            (updated_data['name'], updated_data['description'], updated_data['price'], item_id)
        )
        connection.commit()
        connection.close()
        return jsonify({"message": "Item updated successfully"}), 200

    elif request.method == 'DELETE':
        """Видалити елемент за ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s;", (item_id,))
        connection.commit()
        connection.close()
        return jsonify({"message": "Item deleted successfully"}), 200

