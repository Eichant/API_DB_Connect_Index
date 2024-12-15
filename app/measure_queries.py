import time
import psycopg2
from app.extensions import get_db_connection
from concurrent.futures import ThreadPoolExecutor
from tabulate import tabulate  # Для виведення таблиці в консоль

def round_time(elapsed_time, unit="seconds"):
    """Функція для округлення часу в залежності від одиниці вимірювання."""
    if unit == "seconds":
        return round(elapsed_time, 2)  # Округлення до 2 знаків після коми
    elif unit == "minutes":
        return round(elapsed_time / 60, 2)  
    return elapsed_time

def measure_query_time(query, params=None):
    """Функція для вимірювання часу виконання запиту."""
    print(f"Executing query: {query}")
    connection = get_db_connection()
    cursor = connection.cursor()

    start_time = time.time()
    cursor.execute(query, params)
    connection.commit()  # Якщо це запис в БД (INSERT, UPDATE, DELETE)
    end_time = time.time()

    elapsed_time = end_time - start_time
    connection.close()

    return round_time(elapsed_time, "seconds")

def select_query():
    """Виміряти час для SELECT запиту."""
    query = "SELECT * FROM public.items LIMIT 1000;"  # Вибірка 1000 елементів
    print("Running SELECT query...")
    return measure_query_time(query)

def insert_query(num_records):
    """Виміряти час для INSERT запиту."""
    # Вставка тільки для двох стовпців: name і price
    query = "INSERT INTO public.items (name, price) VALUES (%s, %s);"
    
    # Параметри для вставки
    params = [("Item", 100) for i in range(num_records)]
    
    connection = get_db_connection()
    cursor = connection.cursor()

    print(f"Running INSERT query for {num_records} records...")
    start_time = time.time()
    
    batch_size = 1000  # Розмір пакету для вставки
    for i in range(0, num_records, batch_size):
        cursor.executemany(query, params[i:i + batch_size])  #масове вставлення
    
    connection.commit()
    end_time = time.time()
    connection.close()

    return round_time(end_time - start_time, "seconds")


def update_query(num_records):
    """Виміряти час для UPDATE запиту (з паралельним виконанням)."""
    query = "UPDATE items SET price = price + 10 WHERE id = %s;"
    ids = tuple(range(1, num_records + 1))
    
    # Розділ IDs на частини
    chunk_size = 10000
    chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]

    print(f"Running UPDATE query for {num_records} records...")
    def update_chunk(chunk):
        """Функція для оновлення однієї частини даних."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (chunk,))
        connection.commit()
        connection.close()

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(update_chunk, chunks)
    end_time = time.time()

    return round_time(end_time - start_time, "seconds")

def delete_query(num_records):
    """Виміряти час для DELETE запиту (з паралельним виконанням)."""
    query = "DELETE FROM items WHERE id = %s;"
    ids = tuple(range(1, num_records + 1))
    
    # Розділ IDs на частини
    chunk_size = 10000
    chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]

    print(f"Running DELETE query for {num_records} records...")
    def delete_chunk(chunk):
        """Функція для видалення однієї частини даних."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (chunk,))
        connection.commit()
        connection.close()

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(delete_chunk, chunks)
    end_time = time.time()

    return round_time(end_time - start_time, "seconds")

if __name__ == "__main__":
    # Створення заголовків для таблиці
    headers = ["Records", "Select Time (No Index)", "Select Time (With Index)", 
               "Insert Time (No Index)", "Insert Time (With Index)", 
               "Update Time", "Delete Time"]
    table_data = []

    # Заміряти час для різних запитів і заповнити таблицю
    for records in [10, 100, 1000, 2000]:
        print(f"\nStarting measurements for {records} records:")
        
        # Вимірювання часу без інденксів
        print("\nMeasuring performance without indexes...")
        select_time_no_index = select_query()
        insert_time_no_index = insert_query(records)
        update_time = update_query(records)
        delete_time = delete_query(records)

        # Додавання індексів
        print("\nCreating indexes...")
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_id ON public.items(id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_name ON public.items(name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_price ON public.items(price);")
        connection.commit()
        connection.close()

        # Вимірювання часу з індексами
        print("\nMeasuring performance with indexes...")
        select_time_with_index = select_query()
        insert_time_with_index = insert_query(records)

        # Додавання результату в таблицю
        table_data.append([
            records,
            select_time_no_index, select_time_with_index,
            insert_time_no_index, insert_time_with_index,
            update_time, delete_time
        ])

    # Виведення таблиці в консоль
    print("\nResults:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
