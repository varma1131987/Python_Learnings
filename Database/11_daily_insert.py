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

sql = """
INSERT INTO market_data (symbol, date, close, open, high, low, volume)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    close  = VALUES(close),
    open   = VALUES(open),
    high   = VALUES(high),
    low    = VALUES(low),
    volume = VALUES(volume);
"""

# Replace row['...'] with actual values for manual insertion
data = (
    'NIFTY_BANK',
    '2025-12-19',  # Date
    59069.20,  # Close
    59047.40,  # Open
    59138.60,  # High
    58901.95,  # Low
    179268862  # Volume
)
conn = connect(**db_config)
cursor = conn.cursor()  

cursor.execute(sql, data)
conn.commit()