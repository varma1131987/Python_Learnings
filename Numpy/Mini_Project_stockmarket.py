# mini‑project for the “Stock or Crypto Time Series Analysis” using NumPy.
# Step 1: Import Necessary Libraries ans sample data  
import numpy as np  

import numpy as np

# File path
file_path = r"C:\Users\Hp\github\Python_Learnings\Numpy\90days.csv"

# Read the CSV file
# data = np.genfromtxt(file_path, delimiter=',', skip_header=1)  # Skip header row if present
# # Print the data
# print("Data from CSV:\n", data)

data = np.genfromtxt(
    file_path,
    delimiter=',',
    skip_header=1,
    dtype=None,          # allow mixed types
    encoding='utf-8'     # for strings
)

# print("Raw data:\n", data)

# import numpy as np

# Set NumPy to display numbers in full decimal format
np.set_printoptions(suppress=True,precision=10)  # Suppress scientific notation

print("Raw data (decimal format):\n", data)


# Extract columns
dates   = np.array([row[0] for row in data])          # date (string)
opens   = np.array([row[1] for row in data], float)   # open
highs   = np.array([row[2] for row in data], float)   # high
lows    = np.array([row[3] for row in data], float)   # low
closes  = np.array([row[4] for row in data], float)   # close
volumes = np.array([row[5] for row in data], float)   # volume

print("First 5 dates: ", dates[:5])
print("First 5 closes:", closes[:5])


# Use your closes array as close_a and follow these exact steps to compute daily returns.

close_a = closes  # if you have only one asset

# Create current and previous price arrays

current_prices  = close_a[1:]   # from second day to last day
previous_prices = close_a[:-1]  # from first day to second-last day

# Calculate daily returns

daily_returns = (current_prices - previous_prices) / previous_prices

print("First 5 daily returns:", daily_returns[:5])
print("Total returns count:", len(daily_returns))
print("Original closes count:", len(close_a))

##################################################

# closes already defined from earlier
window_short = 5
kernel_short = np.ones(window_short) / window_short   # [1/5, 1/5, 1/5, 1/5, 1/5]

ma5 = np.convolve(closes, kernel_short, mode='valid')

print("Length of closes:", len(closes))
print("Length of 5-day MA:", len(ma5))
print("First 5 values of 5-day MA:", ma5[:5])

# ma5 will have len(closes) - 5 + 1 values because mode='valid' only keeps full windows.

window_long = 20
kernel_long = np.ones(window_long) / window_long      # [1/20, ..., 1/20]

ma20 = np.convolve(closes, kernel_long, mode='valid')

print("Length of 20-day MA:", len(ma20))
print("First 5 values of 20-day MA:", ma20[:5])
# ma20 will have len(closes) - 20 + 1 values because mode='valid' only keeps full windows.

# You can now use dates_ma5 with ma5, and dates_ma20 with ma20 in tables or plots in your mini‑project report

# next Step 

threshold = 0.01  # 2% daily return 

high_days_mask = daily_returns > threshold

print("High-return mask (first 10):", high_days_mask[:10])

# Count high‑return days

num_high_days = np.sum(high_days_mask)
print("Number of days with return > 2%:", num_high_days)

#  Map back to dates correctly
# # Returns start from the second date (because each return uses today and yesterday), so align with dates[1:]:

high_return_dates = dates[1:][high_days_mask]

print("Dates with return > 2%:")
for d in high_return_dates:
    print(d)

# Now you have both the count and the exact dates for your report

