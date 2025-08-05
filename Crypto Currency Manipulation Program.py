import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Here I set up my workspace with random data that will be constant everytime the code is run
# Data is collected every two days 
np.random.seed(50)
n_days = 100

# Now I create realistic cryptocurrency market data
dates = pd.date_range('2025-04-01', periods=n_days, freq='D')
prices = 100 + np.cumsum(np.random.normal(0, 2, n_days))  # Random walk starting at $100
volumes = np.random.normal(1000, 200, n_days)

# I intentionally inject manipulation patterns 
# First manipulation: pump and dump scheme around day 30-35
prices[30:36] = prices[30:36] + [5, 15, 25, 20, 10, -10]  # Sharp rise then crash
volumes[30:36] = volumes[30:36] * 3  # Triple volume during manipulation

# Second manipulation: another pump around day 70-72 
prices[70:73] = prices[70:73] + [8, 20, 15]
volumes[70:73] = volumes[70:73] * 2.5

# Now I organize everything into a clean data table
df = pd.DataFrame({
    'date': dates,
    'price': prices,
    'volume': volumes})

# I build my detection algorithm to catch the manipulation I just created
def detect_manipulation(df):
    df = df.copy()  
    # Calculate daily price changes as percentages
    df['price_change'] = df['price'].pct_change() * 100
    # I establish what "normal" volume looks like using 20-day average
    df['avg_volume'] = df['volume'].rolling(20).mean()
    df['volume_spike'] = df['volume'] / df['avg_volume']  # This will give me the ratio of the normal volume to the average
    # Here's my detection logic: flag days with big price moves AND unusual volume
    df['suspicious'] = ((abs(df['price_change']) > 5) &  # Price moved more than 5%
        (df['volume_spike'] > 2))         # Volume is 2x higher than normal
    
    return df

# I run my detector on the data (this should catch my planted manipulation!)
results = detect_manipulation(df)

# I examine what my algorithm found
print("Crypto Manipulation Detection Results")
print("=" * 40)

suspicious_days = results[results['suspicious'] == True]
print(f"Found {len(suspicious_days)} suspicious trading days:")
print()

for _, day in suspicious_days.iterrows():
    print(f"Date: {day['date'].strftime('%Y-%m-%d')}")
    print(f"  Price change: {day['price_change']:.1f}%")
    print(f"  Volume spike: {day['volume_spike']:.1f}x normal")
    print()

# Now I create visual evidence to see the patterns clearly
plt.figure(figsize=(12, 8))

# Price chart with suspicious days highlighted
plt.subplot(2, 1, 1)
plt.plot(results['date'], results['price'], 'b-', linewidth=2, label='Price')
# Marking the suspicious days with red dots
suspicious_dates = results[results['suspicious']]['date']
suspicious_prices = results[results['suspicious']]['price']
plt.scatter(suspicious_dates, suspicious_prices, color='red', s=100, label='Suspicious Activity', zorder=5)
plt.title('Cryptocurrency Price with Manipulation Detection')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True, alpha=0.3)

# Volume chart showing the same suspicious periods
plt.subplot(2, 1, 2)
plt.plot(results['date'], results['volume'], 'g-', linewidth=2, label='Volume')
suspicious_volumes = results[results['suspicious']]['volume']
plt.scatter(suspicious_dates, suspicious_volumes, color='red', s=100, label='Suspicious Activity', zorder=5)
plt.title('Trading Volume')
plt.ylabel('Volume')
plt.xlabel('Date')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Finally, my summary of what the algorithm discovered
total_days = len(results)
suspicious_days_count = len(suspicious_days)
print(f"Summary:")
print(f"Total days analyzed: {total_days}")
print(f"Suspicious days detected: {suspicious_days_count}")
print(f"Percentage of suspicious activity: {suspicious_days_count/total_days*100:.1f}%")

# This was a code I wrote in my free time just to give an idea of how these three libraries could be used together 
# Market Manipulation is a very common phenomenon, so this code gives it a graphical representation to make it easy to understand
#Hope u enjoyed!!