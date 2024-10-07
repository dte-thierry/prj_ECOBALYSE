""" ETL to retrieve data from Ecobalyse API """ 

import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')

if __name__ == '__main__':
    start = time.time()
    # retrieve data

    

    end = time.time()
    runtime = end - start
    logger.info(f'----- ETL took {runtime:.3f} seconds to run -----')
