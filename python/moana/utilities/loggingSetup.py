import logging


formatter = logging.Formatter("%(levelname)-9s [%(asctime)s]: %(message)s\n",
                                            "%H:%M:%S")

del logging.root.handlers[:]

logger = logging.getLogger('moana')
logger.propigate = False
logger.setLevel(logging.DEBUG)
logger.handlers = []

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logger.propigate = False
