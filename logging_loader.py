import logging
from logging.handlers import TimedRotatingFileHandler


class Logger():
    """
    Logger object

    Attributes:
    logger -- Instance of Logger object
    """
    def __init__(self, name='main_logger', logname='log/server.log', level=logging.INFO):
        self.handler = TimedRotatingFileHandler(logname, when="midnight", interval=1, encoding='utf8')
        self.handler.suffix = "%Y%m%d"
        self.log_format = "%(asctime)s [%(lineno)d] - %(message)s"
        self.formatter = logging.Formatter(self.log_format)
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(self.handler)
