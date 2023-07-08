import logging
from time import strftime

import watchtower


def configure_logging():
    # Create logger
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Configuring Logger to Use CloudWatch
    # cw_handler = watchtower.CloudWatchLogHandler(log_group="cruddur-backend-flask")

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    LOGGER.addHandler(console_handler)
    # LOGGER.addHandler(cw_handler)
    # LOGGER.info("Test CloudWatch Logs!")

    return LOGGER
