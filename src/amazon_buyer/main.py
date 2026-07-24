from amazon_buyer.amazon import AmazonSetup
from amazon_buyer.browser import BrowserManager
from amazon_buyer.checkout import CheckoutManager
from amazon_buyer.config import Config
from amazon_buyer.exceptions import ApplicationError
from amazon_buyer.logger import configure_logger
from amazon_buyer.product import ProductManager


def main():

    logger = configure_logger()

    logger.info("Monthly Purchase Bot Starting...")

    try:
        config = Config()

        logger.info("Configuration loaded successfully")

        browser = BrowserManager(config.headless)

        try:

            browser.start()

            page = browser.get_page()

            amazon = AmazonSetup(page, browser, config)

            amazon.login()

            logger.info("Amazon authentication successful")

            product = ProductManager(page, config)

            product.open_product()

            logger.info("Product page ready")

            product.get_product_name()

            product_price = product.get_product_price()

            if not product.check_price(product_price):

                logger.info("Product exceeds maximum price. Purchase cancelled.")

                return

            logger.info("Price verification successful")

            checkout = CheckoutManager(page, config)

            checkout.add_to_basket()

            basket_total = checkout.get_basket_total()

            if not checkout.verify_basket_total(basket_total, product_price):

                logger.error("Basket verification failed")

                return

            logger.info("Basket verification successful")

            checkout.proceed_to_checkout()

            logger.info("Checkout page ready")

            checkout.purchase()

            logger.info("Purchase workflow completed successfully")

            input("Press any key to continue...")

        finally:

            browser.close()

    except ApplicationError as error:

        logger.error(error)


if __name__ == "__main__":
    main()