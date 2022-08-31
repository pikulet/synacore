import logging

class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def debug(self, *argv):
        logging.debug(' '.join([str(a) for a in argv]))

    def info(self, *argv):
        logging.info(' '.join([str(a) for a in argv]))
