import logging

import logzero

from manifester.settings import settings


def setup_logzero(level="info", path="logs/manifester.log", silent=True):
    log_fmt = "%(color)s[%(levelname)s %(asctime)s]%(end_color)s %(message)s"
    debug_fmt = (
        "%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]"
        "%(end_color)s %(message)s"
    )
    log_level = getattr(logging, level.upper(), logging.INFO)
    # formatter for terminal
    formatter = logzero.LogFormatter(
        fmt=debug_fmt if log_level is logging.DEBUG else log_fmt
    )
    logzero.setup_default_logger(formatter=formatter, disableStderrLogger=silent)
    logzero.loglevel(log_level)
    # formatter for file
    formatter = logzero.LogFormatter(
        fmt=debug_fmt if log_level is logging.DEBUG else log_fmt, color=False
    )
    logzero.logfile(
        path, loglevel=log_level, maxBytes=1e9, backupCount=3, formatter=formatter
    )


setup_logzero(level=settings.get("log_level", "info"))
