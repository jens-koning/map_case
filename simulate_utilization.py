#### Simulate utilization over 24hrs ####
for v in dir(): del globals()[v]

# load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV data
charger_info_df = pd.read_csv('charger_info.csv')

# Simulate utilization over 24 hours
np.random.seed(42)  # For reproducibility
hours = range(24)
utilization = []

for hour in hours:
    if hour == 9 or hour == 19:
        # Peak utilization
        utilization.append(np.random.uniform(0.7, 1.0, len(charger_info_df)))
    else:
        # Off-peak utilization
        utilization.append(np.random.uniform(0.1, 0.5, len(charger_info_df)))

# Convert utilization to DataFrame
utilization_df = pd.DataFrame(utilization, columns=charger_info_df['charger_id'])
utilization_df['hour'] = hours

# Melt the DataFrame to long format
utilization_long_df = utilization_df.melt(id_vars=['hour'], var_name='charger_id', value_name='utilization')

# Save the simulated utilization data to CSV
utilization_long_df.to_csv('charger_utilization.csv', index=False)

# Plot utilization over time for a few chargers
sample_chargers = utilization_long_df['charger_id'].unique()[:5]
sample_data = utilization_long_df[utilization_long_df['charger_id'].isin(sample_chargers)]

plt.figure(figsize=(12, 6))
for charger_id in sample_chargers:
    charger_data = sample_data[sample_data['charger_id'] == charger_id]
    plt.plot(charger_data['hour'], charger_data['utilization'], label=f'Charger {charger_id}')

plt.xlabel('Hour of the Day')
plt.ylabel('Utilization')
plt.title('Charger Utilization Over 24 Hours')
plt.legend()
plt.grid(True)
plt.savefig('charger_utilization_over_time.png')
plt.show()
