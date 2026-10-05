# database.py

import mysql.connector
from mysql.connector import Error
from config import *


def get_connection():
    """
    Create and return a MySQL database connection.
    """

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="WJ28_krhps",
            database="online_exam"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database Connection Error:", e)
        return None


def close_connection(connection):
    """
    Close the database connection safely.
    """

    if connection is not None and connection.is_connected():
        connection.close()