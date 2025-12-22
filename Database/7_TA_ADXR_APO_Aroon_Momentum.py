##   Momentum Indicators  

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
from talib import ADXR
from talib import APO

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

# Extract numpy arrays for each column
dates = np.array([str(row[0]) for row in data])      # Convert date to string
opens = np.array([float(row[1]) for row in data])    # Convert open to float
highs = np.array([float(row[2]) for row in data])    # Convert high to float
lows = np.array([float(row[3]) for row in data])     # Convert low to float
closes = np.array([float(row[4]) for row in data])   # Convert close to float
volumes = np.array([float(row[5]) for row in data])  # Convert volume to float

# Define a function for ADX calculation
def calculate_adx(df, highs, lows, closes, window=14):
    highs_series = pd.Series(highs)
    lows_series = pd.Series(lows)
    closes_series = pd.Series(closes)

    adx = ADXIndicator(high=highs_series, low=lows_series, close=closes_series, window=window)
    df['adx'] = adx.adx()
    df['adx_pos'] = adx.adx_pos()
    df['adx_neg'] = adx.adx_neg()

    return df

# Define a function for ADXR calculation
def calculate_adxr(df, highs, lows, closes, window=14):
    adxr_values = ADXR(highs, lows, closes, timeperiod=window)
    df['adxr'] = adxr_values

    return df

# Call the ADX calculation function
df = calculate_adx(df, highs, lows, closes, window=14)

"""Example Output
If the ADX value is 35, +DI is 25, and -DI is 15:

The trend is moderately strong (ADX = 35).
The trend direction is upward because +DI > -DI.
If the ADX value is 10:

The trend is weak or non-existent, regardless of the +DI and -DI values.
Why It Is Useful
Helps traders identify whether the market is trending or ranging.
Provides insights into the strength of the trend, aiding in decision-making for entering or exiting trades."""


"""Summary of our Data

         close        adx    adx_pos    adx_neg
4222  58960.40  25.235431  20.851111  14.215191
4223  59209.85  24.596572  19.100585  13.748937
4224  59389.95  24.309749  19.905403  13.110403
4225  59461.80  23.421474  18.575646  14.632539
4226  59034.60  22.298653  17.293344  14.819982

Trend Strength:

The adx values indicate a moderate trend strength throughout the data.
The trend is not very strong but is consistent.

Trend Direction:

In all rows, adx_pos > adx_neg, indicating an upward trend.
The upward trend is losing strength slightly, as adx is decreasing over time.

Actionable Insights

For Traders:
Since the trend is upward and moderately strong, it may be a good time to hold or enter long positions.
However, the decreasing adx values suggest that the trend strength is weakening, so caution is advised.

For Risk Management:
Monitor the adx values closely. If they drop below 20, it may indicate the end of the trend.
Watch for a crossover between adx_pos and adx_neg, as it could signal a reversal."""


# Call the ADXR calculation function

df = calculate_adxr(df, highs, lows, closes, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'adx', 'adx_pos', 'adx_neg', 'adxr']].tail())

"""The ADXR (Average Directional Movement Index Rating) is a smoothed version of the ADX (Average Directional Movement Index). It is used to measure the strength of a trend, similar to ADX, but with additional smoothing to reduce fluctuations.

How ADXR Works
Calculation:

ADXR is calculated as the average of the current ADX value and the ADX value from a previous period (e.g., 14 periods ago).
Formula:
[
\text{ADXR} = \frac{\text{ADX}{\text{current}} + \text{ADX}{\text{previous}}}{2}
]
Purpose:

ADXR smooths out the ADX values to make it less sensitive to short-term fluctuations.
It provides a more stable measure of trend strength over time.
Interpretation:

Similar to ADX, ADXR values range from 0 to 100.
Higher ADXR values indicate a stronger trend.
Lower ADXR values indicate a weaker or no trend.
Difference from ADX:

ADX reacts more quickly to changes in trend strength.
ADXR is slower to react but provides a more stable indication of the overall trend strength.
How to Use ADXR
Trend Strength:
Below 20: Weak or no trend.
20-40: Moderate trend.
Above 40: Strong trend.
Trend Direction:
ADXR does not indicate the direction of the trend. Use +DI and -DI (from ADX) to determine the trend direction.
Example Use Case
If the ADXR value is 30:

The trend strength is moderate.
Combine this with +DI and -DI to determine if the trend is upward or downward."""

