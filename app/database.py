import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

def conn_database():
    while True:
        try:
            conn = psycopg2.connect(host=settings.database_hostname, database = settings.database_name, user= settings.database_username, password=settings.database_password, cursor_factory = RealDictCursor)
            cursor = conn.cursor()
            print("Database connection is successful!")
            break
        except Exception as error:
            print("Connection to Database failed!")
            print(f"The error was: {error}")
            time.sleep(3)
    return cursor, conn