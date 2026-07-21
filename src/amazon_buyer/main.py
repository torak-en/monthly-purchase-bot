from amazon_buyer.config import Config
from amazon_buyer.exceptions import ConfigurationError

def main():
    print("Monthly Purchase Bot Starting...")

    try:
        config = Config()

    except ConfigurationError as error:
        print(error)
        return

    print("Configuration loaded successfully")


if __name__ == "__main__":
    main()