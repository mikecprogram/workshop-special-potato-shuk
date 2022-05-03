import logging as logger


class Logger:

    @staticmethod
    def debug(self, message):
        logger.debug(message)

    @staticmethod
    def event(self, message):
        logger.info(message)

    @staticmethod
    def warning(self, message):
        logger.warning(message)

    @staticmethod
    def error(self, message):
        logger.error(message)

    @staticmethod
    def critical(self, message):
        logger.critical(message)
