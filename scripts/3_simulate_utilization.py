#### Let's simulate charger use over a day! ####
#remove temp objects
for v in dir(): del globals()[v]

# Bring in the necessary tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Grab the data from our CSV
charger_info_df = pd.read_csv('charger_info.csv')

# Time to simulate how busy the chargers get over 24 hours
np.random.seed(42)  # Keeping it consistent
hours = range(24)
utilization = []

for hour in hours:
    if hour == 9 or hour == 19:
        # Busy times
        utilization.append(np.random.uniform(0.5, 0.8, len(charger_info_df)))
    else:
        # Not-so-busy times
        utilization.append(np.random.uniform(0.1, 0.5, len(charger_info_df)))

# Pick 10 random chargers to focus on
selected_chargers = np.random.choice(charger_info_df['charger_id'], size=10, replace=False)

# Turn our utilization data into a DataFrame for these chargers
utilization_df = pd.DataFrame(utilization, columns=charger_info_df['charger_id'])
utilization_df = utilization_df[selected_chargers]
utilization_df['hour'] = hours

# Add the connection type info to our DataFrame
utilization_df = utilization_df.melt(id_vars=['hour'], var_name='charger_id', value_name='utilization')
utilization_df = utilization_df.merge(charger_info_df[['charger_id', 'connection_type']], on='charger_id', how='left')

# Save our simulated data to a new CSV
utilization_df.to_csv('charger_utilization.csv', index=False)

# Let's make a plot to see how utilization changes over time for these 10 chargers
sample_connection_types = utilization_df['connection_type'].unique()[:3]
sample_data = utilization_df[utilization_df['connection_type'].isin(sample_connection_types)]

plt.figure(figsize=(12, 6))
for connection_type in sample_connection_types:
    connection_data = sample_data[sample_data['connection_type'] == connection_type]
    plt.plot(connection_data['hour'], connection_data['utilization'], label=f'Connection Type {connection_type}')

plt.xlabel('Hour of the Day')
plt.ylabel('Utilization')
plt.title('Charger Utilization Over 24 Hours by Connection Type')
plt.legend()
plt.grid(True)
plt.savefig('charger_utilization_over_time.png')
plt.show()

# Make a heatmap of the utilization rate by the hour:)  

# Utilization rate by hour for all connection types
hourly_utilization = utilization_df.groupby(['hour', 'connection_type'])['utilization'].mean().unstack()

# Print the table
print("Utilization Rate by Hour for Each Connection Type:")
print(hourly_utilization)

# Export the table to a .png file with improved aesthetics using seaborn heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(hourly_utilization, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Utilization Rate'})
plt.title('Utilization Rate by Hour for Each Connection Type', fontsize=16, fontweight='bold')
plt.xlabel('Connection Type', fontsize=12)
plt.ylabel('Hour of the Day', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('utilization_rate_by_hour_heatmap.png')
plt.show()
