import logging
import drawlib._const as const

logger = logging.getLogger(const.LIB_NAME)

# set default level
logger.setLevel(logging.INFO)

# set default log format
formatter = logging.Formatter('%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