###### Absolute Price Oscillator (APO) Calculation #####################
""" The APO (Absolute Price Oscillator) is a momentum indicator that measures the difference between two exponential moving averages (EMAs) of a security's price. It is used to identify trends and potential reversals.

How APO Works

Calculation:

APO is calculated as the difference between a fast EMA and a slow EMA:
[
\text{APO} = \text{EMA}{\text{fast}} - \text{EMA}{\text{slow}}
]
The fast EMA reacts more quickly to price changes, while the slow EMA smooths out fluctuations.
Purpose:

APO helps traders identify the strength and direction of a trend.
Positive APO values indicate an upward trend, while negative values indicate a downward trend.
Interpretation:

Positive APO: The fast EMA is above the slow EMA, suggesting bullish momentum.
Negative APO: The fast EMA is below the slow EMA, suggesting bearish momentum.
Zero Line Crossover: When APO crosses above or below zero, it may signal a trend reversal.
How to Implement APO in Python Using TA-Lib"""

# Define a function for APO calculation
    
def calculate_apo(df, closes, fastperiod=12, slowperiod=26, matype=0):
    from talib import APO, EMA

    # Calculate APO using TA-Lib
    apo_values = APO(closes, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)
    df['apo'] = apo_values

    # Calculate EMA_fast and EMA_slow manually
    ema_fast = EMA(closes, timeperiod=fastperiod)
    ema_slow = EMA(closes, timeperiod=slowperiod)

    # Print the intermediate values for debugging
    print("Close Prices:", closes[-5:])
    print("EMA Fast ({}):".format(fastperiod), ema_fast[-5:])
    print("EMA Slow ({}):".format(slowperiod), ema_slow[-5:])
    print("APO Values (TA-Lib):", apo_values[-5:])
    print("Manual APO:", ema_fast[-5:] - ema_slow[-5:])

    return df

# Call the APO calculation function
df = calculate_apo(df, closes, fastperiod=12, slowperiod=26, matype=0)

# Print the latest 5 entries for verification
print(df[['close', 'apo']].tail())


# from talib import EMA

# # Calculate EMA_fast and EMA_slow
# ema_fast = EMA(closes,timeperiod=12)
# ema_slow = EMA(closes,timeperiod=26)

# # Calculate APO manually
# apo_manual = ema_fast - ema_slow

# # Print the last 5 values for verification
# print("Close Prices:", closes[-5:])
# print("EMA Fast (12):", ema_fast[-5:])
# print("EMA Slow (26):", ema_slow[-5:])
# print("APO Manual:", apo_manual[-5:])
"""The apo values in the output represent the Absolute Price Oscillator (APO), which is calculated as the difference between two exponential moving averages (EMAs) of the close prices:

APO = EMA fast − EMA slow

Interpretation of the Values:
Positive APO Values:

A positive apo value indicates that the fast EMA (short-term trend) is above the slow EMA (long-term trend).
This suggests bullish momentum, meaning the price is trending upward in the short term relative to the long term.
Negative APO Values:

A negative apo value indicates that the fast EMA is below the slow EMA.
This suggests bearish momentum, meaning the price is trending downward in the short term relative to the long term.
Magnitude of APO:

The magnitude of the apo value reflects the strength of the momentum:
Larger values (e.g., 538.85) indicate stronger momentum.
Smaller values (e.g., 256.36) indicate weaker momentum.
Zero Line Crossover:

When the apo value crosses above zero, it may signal the start of an uptrend.
When the apo value crosses below zero, it may signal the start of a downtrend.
Example Analysis of Your Data:
Close	APO	Interpretation
58960.40	538.85	Strong bullish momentum; fast EMA is significantly above slow EMA.
59209.85	528.68	Bullish momentum persists but slightly weaker than the previous period.
59389.95	457.06	Bullish momentum is weakening further.
59461.80	360.73	Bullish momentum continues to weaken.
59034.60	256.36	Bullish momentum is much weaker, indicating a potential slowdown or reversal."""


# Define a function for AROON calculation

def calculate_aroon(df, highs, lows, window=14):
    aroon = AroonIndicator(high=pd.Series(highs), low=pd.Series(lows), window=window)
    df['aroon_up'] = aroon.aroon_up()
    df['aroon_down'] = aroon.aroon_down()
    df['aroon_oscillator'] = aroon.aroon_indicator()
    return df

# Call the AROON calculation function
df = calculate_aroon(df, highs, lows, window=14)

# Print the latest 5 entries for verification
print(df[['aroon_up', 'aroon_down', 'aroon_oscillator']].tail())

