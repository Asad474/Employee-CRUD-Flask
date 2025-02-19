from os import environ
from psycopg2 import connect, OperationalError
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

conn = None

try:
    conn = connect(
        database=environ.get('DB_NAME'),
        user=environ.get('DB_USERNAME'),
        password=environ.get('DB_PASSWORD'),
        host=environ.get('DB_HOST'),
        port=environ.get('DB_PORT'),  # Correct environment variable
    )

    print('Database connected successfully.')

except OperationalError as e:
    # Print the error message and details
    print(f"Database connection failed: {e}")
