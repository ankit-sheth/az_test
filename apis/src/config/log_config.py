import logging

# RotatingLogger
LOGGER_NAME = "allianz_logger"
LOG_BACKUP_COUNT = 5
LOG_FILE_BYTES = 5 * 1024 * 1024
LOG_FILE_PATH = "./logs/log"
LOG_LEVEL = logging.DEBUG