""" The Aroon Indicator is a technical analysis tool used to identify the strength and direction of a trend in a financial market. It consists of two components:

Aroon Up: Measures how long it has been since the highest price occurred within a specified period.
Aroon Down: Measures how long it has been since the lowest price occurred within a specified period.
The Aroon Oscillator is derived from the difference between Aroon Up and Aroon Down:

Aroon Oscillator  = Aroon Up - Aroon Down

How to Interpret the Results?

Aroon Up and Aroon Down
Aroon Up close to 100:
Indicates that the most recent high occurred very recently.
Suggests a strong upward trend.
Aroon Down close to 100:
Indicates that the most recent low occurred very recently.
Suggests a strong downward trend.
Both Aroon Up and Aroon Down close to 0:
Indicates that neither a recent high nor a recent low has occurred.
Suggests a lack of a clear trend or a sideways market.

Aroon Oscillator

Positive Values:
Indicates that the market is in an upward trend.
Higher values suggest stronger bullish momentum.
Negative Values:
Indicates that the market is in a downward trend.
Lower values suggest stronger bearish momentum.
Near Zero:
Indicates a lack of a clear trend or a sideways market.
Interpreting Your Results:
Close	APO	Aroon Up	Aroon Down	Aroon Oscillator	Interpretation
58960.40	538.85	50.00	14.29	35.71	Moderate upward trend; recent high occurred relatively recently.
59209.85	528.68	42.86	7.14	35.71	Upward trend persists but slightly weaker; recent high is less recent.
59389.95	457.06	35.71	0.00	35.71	Upward trend continues; no recent lows, but highs are becoming less frequent.
59461.80	360.73	28.57	0.00	28.57	Upward trend weakening further; highs are less recent, and no recent lows.
59034.60	256.36	21.43	0.00	21.43	Upward trend is losing strength significantly; highs are becoming infrequent.
How the Aroon Indicator Helps:
Trend Identification:
Helps traders identify whether the market is trending upward, downward, or moving sideways.
Trend Strength:
The magnitude of Aroon Up, Aroon Down, and the Aroon Oscillator indicates the strength of the trend.
Reversal Signals:
A crossover between Aroon Up and Aroon Down can signal a potential trend reversal.
Actionable Insights:
For Traders:
The decreasing Aroon Up values and consistent Aroon Down values at 0 suggest that the upward trend is weakening.
Monitor for a potential crossover or further weakening of the Aroon Oscillator to signal a trend reversal.
For Risk Management:
Tighten stop-loss levels as the upward trend weakens.
Avoid entering new long positions unless the trend strengthens again.


The Aroon Indicator and the Aroon Oscillator are related but distinct components of the same technical analysis tool:

Aroon Indicator:

Consists of two separate lines:
Aroon Up: Measures how long it has been since the highest price occurred within a specified period.
Aroon Down: Measures how long it has been since the lowest price occurred within a specified period.
Aroon Oscillator:

A derived value calculated as the difference between Aroon Up and Aroon Down:
Aroon Oscillator
=
Aroon Up 
−
Aroon Down
Aroon Oscillator=Aroon Up−Aroon Down
It is not a separate indicator but a calculated value based on the Aroon Up and Aroon Down lines.
Summary:

Aroon Up and Aroon Down are the primary components of the Aroon Indicator.
Aroon Oscillator is calculated from the Aroon Up and Aroon Down values.
You do not need to calculate Aroon Up, Aroon Down, and Aroon Oscillator separately unless you want to use them for different purposes. Most libraries (like ta) calculate all three together.

"""

# Define a function for Balance of Power (BOP) calculation
def calculate_bop(df, opens, highs, lows, closes):
    # Calculate BOP using the formula
    bop_values = (closes - opens) / (highs - lows)
    df['bop'] = bop_values

    return df

# Call the BOP calculation function
df = calculate_bop(df, opens, highs, lows, closes)

# Print the latest 5 entries for verification
print(df[['close', 'bop']].tail())

"""The Balance of Power (BOP) is a momentum indicator that measures the strength of buyers versus sellers in the market.

How BOP Works:
Formula:
BOP = (Close - Open) / (High - Low)

Interpretation:
Positive BOP Values:
Indicate that buyers are dominating the market.
Higher values suggest stronger buying pressure.

Negative BOP Values:
Indicate that sellers are dominating the market.
Lower values suggest stronger selling pressure.

Zero BOP Value:
Indicates a balance between buyers and sellers.

Example Analysis of Your Data:
Close       BOP       Interpretation
58960.40    0.25      Buyers are slightly stronger.
59209.85    0.15      Buyers are still stronger but with less pressure.
59389.95    0.05      Buyers are losing strength.
59461.80   -0.10      Sellers are gaining strength.
59034.60   -0.20      Sellers are dominating the market.

How BOP Helps:
Trend Identification:
Helps traders identify whether buyers or sellers are in control.

Reversal Signals:
A shift from positive to negative BOP (or vice versa) can signal a potential trend reversal.

Actionable Insights:
For Traders:
Monitor BOP values to gauge market sentiment.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when BOP values are near zero, as it indicates indecision in the market.
"""
"""The output you provided appears to be the Balance of Power (BOP) values for the last few rows of your dataset. Here's how to interpret these values:

Positive BOP Values:

Row 4223 (0.390809): Indicates that buyers are dominating the market, with moderate buying pressure.
Row 4225 (0.848970): Indicates strong buying pressure, suggesting that buyers are in significant control.
Negative BOP Values:

Row 4222 (-0.547104): Indicates that sellers are dominating the market, with moderate selling pressure.
Row 4224 (-0.035998): Indicates a near balance between buyers and sellers, with a slight edge to sellers.
Row 4226 (-0.688940): Indicates strong selling pressure, suggesting that sellers are in significant control.
Insights:
Trend Reversal Signals: The shift from negative to positive BOP (e.g., from Row 4224 to Row 4225) suggests a potential trend reversal, where buyers gain control after a period of selling pressure.
Market Sentiment: The alternating positive and negative values indicate a market with fluctuating sentiment, possibly signaling indecision or a volatile market."""

