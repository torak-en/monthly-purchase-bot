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
        logger.debug(f"BrowserManager created (headless={headless})")

        os.makedirs(self.session_directory, exist_ok=True)

        logger.debug(f"Session file: {self.session_file}")

    def start(self):
        
        logger.info("Starting Playwright")

        self.playwright = sync_playwright().start()

        logger.info("Launching Chromium")

        try:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        except Exception:
            raise BrowserError("Failed to start Browser")

        logger.info("Creating browser context")

        if os.path.exists(self.session_file):

            logger.info("Existing session found")

            self.context = self.browser.new_context(storage_state=self.session_file)

        else:

            logger.info("No existing session found")

            self.context = self.browser.new_context()

        logger.info("Creating browser page")

        self.page = self.context.new_page()

        logger.info("Browser started successfully")

    def get_page(self):

        if not self.page:
            raise BrowserError("Browser has not been started")

        return self.page

    def close(self):

        logger.info("Closing browser")

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

        logger.info("Browser closed successfully")

    def save_session(self):

        if not self.context:
            logger.error("Cannot save session. Browser context does not exist.")
            return

        logger.info("Saving session")

        self.context.storage_state(path=self.session_file)

        logger.info("Browser session saved successfully")
