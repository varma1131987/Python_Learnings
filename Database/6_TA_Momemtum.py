# Momentum Indicators  
"""
ADX                  Average Directional Movement Index
ADXR                 Average Directional Movement Index Rating
APO                  Absolute Price Oscillator
AROON                Aroon
AROONOSC             Aroon Oscillator
BOP                  Balance Of Power
CCI                  Commodity Channel Index
CMO                  Chande Momentum Oscillator
DX                   Directional Movement Index
MACD                 Moving Average Convergence/Divergence
MACDEXT              MACD with controllable MA type
MACDFIX              Moving Average Convergence/Divergence Fix 12/26
MFI                  Money Flow Index
MINUS_DI             Minus Directional Indicator
MINUS_DM             Minus Directional Movement
MOM                  Momentum
PLUS_DI              Plus Directional Indicator
PLUS_DM              Plus Directional Movement
PPO                  Percentage Price Oscillator
ROC                  Rate of change : ((price/prevPrice)-1)*100
ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
ROCR                 Rate of change ratio: (price/prevPrice)
ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
RSI                  Relative Strength Index
STOCH                Stochastic
STOCHF               Stochastic Fast
STOCHRSI             Stochastic Relative Strength Index
TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
ULTOSC               Ultimate Oscillator
WILLR                Williams' %R   """


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt     
from mysql.connector import connect, Error  
from dotenv import load_dotenv
import sys
import os
import seaborn as sns
from ta.momentum import (RSIIndicator, StochasticOscillator, WilliamsRIndicator, ROCIndicator, AwesomeOscillatorIndicator, KAMAIndicator)
from ta.trend import ADXIndicator, AroonIndicator, CCIIndicator, MACD
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
print(df.dtypes)
      
# Convert the fetched DataFrame into separate numpy arrays excluding 'symbol'
# Ensure the DataFrame is cleaned and sorted before extraction
data = df[['date', 'open', 'high', 'low', 'close', 'volume']].values  # Exclude 'symbol' column

dates = np.array([str(row[0]) for row in data])      # Convert date to string
opens = np.array([float(row[1]) for row in data])    # Convert open to float
highs = np.array([float(row[2]) for row in data])    # Convert high to float
lows = np.array([float(row[3]) for row in data])     # Convert low to float
closes = np.array([float(row[4]) for row in data])   # Convert close to float
volumes = np.array([float(row[5]) for row in data])  # Convert volume to float

# Print the latest 5 entries for verification
print("Latest 5 dates: ", dates[-5:])
print("Latest 5 closes:", closes[-5:])

# Calculate Momentum Indicators using the 'ta' library

# RSI (14-day)
rsi = RSIIndicator(close=df['close'], window=14)
df['rsi_14'] = rsi.rsi()
print(df[['close', 'rsi_14']].tail())

# # Adding implementations for all momentum indicators
# from ta.momentum import (RSIIndicator, StochasticOscillator, WilliamsRIndicator, ROCIndicator, AwesomeOscillatorIndicator, KAMAIndicator)
# from ta.trend import ADXIndicator, AroonIndicator, CCIIndicator, MACD
# from ta.volatility import BollingerBands

# # Calculate additional indicators
# # ADX (14-day)
# adx = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
# df['adx'] = adx.adx()
# df['adx_pos'] = adx.adx_pos()
# df['adx_neg'] = adx.adx_neg()

# # Aroon (14-day)
# aroon = AroonIndicator(close=df['close'], window=14)
# df['aroon_up'] = aroon.aroon_up()
# df['aroon_down'] = aroon.aroon_down()

# # MACD
# macd = MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
# df['macd'] = macd.macd()
# df['macd_signal'] = macd.macd_signal()
# df['macd_diff'] = macd.macd_diff()

# # Stochastic Oscillator
# stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=14, smooth_window=3)
# df['stoch_k'] = stoch.stoch_k()
# df['stoch_d'] = stoch.stoch_d()

# # Williams %R
# williams = WilliamsRIndicator(high=df['high'], low=df['low'], close=df['close'], lbp=14)
# df['williams_r'] = williams.wr()