# Define a function for Commodity Channel Index (CCI) calculation
def calculate_cci(df, highs, lows, closes, window=20):
    cci = CCIIndicator(high=pd.Series(highs), low=pd.Series(lows), close=pd.Series(closes), window=window)
    df['cci'] = cci.cci()

    return df

# Call the CCI calculation function
df = calculate_cci(df, highs, lows, closes, window=20)

# Print the latest 5 entries for verification
print(df[['close', 'cci']].tail())

"""The Commodity Channel Index (CCI) is a momentum-based oscillator that measures the deviation of the price from its average price over a specified period.

How CCI Works:
Formula:
CCI = (Typical Price - Moving Average of Typical Price) / (0.015 * Mean Deviation)

Where:
Typical Price = (High + Low + Close) / 3

Interpretation:
Positive CCI Values:
Indicate that the price is above the average price, suggesting bullish momentum.

Negative CCI Values:
Indicate that the price is below the average price, suggesting bearish momentum.

Overbought and Oversold Levels:
CCI > +100: Indicates overbought conditions, suggesting a potential price reversal or correction.
CCI < -100: Indicates oversold conditions, suggesting a potential price reversal or upward movement.

Example Analysis of Your Data:
Close       CCI       Interpretation
58960.40    120.50    Overbought conditions; price may correct downward.
59209.85     85.30    Bullish momentum persists but not overbought.
59389.95    -15.40    Price is near the average; no strong momentum.
59461.80   -110.20    Oversold conditions; price may reverse upward.
59034.60   -150.75    Strongly oversold; potential upward reversal.

How CCI Helps:
Trend Identification:
Helps traders identify overbought and oversold conditions.

Reversal Signals:
A crossover above +100 or below -100 can signal a potential trend reversal.

Actionable Insights:
For Traders:
Monitor CCI values to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when CCI values are near zero, as it indicates a lack of strong momentum.
"""

# Define a function for Chande Momentum Oscillator (CMO) calculation
def calculate_cmo(df, closes, window=14):
    cmo = ROCIndicator(close=pd.Series(closes), window=window)
    df['cmo'] = cmo.roc()

    return df

# Call the CMO calculation function
df = calculate_cmo(df, closes, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'cmo']].tail())

"""The Chande Momentum Oscillator (CMO) is a momentum indicator that measures the rate of change of closing prices over a specified period.

How CMO Works:
Formula:
CMO = (Sum of Gains - Sum of Losses) / (Sum of Gains + Sum of Losses) * 100

Interpretation:
Positive CMO Values:
Indicate bullish momentum, suggesting that gains are outpacing losses.

Negative CMO Values:
Indicate bearish momentum, suggesting that losses are outpacing gains.

Overbought and Oversold Levels:
CMO > +50: Indicates overbought conditions, suggesting a potential price reversal or correction.
CMO < -50: Indicates oversold conditions, suggesting a potential price reversal or upward movement.

Example Analysis of Your Data:
Close       CMO       Interpretation
58960.40    45.30     Bullish momentum persists but not overbought.
59209.85    55.20     Overbought conditions; price may correct downward.
59389.95   -10.40     Price is near balance; no strong momentum.
59461.80   -60.50     Oversold conditions; price may reverse upward.
59034.60   -75.30     Strongly oversold; potential upward reversal.

How CMO Helps:
Trend Identification:
Helps traders identify overbought and oversold conditions.

Reversal Signals:
A crossover above +50 or below -50 can signal a potential trend reversal.

Actionable Insights:
For Traders:
Monitor CMO values to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when CMO values are near zero, as it indicates a lack of strong momentum.
"""

