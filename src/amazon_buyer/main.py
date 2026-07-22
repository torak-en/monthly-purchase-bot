from amazon_buyer.amazon import AmazonSetup
from amazon_buyer.browser import BrowserManager
from amazon_buyer.checkout import CheckoutManager
from amazon_buyer.config import Config
from amazon_buyer.exceptions import ConfigurationError
from amazon_buyer.logger import configure_logger
from amazon_buyer.product import ProductManager


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

        page = browser.get_page()

        amazon = AmazonSetup(page, browser, config)

        if not amazon.login():
            logger.error("Amazon authentication failed")
            return

        logger.info("Amazon authentication successful")

        product = ProductManager(page, config)

        if not product.open_product():
            logger.error("Could not open product page")
            return

        logger.info("Product page ready")

        product_name = product.get_product_name()

        if product_name is None:
            logger.error("Could not retrieve product name")
            return

        product_price = product.get_product_price()

        if product_price is None:
            logger.error("Could not retrieve product price")
            return

        if not product.check_price(product_price):
            logger.info("Price too high. No action required.")
            return

        logger.info("Price acceptable")

        checkout = CheckoutManager(page, config)

        if not checkout.add_to_basket():
            logger.error("Failed to add product to basket")
            return

        basket_total = checkout.get_basket_total()

        if basket_total is None:
            logger.error("Could not retrieve basket total")
            return

        if not checkout.verify_basket_total(basket_total, product_price):
            logger.error("Basket total verification failed")
            return

        logger.info("Basket verification successful")

        if not checkout.proceed_to_checkout():
            logger.error("Could not proceed to checkout")
            return

        logger.info("Checkout page ready")

        if not checkout.purchase():
            logger.error("Purchase failed")
            return

        logger.info("Purchase workflow completed successfully")

        input("Press any key to continue...")

    finally:

        browser.close()


if __name__ == "__main__":
    main()