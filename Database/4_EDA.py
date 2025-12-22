import numpy as np


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt     
from mysql.connector import connect, Error  
from dotenv import load_dotenv
import sys
import os
import seaborn as sns

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
print(df.head(5))

"""Check the Data Type of the close Column:
Ensure that the close column is of a numeric type. You can check this using:"""

print(df['close'].dtype)

"""Convert the close Column to Numeric:
If the column contains non-numeric values, you can convert it to numeric using pd.to_numeric"""

# df['close'] = pd.to_numeric(df['close'], errors='coerce')
# print(df['close'].dtype)
# fig1, ax = plt.subplots(1,1,dpi=100)
# df.close.plot(ax=ax);
# ax.set_xlabel('time');
# ax.set_ylabel('close price');
# plt.show()

"""Verify Column Names:
Check the column names in the DataFrame to ensure type exists:"""

print(df.columns)

""" Rename or Create the type Column:
If the column does not exist, you can either:

Rename an existing column to type """

df.rename(columns={'existing_column_name': 'type'}, inplace=True)

print(df.columns)

# Create a new type column with appropriate values:

df['type'] = 'default_value' 

print(df.columns)

"""Ensure weekday Column Exists:
Similarly, verify the weekday column exists. If not, you can create it based on the date column as follows:"""

df['weekday'] = df['date'].dt.day_name()  # Extract weekday names from the 'date' column

print(df.columns)

# sns.catplot(x="type", hue="weekday", kind="count", data=df)
# plt.show()

# We observed that there are some entries for weekends (Saturday and Sunday) in the data. May be these days fall on the evening on the day of Diwali, if Diwali falls on Saturday or Sunday. This is called Muharat trading. Lets ignore this data and hence lets drop it from further analysis.

"""banknifty = banknifty.drop(banknifty[banknifty.weekday >=5].index); # drop Muharat trading days.
sns.catplot(x ="type", hue ="weekday",kind ="count", data = banknifty);  """

# df = df.drop(df[df.weekday >=5].index); # drop Muharat trading days.
# sns.catplot(x ="type", hue ="weekday",kind ="count", data = df);
# plt.show()

"""The error occurs because the weekday column in the DataFrame contains string values (e.g., "Monday", "Tuesday") instead of integers. The comparison df.weekday >= 5 is invalid because Python cannot compare strings with integers.

Fix:
Convert the weekday column to integers representing the days of the week (e.g., Monday = 0, Sunday = 6) before performing the comparison. """

# Convert 'weekday' column to integers (Monday=0, Sunday=6)
df['weekday'] = pd.to_datetime(df['date']).dt.weekday

# Drop rows where 'weekday' is greater than or equal to 5 (Saturday and Sunday)
df = df.drop(df[df['weekday'] >= 5].index)

# pd.to_datetime(df['date']).dt.weekday:
# Converts the date column to a datetime object and extracts the day of the week as an integer (Monday = 0, Sunday = 6).
# [df.drop(df[df['weekday'] >= 5].index)](http://vscodecontentref/2):
# Drops rows where the weekday column has values 5 or 6 (Saturday and Sunday).

df = df.drop(df[df.weekday >=5].index); # drop Muharat trading days.

"""Set the default value of the 'type' column based on weekdays (Monday to Friday) and labe
l weekends as 'Weekend'."""

df['type'] = df['weekday'].apply(lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][x] if x < 5 else 'Weekend')
sns.catplot(x ="type", hue ="weekday",kind ="count", data = df, palette=['blue', 'green', 'orange', 'red', 'violet']);
plt.show()

"""Set the default value of the 'type' column based on weekdays (Monday to Friday) and label weekends as 'Weekend'."""

df['type'] = df['weekday'].apply(lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][x] if x < 5 else 'Weekend')