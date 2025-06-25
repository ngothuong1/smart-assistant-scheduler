import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT")

# Connect
def get_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return connection
    except Error as e:
        print(f"Connect failed: {e}")
        return None

# execute
def execute_query(query, data=None):
    connection = get_connection()
    if not connection:
        print("Connect failed")
        return
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Execute failed: {e}")
    finally:
        connection.close()

def execute_query_and_get_last_row_id(query, data=None):
    connection = get_connection()
    if not connection:
        print("Connect failed")
        return None
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        last_id = cursor.lastrowid
        return last_id
    except Error as e:
        print(f"Execute failed: {e}")
        return None
    finally:
        connection.close()

# truy van
def fetch_query(query, data=None):
    connection = get_connection()
    if not connection:
        print("Connect Failed")
        return []
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        return cursor.fetchall()
    except Error as e:
        print(f"Query failed: {e}")
        return []
    finally:
        connection.close()

def fetch_query_to_dic(query, data=None):
    connection = get_connection()
    if not connection:
        print("Connect Failed")
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, data)
        return cursor.fetchall()
    except Error as e:
        print(f"Query failed: {e}")
        return []
    finally:
        connection.close()

# Hàm chạy script SQL khởi tạo bảng
def initialize_database():
    connection = get_connection()
    if not connection:
        print("===> Không thể kết nối database!")
        return
    try:
        cursor = connection.cursor()
        with open("app/dao/calendar_ai.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        for statement in sql_script.split(";"):
            if statement.strip():
                cursor.execute(statement)
        connection.commit()
        print("==> Database đã được khởi tạo thành công!")
    except Error as e:
        print(f"==> Lỗi khi khởi tạo database: {e}")
    finally:
        connection.close()