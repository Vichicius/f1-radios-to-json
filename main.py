import logging
import logging.handlers
import os

import requests
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# TODO: get current_driver_numbers automatically
current_driver_numbers = range(1,100)

def fetch_all():
    response = requests.get('https://api.openf1.org/v1/team_radio')
    if response.status_code == 200:
        data = response.json()

        with open(f'data/all-radios.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f'Saved all radios on "data/all-radios.json"')

        return data

def fetch_from_local():
    with open(f'data/all-radios.json', 'r') as local_data:
        data = json.load(local_data)
        return data
        
def split_radios_per_driver(data):
    for driver_number in current_driver_numbers:
        driver_data = filter_by_driver_number(data, driver_number)
        if driver_data != []:
            save_driver_data(driver_data, driver_number)
    
def filter_by_driver_number(data, driver_number):
    return [entry for entry in data if entry['driver_number'] == driver_number]

def save_driver_data(driver_data, driver_number):
    # Create driver directory if it doesn't exist
    os.makedirs('data/driver', exist_ok=True)

    # Process data to add meeting and session names
    processed_data = process_radio_data(driver_data)

    # Save all driver data
    with open(f'data/driver/{driver_number}.json', 'w') as json_file:
        json.dump(driver_data, json_file, indent=4)
        logger.info(f'Saved all radio data from driver nº {driver_number}')

def process_radio_data(radio_data):
    for entry in radio_data:
        meeting_name, session_name = extract_session_info(entry['recording_url'])
        entry['meeting_name'] = meeting_name
        entry['session_name'] = session_name
        entry['meeting_year'] = entry['date'][:4]  # Get the first 4 characters of the date string

    return radio_data

def extract_session_info(url):
    try:
        # Split URL to get relevant parts
        parts = url.split('/')
        
        gp_part = parts[5].split('_')
        meeting_name = ' '.join(gp_part[1:])
        
        session_part = parts[6].split('_')
        session_name = ' '.join(session_part[1:])
        
        return meeting_name, session_name
    except:
        return "Unknown GP", "Unknown Session"
    
def main():
    # data = fetch_all()
    data = fetch_from_local() # Use to test without making API calls
    split_radios_per_driver(data)


if __name__ == "__main__":
    main()