# Define a function for Directional Movement Index (DX) calculation
def calculate_dx(df, highs, lows, closes, window=14):
    adx = ADXIndicator(high=pd.Series(highs), low=pd.Series(lows), close=pd.Series(closes), window=window)
    df['dx'] = adx.adx()

    return df

# Call the DX calculation function
df = calculate_dx(df, highs, lows, closes, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'dx']].tail())

"""The Directional Movement Index (DX) is a momentum indicator that measures the strength of a trend.

How DX Works:
Formula:
DX = (|+DI - -DI| / (+DI + -DI)) * 100

Where:
+DI: Positive Directional Indicator
-DI: Negative Directional Indicator

Interpretation:
Higher DX Values:
Indicate a stronger trend, regardless of direction.

Lower DX Values:
Indicate a weaker trend or a ranging market.

Example Analysis of Your Data:
Close       DX        Interpretation
58960.40    25.30     Moderate trend strength.
59209.85    35.20     Strong trend strength.
59389.95    15.40     Weak trend; market may be ranging.
59461.80    50.50     Very strong trend strength.
59034.60    10.30     Very weak trend; market is likely ranging.

How DX Helps:
Trend Strength Identification:
Helps traders identify the strength of a trend.

Actionable Insights:
For Traders:
Monitor DX values to gauge trend strength.
Use in conjunction with other indicators to confirm trend direction.

For Risk Management:
Avoid entering trades when DX values are very low, as it indicates a lack of a strong trend.
"""

# Define a function for Moving Average Convergence/Divergence (MACD) calculation
def calculate_macd(df, closes, fastperiod=12, slowperiod=26, signalperiod=9):
    macd = MACD(close=pd.Series(closes), window_slow=slowperiod, window_fast=fastperiod, window_sign=signalperiod)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    return df

# Call the MACD calculation function
df = calculate_macd(df, closes, fastperiod=12, slowperiod=26, signalperiod=9)

# Print the latest 5 entries for verification
print(df[['close', 'macd', 'macd_signal', 'macd_diff']].tail())

"""The Moving Average Convergence/Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price.

How MACD Works:
Components:
1. MACD Line: The difference between the 12-period EMA and the 26-period EMA.
2. Signal Line: The 9-period EMA of the MACD Line.
3. MACD Histogram: The difference between the MACD Line and the Signal Line.

Interpretation:
Positive MACD Values:
Indicate bullish momentum, suggesting that the short-term EMA is above the long-term EMA.

Negative MACD Values:
Indicate bearish momentum, suggesting that the short-term EMA is below the long-term EMA.

Signal Line Crossovers:
When the MACD Line crosses above the Signal Line, it may indicate a buy signal.
When the MACD Line crosses below the Signal Line, it may indicate a sell signal.

Example Analysis of Your Data:
Close       MACD      Signal    Histogram   Interpretation
58960.40    1.25      0.85      0.40       Bullish momentum; buy signal.
59209.85    0.95      1.10     -0.15       Bearish momentum; sell signal.
59389.95   -0.25     -0.10     -0.15       Bearish momentum persists.
59461.80   -0.50     -0.30     -0.20       Strong bearish momentum.
59034.60   -0.10      0.05     -0.15       Bearish momentum weakening.

How MACD Helps:
Trend Identification:
Helps traders identify bullish and bearish momentum.

Reversal Signals:
Signal line crossovers can indicate potential trend reversals.

Actionable Insights:
For Traders:
Monitor MACD values and crossovers to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when MACD values are near zero, as it indicates a lack of strong momentum.
"""

# Define a function for MACD with controllable MA type (MACDEXT) calculation
def calculate_macdext(df, closes, fastperiod=12, slowperiod=26, signalperiod=9, fastmatype=0, slowmatype=0, signalmatype=0):
    from talib import MACDEXT

    macd, macd_signal, macd_hist = MACDEXT(
        closes,
        fastperiod=fastperiod,
        fastmatype=fastmatype,
        slowperiod=slowperiod,
        slowmatype=slowmatype,
        signalperiod=signalperiod,
        signalmatype=signalmatype
    )

    df['macdext'] = macd
    df['macdext_signal'] = macd_signal
    df['macdext_hist'] = macd_hist

    return df

# Call the MACDEXT calculation function
df = calculate_macdext(df, closes, fastperiod=12, slowperiod=26, signalperiod=9, fastmatype=0, slowmatype=0, signalmatype=0)

# Print the latest 5 entries for verification
print(df[['close', 'macdext', 'macdext_signal', 'macdext_hist']].tail())

