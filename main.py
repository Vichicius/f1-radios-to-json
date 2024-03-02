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


current_driver_numbers = [1, 2, 23, 24, 77, 11, 33, 44, 63, 4, 81, 20, 27, 16, 55, 14, 18, 3, 10, 22, 31]

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
        save_driver_data(driver_data, driver_number)
    
def filter_by_driver_number(data, driver_number):
    return [entry for entry in data if entry['driver_number'] == driver_number]

def save_driver_data(driver_data, driver_number):
    with open(f'data/radio-{driver_number}.json', 'w') as json_file:
        json.dump(driver_data, json_file, indent=4)
        logger.info(f'Saved radio data from driver nº {driver_number}')

def main():
    # data = fetch_all()
    data = fetch_from_local()
    split_radios_per_driver(data)


if __name__ == "__main__":
    main()

