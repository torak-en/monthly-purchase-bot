import logging

from amazon_buyer.exceptions import ProductError

logger = logging.getLogger("amazon_logger")


class ProductManager:

    def __init__(self, page, config):

        self.page = page
        self.config = config

    def open_product(self):

        logger.info("Opening product page")

        try:

            self.page.goto(self.config.product_url, timeout=30000)

            self.page.wait_for_load_state("domcontentloaded", timeout=30000)

        except Exception as error:

            raise ProductError("Failed opening product page: {error}")


        current_url = self.page.url

        try:

            title = self.page.title()

        except Exception:

            title = ""

        logger.debug(f"Product URL: {current_url}")
        logger.debug(f"Product title: {title}")

        if "/ap/signin" in current_url or "Amazon Sign-In" in title:

            raise ProductError("Amazon login required")

        if "Page Not Found" in title or "Sorry" in title:

            raise ProductError("Product page not found")

        logger.info("Product page opened successfully")

        return True

    def get_product_name(self):

        logger.info("Getting product name")

        try:

            product_name = self.page.locator("#productTitle").first.inner_text()

        except Exception as error:

            raise ProductError(f"Failed getting product name: {error}")

        product_name = product_name.strip()

        logger.info(f"Product name: {product_name}")

        return product_name

    def get_product_price(self):

        logger.info("Getting product price")

        try:

            whole_price = self.page.locator(".a-price-whole").first.inner_text()

            fraction_price = self.page.locator(".a-price-fraction").first.inner_text()

        except Exception as error:

            raise ProductError("Failed getting product price: {error}")

        whole_price = whole_price.replace(".", "").strip()
        fraction_price = fraction_price.strip()

        price_text = f"{whole_price}.{fraction_price}"

        try:

            price = float(price_text)

        except ValueError:

            raise ProductError(f"Invalid price format: {price_text}")

        logger.info(f"Product price: £{price:.2f}")

        return price

    def check_price(self, price):

        logger.info("Checking product price")

        logger.debug(f"Current price: {price}")
        logger.debug(f"Max price: {self.config.max_price}")

        if price <= self.config.max_price:
            logger.info("Product is within price limit")

            return True

        logger.info(f"Product exceeds maximum price: {self.config.max_price}")

        return False