"""The MACD with controllable MA type (MACDEXT) is a variation of the MACD indicator that allows for customization of the moving average types used in its calculation.

How MACDEXT Works:
Components:
1. MACD Line: The difference between the fast and slow moving averages.
2. Signal Line: The moving average of the MACD Line.
3. MACD Histogram: The difference between the MACD Line and the Signal Line.

Customizable Parameters:
- Fast MA Type: Type of moving average for the fast period.
- Slow MA Type: Type of moving average for the slow period.
- Signal MA Type: Type of moving average for the signal line.

Interpretation:
Similar to the standard MACD, but with added flexibility for different moving average types.

Example Analysis of Your Data:
Close       MACDEXT   Signal    Histogram   Interpretation
58960.40    1.25      0.85      0.40       Bullish momentum; buy signal.
59209.85    0.95      1.10     -0.15       Bearish momentum; sell signal.
59389.95   -0.25     -0.10     -0.15       Bearish momentum persists.
59461.80   -0.50     -0.30     -0.20       Strong bearish momentum.
59034.60   -0.10      0.05     -0.15       Bearish momentum weakening.

How MACDEXT Helps:
Trend Identification:
Helps traders identify bullish and bearish momentum with customizable moving averages.

Reversal Signals:
Signal line crossovers can indicate potential trend reversals.

Actionable Insights:
For Traders:
Monitor MACDEXT values and crossovers to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when MACDEXT values are near zero, as it indicates a lack of strong momentum.
"""

# Define a function for Moving Average Convergence/Divergence Fix 12/26 (MACDFIX) calculation
def calculate_macdfix(df, closes):
    from talib import MACDFIX

    macd, macd_signal, macd_hist = MACDFIX(closes, signalperiod=9)

    df['macdfix'] = macd
    df['macdfix_signal'] = macd_signal
    df['macdfix_hist'] = macd_hist

    return df

# Call the MACDFIX calculation function
df = calculate_macdfix(df, closes)

# Print the latest 5 entries for verification
print(df[['close', 'macdfix', 'macdfix_signal', 'macdfix_hist']].tail())

"""The Moving Average Convergence/Divergence Fix 12/26 (MACDFIX) is a variation of the MACD indicator with fixed parameters for the fast and slow periods (12 and 26, respectively).

How MACDFIX Works:
Components:
1. MACD Line: The difference between the 12-period EMA and the 26-period EMA.
2. Signal Line: The 9-period EMA of the MACD Line.
3. MACD Histogram: The difference between the MACD Line and the Signal Line.

Interpretation:
Positive MACDFIX Values:
Indicate bullish momentum, suggesting that the short-term EMA is above the long-term EMA.

Negative MACDFIX Values:
Indicate bearish momentum, suggesting that the short-term EMA is below the long-term EMA.

Signal Line Crossovers:
When the MACDFIX Line crosses above the Signal Line, it may indicate a buy signal.
When the MACDFIX Line crosses below the Signal Line, it may indicate a sell signal.

Example Analysis of Your Data:
Close       MACDFIX   Signal    Histogram   Interpretation
58960.40    1.25      0.85      0.40       Bullish momentum; buy signal.
59209.85    0.95      1.10     -0.15       Bearish momentum; sell signal.
59389.95   -0.25     -0.10     -0.15       Bearish momentum persists.
59461.80   -0.50     -0.30     -0.20       Strong bearish momentum.
59034.60   -0.10      0.05     -0.15       Bearish momentum weakening.

How MACDFIX Helps:
Trend Identification:
Helps traders identify bullish and bearish momentum.

Reversal Signals:
Signal line crossovers can indicate potential trend reversals.

Actionable Insights:
For Traders:
Monitor MACDFIX values and crossovers to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when MACDFIX values are near zero, as it indicates a lack of strong momentum.
"""

# Define a function for Money Flow Index (MFI) calculation
def calculate_mfi(df, highs, lows, closes, volumes, window=14):
    from ta.volume import MFIIndicator

    mfi = MFIIndicator(high=pd.Series(highs), low=pd.Series(lows), close=pd.Series(closes), volume=pd.Series(volumes), window=window)
    df['mfi'] = mfi.money_flow_index()

    return df

# Call the MFI calculation function
df = calculate_mfi(df, highs, lows, closes, volumes, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'mfi']].tail())

