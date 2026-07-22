from amazon_buyer.browser import BrowserManager
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

    browser = BrowserManager(False)

    try:

        browser.start()

        logger.info("Browser started successfully")

        page = browser.get_page()

        page.goto(config.product_url)

        input("Press Enter to close the browser")

    finally:

        browser.close()


if __name__ == "__main__":
    main()