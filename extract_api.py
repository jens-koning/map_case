#### Extract data from API and save to csv ####
#remove temp objects
for v in dir(): del globals()[v]

# load libraries
import json
import pandas as pd
import requests

# Fetch data from the API
response = requests.get('https://charging.eviny.no/api/map/chargingStations')
data = response.json()

# Load JSON data
with open('charging_stations_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant information
charger_info = []

for station in data['chargingStations']:
    for connection_type, connections in station['connectionsTypes'].items():
        for conn in connections:
            charger_info.append({
                'station_id': station['id'],
                'station_name': station['name'],
                'connection_type': connection_type,
                'charger_id': conn['id'],
                'status': conn['status'],
                'effect': conn['effect'],
                'tariffDefinition': conn['tariffDefinition'],
                'latitude': station['location']['lat'],
                'longitude': station['location']['lng']
            })

# convert to pandas df 
charger_info_df = pd.DataFrame(charger_info)

# inspecting the data
print(charger_info_df.head())
print(charger_info_df.describe()) 
# there are 4222 rows/observations
print(charger_info_df.info())

# count columns with NA
print(charger_info_df.isna().sum()) 
# 0 missing values in columns - data 100% complete

# save to csv in working dir
charger_info_df.to_csv('charger_info.csv', index=False)
