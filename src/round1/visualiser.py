import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

days = [0]

dfs = []
for day in days:
    df = pd.read_csv(f'data/round_1/prices_round_1_day_{day}.csv', sep=';')
    df['day'] = day
    dfs.append(df)
prices = pd.concat(dfs, ignore_index=True)
prices = prices[prices['mid_price'] > 0]

pepper = prices[prices['product'] == 'INTARIAN_PEPPER_ROOT'].reset_index(drop=True)
osmium = prices[prices['product'] == 'ASH_COATED_OSMIUM'].reset_index(drop=True)

fig, axes = plt.subplots(2, 1, figsize=(16, 10))
colors = {-2: 'blue', -1: 'orange', 0: 'green'}

for day in days:
    p = pepper[pepper['day'] == day]
    o = osmium[osmium['day'] == day]
    axes[0].plot(p['timestamp'], p['mid_price'], color=colors[day], linewidth=0.8, label=f'Day {day}')
    axes[1].plot(o['timestamp'], o['mid_price'], color=colors[day], linewidth=0.8, label=f'Day {day}')

# Pepper: add linear trend per day
for day in days:
    p = pepper[pepper['day'] == day]
    x = p['timestamp'].values
    y = p['mid_price'].values
    coeffs = np.polyfit(x, y, 1)
    axes[0].plot(x, np.polyval(coeffs, x), color=colors[day], linewidth=2, linestyle='--')


axes[1].axhline(10000, color='red', linewidth=1.5, linestyle='--', label='Fair value (10000)')
axes[1].fill_between(osmium[osmium['day']==0]['timestamp'], 9995, 10005, alpha=0.1, color='red', label='±5 band')

axes[0].set_title('INTARIAN_PEPPER_ROOT — Mid Price by Day (dashed = linear trend)', fontsize=12)
axes[0].set_ylabel('Price')
axes[0].set_xlabel('Timestamp')
axes[0].legend()
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))

axes[1].set_title('ASH_COATED_OSMIUM — Mid Price by Day', fontsize=12)
axes[1].set_ylabel('Price')
axes[1].set_xlabel('Timestamp')
axes[1].legend()
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))

plt.tight_layout()
plt.show()