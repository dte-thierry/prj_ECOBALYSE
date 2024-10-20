""" Retrieve data from Ecobalyse API """ 

import logging
import time
import os

# Define the logs directory with an absolute path
logs_dir = '/app/logs'

# Create logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
log_file_path = os.path.join(logs_dir, 'ecbl_extract.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

# Create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info("Logger is configured and ready to log.")
logger.info(f"Log file path: {log_file_path}")

if __name__ == '__main__':
    start = time.time()
    logger.info("Starting the Extract Process.")

    # Simulate data retrieval
    time.sleep(5)  # Simulate a delay

    end = time.time()
    runtime = end - start
    logger.info(f'----- Data retrieval took {runtime:.3f} seconds to run -----')

    # Check if the log file is created
    if os.path.exists(log_file_path):
        logger.info(f"Log file {log_file_path} created successfully.")
    else:
        logger.error(f"Failed to create log file {log_file_path}.")

    # Keep the container running for debugging
    time.sleep(20)