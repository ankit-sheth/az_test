import os
import sys
import logging
import uuid

from logging.handlers import RotatingFileHandler

from src.config import log_config

# This code is mainly copied from the python logging module, with minor modifications

# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame.
#
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

## class with custom filter and format
class CustomLogger(logging.Logger):
    def __init__(self,  request_trace_id=None):

        self.request_trace_id = request_trace_id
        self.extra_info = {"extra": None}
        ##self.log_formatter(logging)
        self.logger = self.setup_logger(log_config.LOGGER_NAME, log_config.LOG_FILE_PATH, log_config.LOG_LEVEL)

    def setup_logger(self, name, log_file, level=log_config.LOG_LEVEL):
        """
        Sets up a logger with a rotating file handler and a custom format.

        Args:
            name (str): The name of the logger.
            log_file (str): The file path for the log file.
            level: The logging level (default is INFO).

        Returns:
            logging.Logger: Configured logger object.
        """
        # Define a custom formatter including file, function, and line details
        formatter = logging.Formatter(
            '%(request_trace_id)s | %(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
        )

        # logging.basicConfig(level=level, format="'%(request_trace_id)s | %(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'")

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if logger.hasHandlers():
            logger.handlers.clear()

        ## below line must required to disable parent logger logs, otherwise it prints two times
        logger.propagate = False

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=log_config.LOG_FILE_BYTES,
            backupCount=log_config.LOG_BACKUP_COUNT,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.logger.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)

    # Add other convenience methods

    def log(self, level, msg, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.logger.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None):

        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        # Add wrapping functionality here.
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller throws an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        extra_info = extra if extra is not None else self.extra_info

        d = {'request_trace_id': self.request_trace_id}

        if extra_info is not None:
            extra_info.update(d)
        else:
            extra_info = d

        record = self.logger.makeRecord(
            self.logger.name, level, fn, lno, msg, args, exc_info, func, extra=extra_info)

        self.logger.handle(record)

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = logging.currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.logger.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARN'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.logger.isEnabledFor(logging.WARN):
            self._log(logging.WARN, msg, args, **kwargs)

    def get_trace_id(self):
        return self.request_trace_id