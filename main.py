import os
import logging
import config as conf
from controller.coreController import Core


logger = logging.getLogger(__name__)  
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

Core.exec(logger, 'https://blaze.com/pt/games/crash')
