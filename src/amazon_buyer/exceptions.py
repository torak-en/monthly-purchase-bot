class ApplicationError(Exception):
    pass

class ConfigurationError(ApplicationError):

    def __init__(self, errors):

        self.errors = errors

        error_message = self.format_message()

        super().__init__(error_message)


    def format_message(self):

        error_message = "Configuration errors found:\n"

        for error in self.errors:
            error_message += f"{error}\n"

        return error_message


class BrowserError(ApplicationError):
    pass


class AmazonError(ApplicationError):
    pass


class ProductError(ApplicationError):
    pass


class CheckoutError(ApplicationError):
    pass