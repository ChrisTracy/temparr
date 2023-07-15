import os
import logging
import time
from pyarr import RadarrAPI
from datetime import datetime

#function to check if root folder exists
def check_root_folder(root_folder):
    root_folders = radarr.get_root_folder()
    exist = 0
    for folder in root_folders:
        if root_folder in folder['path']:
            exist = 1
    if exist == 1: return True
    else: return False

#function to change days to seconds
def days_to_seconds(number_of_days):
    days = float(number_of_days)
    return int(days * 24 * 60 * 60)

#function to check if file can be deleted based on time
def validate_timespan_for_delete(added, current_time, keep_time):
    unified_added = added.split('T', 1)[0]  # Formatting of date
    date_added_to_datetime = datetime.strptime(unified_added, '%Y-%m-%d')  # More formatting of date
    date_added_in_seconds = int(date_added_to_datetime.timestamp())
    saved_time = current_time - date_added_in_seconds  # Seconds since download
    if saved_time >= keep_time:
        return True  # Checks if movie has been saved longer than wanted
    else:
        return False

# Set logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set host URL, API key, temporary folder, keep time, and recurrence
host_url = os.environ.get('HOST_URL')
api_key = os.environ.get('API_KEY')
temporary_folder = os.environ.get('TEMPORARY_FOLDER')
keep_time = os.environ.get('KEEP_TIME')
recurrence = int(os.environ.get('RECURRENCE'))

#add slash to tempfolder if it does not exist
if "/" not in temporary_folder:
    logging.info("/ not added to folder. adding / to prevent errors.")
    temporary_folder = "/"+temporary_folder

#convert  keep time to seconds
keep_time = days_to_seconds(float(keep_time))
logging.info(f"Converting keep_time to seconds. Data will be deleted {keep_time} seconds after creation!")

# Instantiate RadarrAPI object
logging.info("Connecting to Radarr")
try:
    radarr = RadarrAPI(host_url, api_key)
except:
    logging.error("Not able to connect to Radarr!")
    exit()

#check if the root folder exists
logging.info("Ensuring root folder exists")
root_folder_exists = check_root_folder(temporary_folder)
if root_folder_exists == False:
    logging.error(f"Root Folder: {temporary_folder} does not exist!")
    exit()

#start loop based on reccurence time
logging.info("All checks passed. Starting server!")
while True:
    # Get movies
    movies = radarr.get_movie()

    #get time
    current_time = int(datetime.today().timestamp())  # Now in seconds
     
    #loop movies and remove if criteria are met
    for movie in movies:
        folder = movie['folderName']
        if temporary_folder in folder and 'movieFile' in movie:
            movie_file = movie['movieFile']
            added = movie_file['dateAdded']
            delete = validate_timespan_for_delete(added, current_time, keep_time)
            if delete:
                movie_title = movie['title']
                logging.info(f'Deleting {movie_title}')
                radarr.del_movie(movie['id'], True)

    # Wait for the next recurrence
    logging.info(f"Waiting for {recurrence} minutes until the next run...")
    time.sleep(recurrence * 60)