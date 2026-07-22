import logging
from plistlib import load

logger = logging.getLogger("amazon_logger")


class AmazonSetup:

    def __init__(self, page, browser, config):

        self.page = page
        self.browser = browser
        self.config = config


    def is_logged_in(self, check_page=True):

        logger.info("Checking Amazon login status")

        try:
            if check_page:
                self.page.goto(
                    "https://www.amazon.co.uk/gp/your-account/order-history",timeout=30000)

                self.page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=30000
                )

        except Exception as error:
            logger.error(
                f"Failed checking login status: {error}"
            )

            return False


        current_url = self.page.url

        try:
            title = self.page.title()

        except Exception:
            title = ""


        logger.debug(
            f"Current URL: {current_url}"
        )

        logger.debug(
            f"Page title: {title}"
        )


        if (
            "/ap/signin" in current_url
            or "Amazon Sign-In" in title
        ):

            logger.info(
                "Amazon login page detected"
            )

            return False


        logger.info(
            "User appears to be logged in"
        )

        return True


    def login(self):

        if self.is_logged_in():

            logger.info(
                "Already logged in"
            )

            return True


        logger.info(
            "Manual login required"
        )


        input(
            "Please log into Amazon manually, then press Enter..."
        )


        if not self.is_logged_in():

            logger.error(
                "Login verification failed"
            )

            return False


        self.browser.save_session()


        logger.info(
            "Login successful"
        )

        return True
        