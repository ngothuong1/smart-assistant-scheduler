from app.dao import mysql_connection
from datetime import datetime
import pytz, json

#lay ra nguoi dung dua vao id cua nguoi dung
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s LIMIT 1"
    user_id = (str(user_id),)
    result = mysql_connection.fetch_query(query, user_id)
    if result:
        (user_id, full_name, avatar, email) = result[0]
        return result[0]
    else:
        return None
# lay ra google token cua nguoi dung dua vao user_id
def get_users_token(user_id):
    query = "SELECT google_token FROM users_token WHERE user_id = %s LIMIT 1"
    user_token_id = (user_id,)
    result = mysql_connection.fetch_query(query, user_token_id)
    if result:
        return result[0][0]
    else:
        return None

#tao mot user moi sau khi nguoi dung xac thuc
def create_new_users(id, name, avatar, email):
    query = "INSERT INTO users (id, full_name, avatar, email) VALUES (%s, %s, %s, %s)"
    new_user = (id, name, avatar, email)
    mysql_connection.execute_query(query, new_user)

#lay tao moi mot google token
def create_new_users_token(user_id, google_json):
    query = "INSERT INTO users_token (user_id, google_token) VALUES (%s, %s)"
    query_data = (user_id, google_json)
    mysql_connection.execute_query(query, query_data)

#cap nhat google token
def update_users_google_token(user_id, creds_json):
    query = "UPDATE users_token SET google_token = %s WHERE user_id = %s"
    query_data = (creds_json, user_id)
    mysql_connection.execute_query(query, query_data)

def update_history_id_for_user(user_id, google_history_id):
    query = "UPDATE users_token SET google_history_id = %s WHERE user_id = %s"
    query_data = (google_history_id, user_id)
    mysql_connection.execute_query(query, query_data)

def get_user_by_history_id(history_id):
    query = "SELECT user_id FROM users_token WHERE google_history_id = %s LIMIT 1"
    query_data = (history_id,)
    result = mysql_connection.fetch_query(query, query_data)

#lay ra google token cua nguoi dung da dang nhap
def get_users_google_token(user_id):
    query = "SELECT google_token FROM users_token WHERE user_id = %s LIMIT 1"
    user_token_id = (user_id,)
    result = mysql_connection.fetch_query(query, user_token_id)
    if result:
        return result[0][0]
    else:
        return None