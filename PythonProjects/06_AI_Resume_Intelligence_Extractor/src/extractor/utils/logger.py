"""
LoggerFactory
-------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Description: Configurable logging utility for debug and production modes.
Date: October 25, 2025

Usage:
    from extractor.utils.logger import LoggerFactory
    logger = LoggerFactory(debug=True).get_logger("ResumeParser")
"""

import logging

class LoggerFactory:
    def __init__(self, debug=False):
        """
        Initialize the logger factory.

        Args:
            debug (bool): If True, sets logging level to DEBUG.
        """
        self.debug = debug

    def get_logger(self, name="ResumeExtractor"):
        """
        Returns a configured logger instance.

        Args:
            name (str): Logger name.

        Returns:
            logging.Logger: Configured logger.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            # formatter = logging.Formatter("[%(levelname)s] %(message)s")
            # [Corrected Line 42]
            formatter = logging.Formatter("[%(levelname)s] (%(filename)s:%(lineno)d) %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        return logger
