import pandas as pd
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os


# Explicitly specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# Load environment variables
load_dotenv(dotenv_path)

# Database connection details
db_config = {
    'host': os.getenv("MYSQL_HOST", "localhost"),
    'port': int(os.getenv("MYSQL_PORT", 3306)),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE", "fraud_detection")
}
# Path to the CSV file
csv_file = 'C:\\Users\\Hp\\github\\Python_Learnings\\Database\\NSEBANK_MAX_1DAY.csv'

def load_csv_to_mysql():
    try:
        # Read the CSV file
        data = pd.read_csv(csv_file)

        # # Convert date columns to the correct format (if needed)
        # data['created_date'] = pd.to_datetime(data['created_date'], format='%d-%m-%Y', errors='coerce')
        # data['closed_date'] = pd.to_datetime(data['closed_date'], format='%d-%m-%Y', errors='coerce')

        # Establish a database connection
        connection = connect(**db_config)
        cursor = connection.cursor()

        # Insert data row by row
        for index, row in data.iterrows():
            try:
                cursor.execute(
                    """
                    INSERT INTO market_data (symbol, date, close, open, high, low, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        'NIFTY_BANK', row['date'], row['close'], row['open'], row['high'], row['low'], row['volume']
                    )       
                )
            except Error as e:
                print(f"Error inserting row {index}: {e}")

        # Commit the transaction
        connection.commit()
        print("Data loaded successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("Loading CSV data into the database...")
    load_csv_to_mysql()
