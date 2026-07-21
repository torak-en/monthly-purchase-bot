from email import message


class ConfigurationError(Exception):
    def __init__(self, errors):
        self.errors = errors

        error_message = self.format_message()

        super().__init__(error_message)

    def format_message(self):
        error_message = "Configuration errors found:\n"

        for error in self.errors:
            error_message += f"{error}\n"

        return error_message