import logging
import os

from playwright.sync_api import sync_playwright
from amazon_buyer.exceptions import BrowserError

logger = logging.getLogger("amazon_logger")


class BrowserManager:

    def __init__(self, headless):
        
        self.headless = headless

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        self.session_directory = "sessions"
        self.session_file = os.path.join(self.session_directory, "amazon_session.json")
        
        os.makedirs(self.session_directory, exist_ok=True)

        logger.debug(f"BrowserManager created (headless={headless})")

        logger.debug(f"Session file: {self.session_file}")


    def start(self):
        
        logger.info("Starting Playwright")

        try:
            self.playwright = sync_playwright().start()

            logger.info("Launching Chromium")

            self.browser = self.playwright.chromium.launch(headless=self.headless)

        except Exception as error:

            raise BrowserError(f"Failed to start browser: {error}")

        logger.info("Creating browser context")

        try:

            if os.path.exists(self.session_file):

                logger.info("Existing session found")

                self.context = self.browser.new_context(storage_state=self.session_file)

            else:

                logger.info("No existing session found")

                self.context = self.browser.new_context()

            logger.info("Creating browser page")

            self.page = self.context.new_page()

        except Exception as error:

            raise BrowserError(f"Failed to create browser context: {error}")

        logger.info("Browser started successfully")


    def get_page(self):

        if not self.page:

            raise BrowserError("Browser page has not been created")

        return self.page


    def save_session(self):

        if not self.context:

            raise BrowserError("Cannot save session. Browser context does not exist.")

        logger.info("Saving session")

        try:

            self.context.storage_state(path=self.session_file)

        except Exception as error:

            raise BrowserError(f"Failed to save browser session: {error}")

        logger.info("Browser session saved successfully")


    def close(self):

        logger.info("Closing browser")

        try:

            if self.page:

                logger.debug("Closing page")
                self.page.close()
                self.page = None

            if self.context:

                logger.debug("Closing browser context")
                self.context.close()
                self.page = None

            if self.browser:

                logger.debug("Closing browser")
                self.browser.close()
                self.browser = None

            if self.playwright:

                logger.debug("Stopping Playwright")
                self.playwright.stop()
                self.playwright = None

        except Exception as error:

            raise BrowserError(f"Failed to close browser: {error}")

        logger.info("Browser closed successfully")