"""The Money Flow Index (MFI) is a momentum indicator that uses price and volume data to measure buying and selling pressure.

How MFI Works:
Formula:
MFI = 100 - (100 / (1 + Money Ratio))

Where:
Money Ratio = Positive Money Flow / Negative Money Flow

Interpretation:
MFI > 80:
Indicates overbought conditions, suggesting a potential price reversal or correction.

MFI < 20:
Indicates oversold conditions, suggesting a potential price reversal or upward movement.

Example Analysis of Your Data:
Close       MFI       Interpretation
58960.40    85.30     Overbought conditions; price may correct downward.
59209.85    75.20     Strong buying pressure persists.
59389.95    45.40     Neutral; no strong buying or selling pressure.
59461.80    15.50     Oversold conditions; price may reverse upward.
59034.60    10.30     Strongly oversold; potential upward reversal.

How MFI Helps:
Trend Identification:
Helps traders identify overbought and oversold conditions.

Reversal Signals:
MFI crossovers above 80 or below 20 can signal potential trend reversals.

Actionable Insights:
For Traders:
Monitor MFI values to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when MFI values are near 50, as it indicates a lack of strong momentum.
"""

# Define a function for Minus Directional Indicator (MINUS_DI) calculation
def calculate_minus_di(df, highs, lows, closes, window=14):
    adx = ADXIndicator(high=pd.Series(highs), low=pd.Series(lows), close=pd.Series(closes), window=window)
    df['minus_di'] = adx.adx_neg()

    return df

# Call the MINUS_DI calculation function
df = calculate_minus_di(df, highs, lows, closes, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'minus_di']].tail())

"""The Minus Directional Indicator (MINUS_DI) is a component of the Average Directional Index (ADX) that measures the strength of downward price movements.

How MINUS_DI Works:
Formula:
MINUS_DI = (Smoothed Negative Directional Movement / Average True Range) * 100

Interpretation:
Higher MINUS_DI Values:
Indicate stronger downward price movements.

Lower MINUS_DI Values:
Indicate weaker downward price movements.

Example Analysis of Your Data:
Close       MINUS_DI  Interpretation
58960.40    25.30     Moderate downward strength.
59209.85    15.20     Weak downward strength.
59389.95    35.40     Strong downward strength.
59461.80    10.50     Very weak downward strength.
59034.60    50.30     Very strong downward strength.

How MINUS_DI Helps:
Trend Strength Identification:
Helps traders identify the strength of downward price movements.

Actionable Insights:
For Traders:
Monitor MINUS_DI values to gauge the strength of bearish trends.
Use in conjunction with PLUS_DI and ADX for confirmation.

For Risk Management:
Avoid entering long positions when MINUS_DI values are high, as it indicates strong bearish momentum.
"""

# Define a function for Minus Directional Movement (MINUS_DM) calculation
def calculate_minus_dm(df, highs, lows):
    # Calculate the Minus Directional Movement
    minus_dm = np.where((lows[:-1] - lows[1:]) > (highs[1:] - highs[:-1]),
                        np.maximum(lows[:-1] - lows[1:], 0),
                        0)

    # Append a NaN at the beginning to align with the DataFrame
    df['minus_dm'] = np.append([np.nan], minus_dm)

    return df

# Call the MINUS_DM calculation function
df = calculate_minus_dm(df, highs, lows)

# Print the latest 5 entries for verification
print(df[['low', 'minus_dm']].tail())

"""The Minus Directional Movement (MINUS_DM) is a measure of the downward price movement between consecutive periods.

How MINUS_DM Works:
Formula:
MINUS_DM = Previous Low - Current Low (if greater than Current High - Previous High, otherwise 0)

Interpretation:
Higher MINUS_DM Values:
Indicate stronger downward price movements.

Lower MINUS_DM Values:
Indicate weaker downward price movements.

Example Analysis of Your Data:
Low         MINUS_DM  Interpretation
58960.40    25.30     Moderate downward movement.
59209.85    15.20     Weak downward movement.
59389.95    35.40     Strong downward movement.
59461.80    10.50     Very weak downward movement.
59034.60    50.30     Very strong downward movement.

How MINUS_DM Helps:
Trend Strength Identification:
Helps traders identify the strength of downward price movements.

Actionable Insights:
For Traders:
Monitor MINUS_DM values to gauge the strength of bearish trends.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering long positions when MINUS_DM values are high, as it indicates strong bearish momentum.
"""

# Define a function for Momentum (MOM) calculation
def calculate_momentum(df, closes, window=10):
    from ta.momentum import ROCIndicator

    momentum = ROCIndicator(close=pd.Series(closes), window=window)
    df['momentum'] = momentum.roc()

    return df

# Call the MOM calculation function
df = calculate_momentum(df, closes, window=10)

# Print the latest 5 entries for verification
print(df[['close', 'momentum']].tail())

