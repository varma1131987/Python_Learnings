# Price trend and returns analysis
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
df = df.sort_values(by='date')
# Calculate daily returns
df['daily_return'] = df['close'].pct_change()

# # Plot closing price trend
# plt.figure(figsize=(12, 6))
# plt.plot(df['date'], df['close'], label='Closing Price')
# plt.title('Closing Price Trend Over Time')  
# plt.xlabel('Date')
# plt.ylabel('Closing Price') 
# plt.legend()
# plt.show()  

# Plot daily returns
# plt.figure(figsize=(12, 6))
# plt.plot(df['date'], df['daily_return'], label='Daily Return', color='orange')
# plt.title('Daily Returns Over Time')
# plt.xlabel('Date')
# plt.ylabel('Daily Return')
# plt.legend()
# plt.show()
# # Calculate and print summary statistics for daily returns
# print("Daily Returns Summary Statistics:")
# print(df['daily_return'].describe())

# # Identify and print dates with highest and lowest returns
# max_return_date = df.loc[df['daily_return'].idxmax()]['date']
# min_return_date = df.loc[df['daily_return'].idxmin()]['date']
# print(f"Highest Daily Return on: {max_return_date.date()}")
# print(f"Lowest Daily Return on: {min_return_date.date()}")  
# # Plot histogram of daily returns
# plt.figure(figsize=(10, 5))
# plt.hist(df['daily_return'].dropna(), bins=50, color='gray', edgecolor='black')
# plt.title('Histogram of Daily Returns')
# plt.xlabel('Daily Return')  
# plt.ylabel('Frequency')
# plt.show()  
# # Calculate moving averages
df['MA20'] = df['close'].rolling(window=20).mean()
df['MA50'] = df['close'].rolling(window=50).mean()      
# Plot closing price with moving averages
plt.figure(figsize=(12, 6))     
plt.plot(df['date'], df['close'], label='Closing Price')
plt.plot(df['date'], df['MA20'], label='20-Day MA', color='red')
plt.plot(df['date'], df['MA50'], label='50-Day MA', color='green')
plt.title('Closing Price with Moving Averages')         
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# # # Identify crossover points
# df['MA_Crossover'] = np.where(df['MA20'] > df['MA50'], 1, 0)
# df['Crossover_Signal'] = df['MA_Crossover'].diff()      
# crossover_dates = df[df['Crossover_Signal'] != 0][['date', 'Crossover_Signal']]
# print("Moving Average Crossover Dates:")    
# print(crossover_dates)
# # Plot closing price with crossover points
# plt.figure(figsize=(12, 6))
# plt.plot(df['date'], df['close'], label='Closing Price')
# plt.plot(df['date'], df['MA20'], label='20-Day MA', color='red')
# plt.plot(df['date'], df['MA50'], label='50-Day MA', color='green')
# plt.scatter(crossover_dates['date'], df.loc[crossover_dates.index, 'close'],
#             color='blue', label='Crossover Points', zorder=5)
# plt.title('Closing Price with Moving Averages and Crossover Points')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend()
# plt.show()

# # Volatility analysis using rolling standard deviation
# df['Volatility'] = df['daily_return'].rolling(window=20).std() * np.sqrt(20)
# # Plot volatility over time 
# plt.figure(figsize=(12, 6))
# plt.plot(df['date'], df['Volatility'], label='20-Day Rolling Volatility', color='purple')
# plt.title('Volatility Over Time')       
# plt.xlabel('Date')
# plt.ylabel('Volatility')
# plt.legend()
# plt.show()
# # Print summary statistics for volatility
# print("Volatility Summary Statistics:")
# print(df['Volatility'].describe())
# # Identify and print dates with highest volatility
# max_volatility_date = df.loc[df['Volatility'].idxmax()]['date'] 
# print(f"Highest Volatility on: {max_volatility_date.date()}")

# Correlation analysis between closing price and volume
correlation = df['close'].corr(df['volume'])
print(f"Correlation between Closing Price and Volume: {correlation}")
# Scatter plot of closing price vs. volume
plt.figure(figsize=(10, 6)) 
plt.scatter(df['volume'], df['close'], alpha=0.5)
plt.title('Closing Price vs. Volume')
plt.xlabel('Volume')
plt.ylabel('Closing Price')
plt.show()

# Identify and print dates with unusually high volume (e.g., above 95th percentile)
high_volume_threshold = df['volume'].quantile(0.95) 
high_volume_dates = df[df['volume'] > high_volume_threshold][['date', 'volume']]
print("Dates with Unusually High Volume:")
print(high_volume_dates)
