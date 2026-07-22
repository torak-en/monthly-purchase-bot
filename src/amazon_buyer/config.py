import os

from dotenv import load_dotenv

from amazon_buyer.exceptions import ConfigurationError


class Config:
    def __init__(self):
        load_dotenv()
        
        self.amazon_email = os.getenv("AMAZON_EMAIL")
        self.amazon_password = os.getenv("AMAZON_PASSWORD")
        self.product_url = os.getenv("PRODUCT_URL")
        self.max_price = os.getenv("MAX_PRICE")
        self.headless = os.getenv("HEADLESS")
        self.dry_run = os.getenv("DRY_RUN")
        
        self.validate()

        self.max_price = float(self.max_price)

    def validate(self):
        errors = []
        
        errors.append(self.validate_amazon_email())
        errors.append(self.validate_amazon_password())
        errors.append(self.validate_product_url())
        errors.append(self.validate_max_price())
        errors.append(self.validate_headless())
        errors.append(self.validate_dry_run())
        
        errors = [error for error in errors if error is not None]

        if errors:
            raise ConfigurationError(errors)


    def validate_amazon_email(self):
        if not self.amazon_email:
            return "AMAZON_EMAIL is missing"
        
        if "@" not in self.amazon_email:
            return "AMAZON_EMAIL is not a valid email address"
        
        return None

    def validate_amazon_password(self):
        if not self.amazon_password:
            return "AMAZON_PASSWORD is missing"

        return None

    def validate_product_url(self):
        if not self.product_url:
            return "PRODUCT_URL is missing"

        if not self.product_url.startswith("https://"):
            return "PRODUCT_URL must start with https://"

        if "amazon.co.uk" not in self.product_url:
            return "PRODUCT_URL is not a valid amazon url"

        return None

    def validate_max_price(self):
        if not self.max_price:
            return "MAX_PRICE is missing"

        try:
            price = float(self.max_price)
        except ValueError:
            return "MAX_PRICE must be a number"

        if price <= 0:
            return "MAX_PRICE must be greater than zero"

        return None


    def validate_headless(self):
        if not self.headless:
            return "HEADLESS is missing"

        if self.headless.lower() not in ["true", "false"]:
            return "HEADLESS must be either True or False"

        return None

    def validate_dry_run(self):
        if not self.dry_run:
            return "DRY_RUN is missing"

        if self.dry_run.lower() not in ["true", "false"]:
            return "DRY_RUN must be either True or False"

        return None