# # Rate of Change (ROC)
# roc = ROCIndicator(close=df['close'], window=12)
# df['roc'] = roc.roc()

# # Commodity Channel Index (CCI)
# cci = CCIIndicator(high=df['high'], low=df['low'], close=df['close'], window=20)
# df['cci'] = cci.cci()

# # Bollinger Bands
# bollinger = BollingerBands(close=df['close'], window=20, window_dev=2)
# df['bollinger_mavg'] = bollinger.bollinger_mavg()
# df['bollinger_hband'] = bollinger.bollinger_hband()
# df['bollinger_lband'] = bollinger.bollinger_lband()

# # Adding implementations for the remaining indicators
# from ta.momentum import (CMOIndicator, KAMAIndicator, PercentagePriceOscillator, StochasticRSIIndicator, TRIXIndicator, UltimateOscillator)

# # Chande Momentum Oscillator (CMO)
# cmo = CMOIndicator(close=df['close'], window=14)
# df['cmo'] = cmo.cmo()

# # KAMA (Kaufman's Adaptive Moving Average)
# kama = KAMAIndicator(close=df['close'], window=10, pow1=2, pow2=30)
# df['kama'] = kama.kama()

# # Percentage Price Oscillator (PPO)
# ppo = PercentagePriceOscillator(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
# df['ppo'] = ppo.ppo()
# df['ppo_signal'] = ppo.ppo_signal()
# df['ppo_hist'] = ppo.ppo_hist()

# # Stochastic RSI
# stoch_rsi = StochasticRSIIndicator(close=df['close'], window=14, smooth1=3, smooth2=3)
# df['stoch_rsi_k'] = stoch_rsi.stochrsi_k()
# df['stoch_rsi_d'] = stoch_rsi.stochrsi_d()

# # TRIX
# trix = TRIXIndicator(close=df['close'], window=15)
# df['trix'] = trix.trix()

# # Ultimate Oscillator
# ult_osc = UltimateOscillator(high=df['high'], low=df['low'], close=df['close'], window1=7, window2=14, window3=28)
# df['ult_osc'] = ult_osc.ultimate_oscillator()

# # Print the last 5 days of all indicators
# print(df.tail(5))

# # Ensure all columns used in indicators are cleaned and converted to numeric
# # Replace None or NaN values in 'high', 'low', and 'close' columns with 0
# df['high'] = pd.to_numeric(df['high'], errors='coerce').fillna(0)
# df['low'] = pd.to_numeric(df['low'], errors='coerce').fillna(0)
# df['close'] = pd.to_numeric(df['close'], errors='coerce').fillna(0)

# # Re-run the ADX calculation
# adx = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
# df['adx'] = adx.adx()
# df['adx_pos'] = adx.adx_pos()
# df['adx_neg'] = adx.adx_neg()


# # Use your closes array as close_a and follow these exact steps to compute daily returns.   
# close_a = closes  # if you have only one asset
# # Create current and previous price arrays
# current_prices  = close_a[1:]   # from second day to last day
# previous_prices = close_a[:-1]  # from first day to second-last day
# # Calculate daily returns
# daily_returns = (current_prices - previous_prices) / previous_prices
# print("First 5 daily returns:", daily_returns[:5])
# print("Total returns count:", len(daily_returns))
# print("Original closes count:", len(close_a))
# # ##################################################
# # closes already defined from earlier
# window_short = 5
# kernel_short = np.ones(window_short) / window_short   # [1/5, 1/5, 1/5, 1/5, 1/5]
# ma5 = np.convolve(closes, kernel_short, mode='valid')
# print("Length of closes:", len(closes))
# print("Length of 5-day MA:", len(ma5))  
# print("First 5 values of 5-day MA:", ma5[:5])
# # ma5 will have len(closes) - 5 + 1 values because mode='valid' only keeps full windows.
# window_long = 20
# kernel_long = np.ones(window_long) / window_long      # [1/20, ..., 1/20]
# ma20 = np.convolve(closes, kernel_long, mode='valid')
# print("Length of 20-day MA:", len(ma20))
# print("First 5 values of 20-day MA:", ma20[:5])
# # ma20 will have len(closes) - 20 + 1 values because mode='valid' only keeps full windows.
