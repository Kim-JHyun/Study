from tasks.reference.func import init_logger
#from tasks.task2.scrap import scrap_items
from tasks.task3.save import save_data
from tasks.task4.win32hwp import init
from tasks.task2.scrapadd import scrap_items
import os

# selenium == 4.11.2/ python == 3.9.0

if __name__ == '__main__':
    main_path = os.path.dirname(__file__)
    LOG_PATH = main_path + r'\log'
    
    logger = init_logger(LOG_PATH)
    logger.info('Start Process')
    data = scrap_items(logger)
    save_data(logger=logger, data=data)
    init(logger, data)
    logger.info('process complete')
