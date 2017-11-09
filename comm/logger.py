import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')

# add formatter to sh
sh.setFormatter(formatter)

# add sh to logger
logger.addHandler(sh)

logger.debug('debug message')