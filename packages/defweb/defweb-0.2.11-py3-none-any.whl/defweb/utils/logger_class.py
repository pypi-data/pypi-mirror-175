"""
logger_class.py
================
"""
import logging

import colors


class HelperLogger(logging.Logger):
    """
    The HelperLogger is used by the application as its logging class and *extends* the default python
    logger.logging class.
    """

    level_map = {
        "debug": "magenta",
        "info": "white",
        "warning": "yellow",
        "error": "red",
        "critical": "red",
        "data": "green",
        "data_out": "orange",
    }

    def __init__(self, name, level=logging.NOTSET):

        super().__init__(name, level)

    def data(self, msg, socks_version, outgoing=False, *args, **kwargs):
        """
        Custom data logger, piggybacking the info method of python logger

        :param socks_version: Socks version that produced the data entry
        :type socks_version: str
        :param msg: Message to log
        :type msg: str
        """

        if not outgoing:
            msg = colors.color(
                f"[{socks_version}] {msg}", fg=HelperLogger.level_map["data"]
            )
        else:
            msg = colors.color(
                f"[{socks_version}] {msg}", fg=HelperLogger.level_map["data_out"]
            )

        return super(HelperLogger, self).info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Log ‘msg % args’ with severity ‘DEBUG’ and color *MAGENTA.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.debug(“Houston, we have a %s”, “thorny problem”, exc_info=1)

        :param msg: Message to log
        :type msg: str
        """

        msg = colors.color("[D] {}".format(msg), fg=HelperLogger.level_map["debug"])

        return super(HelperLogger, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log ‘msg % args’ with severity ‘INFO’ and color *WHITE*.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.info(“Houston, we have a %s”, “interesting problem”, exc_info=1)

        :param msg: Message to log
        :type msg: str
        """

        msg = colors.color("[+] {}".format(msg), fg=HelperLogger.level_map["info"])

        return super(HelperLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log ‘msg % args’ with severity ‘WARNING’ and color *YELLOW*.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.warning(“Houston, we have a %s”, “bit of a problem”, exc_info=1)

        :param msg: Message to log
        :type msg: str
        """

        msg = colors.color("[*] {}".format(msg), fg=HelperLogger.level_map["warning"])

        return super(HelperLogger, self).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log ‘msg % args’ with severity ‘ERROR’ and color *RED*.

        Store logged message to the database for dashboard alerting.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.error(“Houston, we have a %s”, “major problem”, exc_info=1)

        :param msg: Message to log
        :type msg: str
        """

        msg = colors.color("[!] {}".format(msg), fg=HelperLogger.level_map["error"])

        return super(HelperLogger, self).error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log ‘msg % args’ with severity ‘CRITICAL’ and color *RED*.

        Store logged message to the database for dashboard alerting.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.critical(“Houston, we have a %s”, “hell of a problem”, exc_info=1)

        :param msg: Message to log
        :type msg: str
        """

        msg = colors.color("[!!] {}".format(msg), fg=HelperLogger.level_map["critical"])

        return super(HelperLogger, self).critical(msg, *args, **kwargs)
