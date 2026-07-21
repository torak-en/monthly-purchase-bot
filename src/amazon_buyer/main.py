from amazon_buyer.config import Config
from amazon_buyer.exceptions import ConfigurationError
from amazon_buyer.logger import configure_logger

def main():

    logger = configure_logger()

    logger.info("Monthly Purchase Bot Starting...")

    try:
        config = Config()

    except ConfigurationError as error:
        logger.error(error)
        return

    logger.info("Configuration loaded successfully")


if __name__ == "__main__":
    main()