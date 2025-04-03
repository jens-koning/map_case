# remove all objects from the environment
rm(list = ls())

# load libraries
library(httr)
library(jsonlite)
library(dplyr)
library(lubridate)

# Fetch data from the API
fetch_charging_data <- function() {
  api_url <- "https://charging.eviny.no/api/map/chargingStations"
  response <- GET(api_url)
  
  if (http_status(response)$category == "Success") {
    data <- content(response, "text", encoding = "UTF-8")
    return(fromJSON(data))
  } else {
    stop("Failed to fetch data from API. Status code: ", status_code(response))
  }
}

# Main function
main <- function() {
  # Fetch the raw data
  raw_data <- fetch_charging_data()
  
  # Display the raw data structure
  cat("Raw Data Structure:\n")
  print(str(raw_data))
  
  # Display the first few records of raw data
  cat("\nSample of Raw Data:\n")
  print(head(raw_data))
  
  # Save the data to a JSON file
  json_data <- toJSON(raw_data, pretty = TRUE)
  write(json_data, "charging_stations_data.json")
  cat("\nData saved to charging_stations_data.json\n")
  
  # Return the raw data for further processing
  return(raw_data)
}

# Run the main function
result <- main()
