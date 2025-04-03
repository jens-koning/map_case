#### Simulate utilization over 24hrs ####
import pandas as pd
import numpy as np

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
