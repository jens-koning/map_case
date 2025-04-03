#### Visualizing charger locations in R ####
rm(list=ls())

# Load necessary libraries
library(sf)
library(ggplot2)
library(dplyr)
library(rnaturalearth)
library(rnaturalearthdata)
library(viridis)

# Load the CSV data
charger_info_df <- read.csv('charger_info.csv')

# Group by station name and get the first entry for each station
grouped_df <- charger_info_df %>%
  group_by(station_name) %>%
  slice(1) %>%
  ungroup()
# Create an sf object
gdf <- st_as_sf(grouped_df, coords = c("longitude", "latitude"), crs = 4326)

# Load world map data
world <- ne_countries(scale = "medium", returnclass = "sf")

# Filter for specific countries
selected_countries <- world %>%
  filter(name %in% c('Norway', 'Sweden', 'Denmark', 'Finland', 'Germany'))

# Very simple plot of charger locations
p1 <- ggplot(data = selected_countries) +
  geom_sf() +
  geom_sf(data = gdf, color = 'red', size = 1) +
  coord_sf(xlim = c(3, 27), ylim = c(47, 71), expand = FALSE) +
  ggtitle('Charger Network Eviny') +
  theme_minimal()
ggsave('charger_locations.png', p1, width = 10, height = 10)

  # Load GADM data for Norway, can't do all due to time restrictions 
gadm_data_norway <- st_read(dsn = "gadm41_NOR_2.json", stringsAsFactors = FALSE)

# Transform the CRS of gadm_data_norway to match the coordinates of gdf
gadm_data_norway <- st_transform(gadm_data_norway, crs = st_crs(gdf))

# Attach the coordinates to a district shape for Norway (GADM level 2)
gdf$district <- st_join(gdf, gadm_data_norway, join = st_intersects)$NAME_2

# Count the number of stations per district in Norway
district_counts_norway <- gdf %>%
  group_by(district) %>%
  summarise(station_count = n_distinct(station_id))

# Merge the counts with the GADM data for Norway
gadm_data_norway <- st_join(gadm_data_norway, district_counts_norway, join = st_intersects)

gadm_data_norway$station_count[is.na(gadm_data_norway$station_count)] <- 0

# Charger station density by district
p2 <- ggplot(data = gadm_data_norway) +
  geom_sf(aes(fill = log1p(station_count))) +
  scale_fill_viridis_c(option = "viridis", direction = -1, name = "Number of Stations") +
  ggtitle('Eviny Charger Network Density in Norway (by District)') +
  theme_minimal()
ggsave('charger_density_district_nor.png', p2, width = 10, height = 10)

# create new .csv with district and station count
write.csv(gadm_data_norway, 'charger_density_district_nor.csv', row.names = FALSE)