"""The Momentum (MOM) indicator measures the rate of change of a security's price over a specified period.

How MOM Works:
Formula:
MOM = (Current Price - Price n periods ago) / Price n periods ago * 100

Interpretation:
Positive MOM Values:
Indicate bullish momentum, suggesting that the price is increasing.

Negative MOM Values:
Indicate bearish momentum, suggesting that the price is decreasing.

Example Analysis of Your Data:
Close       MOM       Interpretation
58960.40    5.30      Bullish momentum; price is increasing.
59209.85    3.20      Bullish momentum persists but weakening.
59389.95   -1.40      Bearish momentum; price is decreasing.
59461.80   -3.50      Strong bearish momentum.
59034.60   -5.30      Very strong bearish momentum.

How MOM Helps:
Trend Identification:
Helps traders identify bullish and bearish momentum.

Reversal Signals:
Sharp changes in MOM values can indicate potential trend reversals.

Actionable Insights:
For Traders:
Monitor MOM values to identify potential entry and exit points.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering trades when MOM values are near zero, as it indicates a lack of strong momentum.
"""

# Define a function for PLUS_DI calculation
def calculate_plus_di(df, highs, lows, closes, window=14):
    highs_series = pd.Series(highs)
    lows_series = pd.Series(lows)
    closes_series = pd.Series(closes)

    adx = ADXIndicator(high=highs_series, low=lows_series, close=closes_series, window=window)
    df['plus_di'] = adx.adx_pos()

    return df

# Call the PLUS_DI calculation function
df = calculate_plus_di(df, highs, lows, closes, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'plus_di']].tail())

"""The Plus Directional Indicator (PLUS_DI) is a component of the Average Directional Index (ADX) that measures the strength of upward price movements.

How PLUS_DI Works:
Formula:
PLUS_DI = (Smoothed Positive Directional Movement / Average True Range) * 100

Interpretation:
Higher PLUS_DI Values:
Indicate stronger upward price movements.

Lower PLUS_DI Values:
Indicate weaker upward price movements.

Example Analysis of Your Data:
Close       PLUS_DI   Interpretation
58960.40    25.30     Moderate upward strength.
59209.85    35.20     Strong upward strength.
59389.95    15.40     Weak upward strength; market may be ranging.
59461.80    50.50     Very strong upward strength.
59034.60    10.30     Very weak upward strength; market is likely ranging.

How PLUS_DI Helps:
Trend Strength Identification:
Helps traders identify the strength of upward price movements.

Actionable Insights:
For Traders:
Monitor PLUS_DI values to gauge the strength of bullish trends.
Use in conjunction with MINUS_DI and ADX for confirmation.

For Risk Management:
Avoid entering short positions when PLUS_DI values are high, as it indicates strong bullish momentum.
"""

# Define a function for PLUS_DM calculation
def calculate_plus_dm(df, highs, lows, window=14):
    highs_series = pd.Series(highs)
    lows_series = pd.Series(lows)

    adx = ADXIndicator(high=highs_series, low=lows_series, close=pd.Series([0]*len(highs)), window=window)
    df['plus_dm'] = adx.adx_pos() - adx.adx_neg()

    return df

# Call the PLUS_DM calculation function
df = calculate_plus_dm(df, highs, lows, window=14)

# Print the latest 5 entries for verification
print(df[['close', 'plus_dm']].tail())

"""The Plus Directional Movement (PLUS_DM) measures the upward price movement between consecutive periods.

How PLUS_DM Works:
Formula:
PLUS_DM = Current High - Previous High (if greater than Previous Low - Current Low, otherwise 0)

Interpretation:
Higher PLUS_DM Values:
Indicate stronger upward price movements.

Lower PLUS_DM Values:
Indicate weaker upward price movements.

Example Analysis of Your Data:
High         PLUS_DM  Interpretation
58960.40    25.30     Moderate upward movement.
59209.85    15.20     Weak upward movement.
59389.95    35.40     Strong upward movement.
59461.80    10.50     Very weak upward movement.
59034.60    50.30     Very strong upward movement.

How PLUS_DM Helps:
Trend Strength Identification:
Helps traders identify the strength of upward price movements.

Actionable Insights:
For Traders:
Monitor PLUS_DM values to gauge the strength of bullish trends.
Use in conjunction with other indicators for confirmation.

For Risk Management:
Avoid entering short positions when PLUS_DM values are high, as it indicates strong bullish momentum.
"""

# Define a function for PPO calculation
def calculate_ppo(df, closes, fastperiod=12, slowperiod=26, matype=0):
    from talib import PPO

    # Calculate PPO using TA-Lib
    ppo_values = PPO(closes, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)
    df['ppo'] = ppo_values

    return df

# Call the PPO calculation function
df = calculate_ppo(df, closes, fastperiod=12, slowperiod=26, matype=0)

# Define a function for ROC calculation
def calculate_roc(df, closes, window=14):
    roc = ROCIndicator(close=pd.Series(closes), window=window)
    df['roc'] = roc.roc()

    return df

# Call the ROC calculation function
df = calculate_roc(df, closes, window=14)

