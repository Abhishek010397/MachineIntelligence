import logging
import re
from logging.handlers import TimedRotatingFileHandler
class Logging:
    logger = logging.getLogger(__name__)
    logFormatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    #logging.getLogger("pymodbus").setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)

    '''FILE HANDLER'''
    logname= "application_name.log"
    file_handler = logging.handlers.TimedRotatingFileHandler(filename=logname, when="midnight", interval=1)
    file_handler.suffix = "%Y%m%d"
    file_handler.setFormatter(logFormatter)
    file_handler.setLevel(logging.DEBUG)
    file_handler.extMatch = re.compile(r"^\d{8}$")

    '''STREAM HANDLER'''
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logFormatter)


    logger.addHandler(file_handler)
    logger.addHandler(console_handler)



