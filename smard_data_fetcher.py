import time
import pandas as pd
from datetime import datetime
from deutschland import smard
from deutschland.smard.api import default_api
from pprint import pprint

# Define API Configuration
configuration = smard.Configuration(host="https://www.smard.de/app")

# Define parameters
filters = [1225, 4067]  # Stromerzeugung: Wind Offshore (1225) & Wind Onshore (4067)
region = "DE"
resolution = "hour"

# Function to fetch and organize data
def fetch_and_organize_data():
    with smard.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        
        all_columns = []  # List to store combined results
        
        for filter_value in filters:
            print(f"Fetching data for filter: {filter_value}")
            all_timestamps = []  # List to store combined results
            
            # Fetch timestamps
            try:
                api_response = api_instance.chart_data_filter_region_index_resolution_json_get(filter_value, region, resolution)
                timestamps = api_response.get('timestamps')
                
                if not timestamps:
                    print(f"No timestamps found for filter: {filter_value}")
                    continue
                
                for timestamp in timestamps[1:-1]:  # Skip the first and last timestamp
                    try:
                        api_response = api_instance.chart_data_filter_region_filter_copy_region_copy_resolution_timestamp_json_get(
                            filter=filter_value, filter_copy=filter_value, 
                            region=region, region_copy=region, 
                            resolution=resolution, timestamp=timestamp
                        )
                        
                        # Create DataFrame from the response
                        values_df = pd.DataFrame(
                            api_response.get("series"),
                            columns=["timestamps", filter_value]
                        )
                        
                        # Convert timestamps to datetime and set as index
                        values_df.index = pd.to_datetime(values_df["timestamps"], unit='ms')
                        values_df.drop("timestamps", axis=1, inplace=True)
                        
                        all_timestamps.append(values_df)
                    
                    except Exception as e:
                        print(f"Error fetching data for timestamp {timestamp}: {e}")
                        continue
                
                # Combine all timestamps for the current filter
                if all_timestamps:
                    time_df = pd.concat(all_timestamps, axis=0)
                    all_columns.append(time_df)
                else:
                    print(f"No data found for filter: {filter_value}")
            
            except Exception as e:
                print(f"Error fetching timestamps for filter {filter_value}: {e}")
                continue
        
        # Combine all filters into a single DataFrame
        if all_columns:
            all_df = pd.concat(all_columns, axis=1)
            return all_df
        else:
            print("No data fetched for any filter.")
            return None

# Save the DataFrame to a CSV file
def save_data_to_csv(df, filename="smard_data.csv"):
    if df is not None:
        df.to_csv(filename)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Main execution
if __name__ == "__main__":
    data_df = fetch_and_organize_data()
    save_data_to_csv(data_df)