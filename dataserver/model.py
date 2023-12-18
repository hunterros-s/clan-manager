import shared

import os
import json

# Get the directory path of the current Python file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define consistent path for the data file based on the shared clan tag
data_file_path = os.path.join(current_directory, f"data-{shared.clan_tag}.json")

def import_data():
    # Log an informational message indicating an attempt to load clan data from the file
    shared.log.info(f"Attempting to load clan data from {data_file_path}")
    try:
        # Try to open and read the JSON data from the specified file
        with open(data_file_path, 'r') as json_file:
            # Load the JSON data into the shared.clan_data dictionary
            shared.clan_data = json.load(json_file)
            # Log a message confirming successful loading of clan data
            shared.log.info(f"Clan data loaded from {data_file_path}")
            return True
    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        # Log a message indicating that the file wasn't found and clan data couldn't be loaded
        shared.log.info(f"File not found: {data_file_path}; clan data not loaded")
        # Log a message indicating initialization of an empty clan data object
        shared.log.info(f"Initializing empty clan data object")
        # Create an empty dictionary for clan_data as the file wasn't found
        shared.clan_data = {}
        return False

def save_data():
    # Log an informational message indicating an attempt to clan member data to the file
    shared.log.info(f"Attempting to write clan data to {data_file_path}")
    try:
        # Try to open the JSON file in write mode
        with open(data_file_path, 'w') as json_file:
            # Write the data from the dictionary to the file in a formatted JSON structure with indentation
            json.dump(shared.clan_data, json_file, indent=2)
            # Log a message confirming successful writing of member data to the file
            shared.log.info(f"Clan data successfully written to {data_file_path}")
    except Exception as e:
        # Handle any exceptions that might occur during the file write process
        # Log an error message including the specific exception that occurred
        shared.log.info(f"An error occurred while saving clan data: {e}")

