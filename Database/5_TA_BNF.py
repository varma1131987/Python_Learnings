import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt     
from mysql.connector import connect, Error  
from dotenv import load_dotenv
import sys
import os
import seaborn as sns
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

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
    'database': os.getenv("MYSQL_DATABASE", "market_data")      
}

def fetch_data_to_dataframe(query):
    try:
        # Establish a database connection
        connection = connect(**db_config)
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get column names from the cursor
        column_names = [i[0] for i in cursor.description]

        # Create a pandas DataFrame from the fetched data
        df = pd.DataFrame(rows, columns=column_names)

        return df

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Fetch data from the database
query = "SELECT * FROM market_data;"    
df = fetch_data_to_dataframe(query)
# Ensure 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date', ascending=False)  # Ensure the DataFrame is sorted by the latest dates first
print(df.head(5))

"""Check the Data Type of the close Column:
Ensure that the close column is of a numeric type. You can check this using:"""

print(df['close'].dtype)

"""Convert the close Column to Numeric:
If the column contains non-numeric values, you can convert it to numeric using pd.to_numeric"""


df = df.sort_values('date').set_index('date')

# RSI (14-day)
rsi = RSIIndicator(close=df['close'], window=14)
df['rsi_14'] = rsi.rsi()
print(df[['close', 'rsi_14']].tail())




# # MACD (12,26,9)
# macd = MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
# df['macd'] = macd.macd()
# df['macd_signal'] = macd.macd_signal()
# df['macd_hist'] = macd.macd_diff()

# # Bollinger Bands (20, 2)
# bb = BollingerBands(close=df['close'], window=20, window_dev=2)
# df['bb_high'] = bb.bollinger_hband()
# df['bb_low'] = bb.bollinger_lband()
# df['bb_width'] = bb.bollinger_wband()