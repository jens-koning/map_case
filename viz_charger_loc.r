#### Let's map out some charger spots in R! ####
rm(list=ls())

# Load up the libraries we need
library(sf)
library(ggplot2)
library(dplyr)
library(rnaturalearth)
library(rnaturalearthdata)
library(viridis)

# Grab the data from our CSV
charger_info_df <- read.csv('charger_info.csv')

# Group by station name and snag the first entry for each
grouped_df <- charger_info_df %>%
  group_by(station_name) %>%
  slice(1) %>%
  ungroup()
# Turn it into an sf object
gdf <- st_as_sf(grouped_df, coords = c("longitude", "latitude"), crs = 4326)

# Get the world map data
world <- ne_countries(scale = "medium", returnclass = "sf")

# Pick out the countries we're interested in
selected_countries <- world %>%
  filter(name %in% c('Norway', 'Sweden', 'Denmark', 'Finland', 'Germany'))

# Quick and simple plot of charger locations
p1 <- ggplot(data = selected_countries) +
  geom_sf() +
  geom_sf(data = gdf, color = 'red', size = 1) +
  coord_sf(xlim = c(3, 27), ylim = c(47, 71), expand = FALSE) +
  ggtitle('Charger Network Eviny') +
  theme_minimal()
ggsave('charger_locations.png', p1, width = 10, height = 10)

# Load up the GADM data for Norway, can't do all due to time crunch
gadm_data_norway <- st_read(dsn = "gadm41_NOR_2.json", stringsAsFactors = FALSE)

# Make sure the CRS of gadm_data_norway matches gdf
gadm_data_norway <- st_transform(gadm_data_norway, crs = st_crs(gdf))

# Match up the coordinates with district shapes for Norway (GADM level 2)
gdf$district <- st_join(gdf, gadm_data_norway, join = st_intersects)$NAME_2

# Count how many stations are in each district in Norway
district_counts_norway <- gdf %>%
  group_by(district) %>%
  summarise(station_count = n_distinct(station_id))

# Merge those counts with the GADM data for Norway
gadm_data_norway <- st_join(gadm_data_norway, district_counts_norway, join = st_intersects)

gadm_data_norway$station_count[is.na(gadm_data_norway$station_count)] <- 0

# Plot the charger station density by district
p2 <- ggplot(data = gadm_data_norway) +
  geom_sf(aes(fill = log1p(station_count))) +
  scale_fill_viridis_c(option = "viridis", direction = -1, name = "Number of Stations") +
  ggtitle('Eviny Charger Network Density in Norway (by District)') +
  theme_minimal()
ggsave('charger_density_district_nor.png', p2, width = 10, height = 10)

# Save a new .csv with district and station count
write.csv(gadm_data_norway, 'charger_density_district_nor.csv', row.names = FALSE)
