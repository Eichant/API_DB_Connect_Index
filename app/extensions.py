import psycopg2
from flask_jwt_extended import JWTManager

jwt = JWTManager()

# Параметри підключення до бази даних
DB_CONFIG = {
    'host': 'pg-1eb05510-istu-e39f.l.aivencloud.com',
    'port': '27525',
    'database': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_qjso-d21rHdvVuFmVz1'
}

#підключення до бази даних
def get_db_connection():
    connection = psycopg2.connect(
        dbname=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )
    return connection

#функція для виконання запиту
def execute_query(query, params=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)  
            connection.commit()  
            return cursor.fetchall()  
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()  

#виконання SELECT запиту
query = "SELECT * FROM public.items LIMIT 5"
result = execute_query(query)
print(result)
