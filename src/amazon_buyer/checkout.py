import logging

from amazon_buyer.exceptions import CheckoutError

logger = logging.getLogger("amazon_logger")


class CheckoutManager:

    def __init__(self, page, config):

        self.page = page
        self.config = config


    def add_to_basket(self):

        logger.info("Adding product to basket")

        try:

            add_button = self.page.locator('#add-to-cart-button')

            add_button.wait_for(state="visible", timeout=10000)

            logger.debug("Adding product to basket")

            add_button.click()

        except Exception as error:

            raise CheckoutError(f"failed to add product to basket: {error}")

        logger.info("Add to basket button clicked")

        return True


    def get_basket_total(self):

        logger.info("Verifying basket total")

        try:

            whole = self.page.locator(".a-price-whole").first.inner_text()

            fraction = self.page.locator(".a-price-fraction").first.inner_text()

        except Exception as error:

            raise CheckoutError(f"Failed to verify basket total: {error}")

        price_text = (whole.replace(".", "").strip() + "." + fraction.strip())

        try:

            basket_total = float(price_text)

        except ValueError:

            raise CheckoutError(f"Invalid basket total format: {price_text}")

        logger.info(f"Basket total: {basket_total:.2f}")

        return basket_total

    def verify_basket_total(self, basket_total, expected_price):

        logger.info("Verifying basket total")

        if abs(basket_total - expected_price) > 0.01:

            logger.error(f"Basket total mismatch. Expected £{expected_price:.2f}, got £{basket_total:.2f}")

            return False

        logger.info("Basket total matches product price")

        return True

    def proceed_to_checkout(self):

        logger.info("Proceeding to checkout")

        try:

            checkout_button = self.page.locator("input[name='proceedToRetailCheckout']")

            checkout_button.wait_for(state="visible", timeout=10000)

            checkout_button.click()

            self.page.wait_for_load_state("domcontentloaded", timeout=30000)

        except Exception as error:

            raise CheckoutError(f"Failed to proceed to checkout: {error}")

        logger.info("Checkout page loaded")

        return True

    def purchase(self):

        logger.info("Preparing to purchase")

        try:

            purchase_button = self.page.locator("#placeOrder:not([disabled])").first

            purchase_button.wait_for(state="visible", timeout=10000)

        except Exception as error:

            raise CheckoutError(f"Could not locate purchase button: {error}")

        logger.info("Purchase button located")

        if self.config.dry_run:

            logger.warning("Dry run enabled - purchase button found but not clicked")

            return True

        logger.warning("Submitting order")

        purchase_button.click()

        logger.warning("Order submitted")

        return True
