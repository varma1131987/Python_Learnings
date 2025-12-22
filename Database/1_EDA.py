"""Store in MySQL → load into pandas DataFrame → do EDA/plots in pandas → use NumPy arrays only for the inner numeric pieces that need speed"""


import pandas as pd
from mysql.connector import connect, Error  
from dotenv import load_dotenv
import os
# Explicitly specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env') 

# CSV or JSON or txt or other file paths can also be set in .env if needed : Next JSON / CSV / TXT file loading can be done using pd.read_json / pd.read_csv / pd.read_table

# MySQl or Snowflake & Oracle or AWS Databases can be connected similarly using their respective connectors

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
# Example usage
if __name__ == "__main__":  
    query = "SELECT * FROM market_data;"  
    df = fetch_data_to_dataframe(query)
    if df is not None:
        # print(df.tail())   
        print(df.head() )     
        print(df.info())
        print(df['close'].describe())  # Perform descriptive statistics on 'close' column only              
        print(df.isna().sum())    # check missing values
