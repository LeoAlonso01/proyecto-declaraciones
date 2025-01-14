import psycopg2
from psycopg2 import sql

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="052613",
            host="localhost",
            port="5432",
            database="Test"
        )
        cursor = connection.cursor()
        print("Connection to PostgreSQL DB successful")
        return connection, cursor
    except Exception as error:
        print(f"Error connecting to PostgreSQL DB: {error}")
        return None, None

def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("PostgreSQL connection closed")

if __name__ == "__main__":
    conn, cur = connect_to_db()
    if conn and cur:
        # Perform database operations here
        close_connection(conn, cur)