import numpy as np


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt     
from mysql.connector import connect, Error  
from dotenv import load_dotenv
import sys
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
df = df.sort_values(by='date', ascending=False)  # Sort by date in descending order to get the latest dates first

#Convert DataFrame columns to NumPy arrays for analysis
dates   = df['date'].to_numpy()          # date (datetime)
prices  = df['close'].to_numpy()         # closing prices
volumes = df['volume'].to_numpy()        # trading volumes    
print("First 5 dates: ", dates[:5])
print("First 5 closing prices:", prices[:5])      
print("First 5 volumes:", volumes[:5])  
# Calculate daily returns   
df['daily_return'] = df['close'].pct_change()
daily_returns = df['daily_return'].to_numpy()   
print("First 5 daily returns:", daily_returns[:5])