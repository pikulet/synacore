import logging

class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def debug(self, *argv):
        logging.debug(' '.join([str(a) for a in argv]))
