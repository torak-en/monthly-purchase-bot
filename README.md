# Amazon Monthly Purchase Bot

A Python automation project that automates the monthly purchase of an Amazon product using Playwright browser automation.

## Overview

Amazon Monthly Purchase Bot is a Python automation project built with Playwright that automates the process of purchasing a recurring Amazon product. 

The application stores a Playwright browser session after a one-time manual login, verifies the product price against a configurable maximum, and supports a configurable dry-run mode for safe testing.

## Features

- Playwright browser automation
- Automatic detection of Amazon login status
- Product information scraping
- Configurable maximum price verification
- Dry-run mode for safe testing
- Comprehensive logging
- Environment variable configuration

## Tech Stack

- Python 3.13
- Playwright
- python-dotenv
- Python Logging
- Git

## How It Works

```text
Start
  |
  v
Load configuration
  |
  v
Load saved browser session
  |
  v
Logged in?
  |----------------No------------------|
  |                                    |
 Yes                                   v
  |                             Manual login
  |                                    |
  |                             Save session
  |                                    |
  +------------------------------------+
  |
  v
Open product page
  |
  v
Read product title & price
  |
  v
Price <= Max Price?
  |--------No------> Exit
  |
 Yes
  |
  v
Add to basket
  |
  v
Verify basket total
  |
  v
Proceed to checkout
  |
  v
Locate "Buy now" button
  |
  v
Dry run?
  |--------Yes-----> Stop safely
  |
 No
  |
  v
Purchase product
```

## Project Structure

### Repository Structure:

```text
monthly-purchase-bot/
│
├── src/
│   └── amazon_buyer/
│       ├── amazon.py
│       ├── browser.py
│       ├── checkout.py
│       ├── config.py
│       ├── exceptions.py
│       ├── logger.py
│       ├── main.py
│       └── product.py
│
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

### Generated Runtime Files:

```text
monthly-purchase-bot/
│
├── sessions/
│   └── amazon_session.json
│
└── logs/
    └── application.log
```


## Installation

```bash
git clone https://github.com/torak-en/monthly-purchase-bot.git

cd monthly-purchase-bot

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

playwright install chromium
```

## Configuration

Create a `.env` file in the project root using the following variables:

| Variable      | Description                                               |
|---------------|-----------------------------------------------------------|
| `PRODUCT_URL` | URL of the Amazon product to purchase                     |
| `MAX_PRICE`   | Maximum price you are willing to pay                      |
| `HEADLESS`    | `True` to run without a browser window, otherwise `False` |
| `DRY_RUN`     | `True` to stop before purchasing, otherwise `False`       |

Example:

```env
PRODUCT_URL=https://www.amazon.co.uk/...

MAX_PRICE=15.00

HEADLESS=False

DRY_RUN=True
```

## Usage

Run the application using:

```bash
python -m amazon_buyer.main
```

On the first run:

- The application detects that no browser session exists.
- Playwright opens Amazon and prompts you to log in manually.
- After a successful login, the browser session is saved.

On subsequent runs:

- The saved session is automatically loaded.
- No additional login is required unless the session expires.

## Dry-Run Mode

Dry-run mode allows the workflow to be tested safely.

When enabled, the application:

- Opens the product page
- Verifies the product price
- Adds the product to the basket
- Verifies the basket total
- Proceeds to the checkout page
- Locates the **Buy now** button
- Stops immediately before clicking it

This allows the complete workflow to be verified without placing an order.

## Example Output

*Application logs will be added here.*

## Current Limitations

- Amazon page structure may change.
- Built specifically for Amazon UK.
- Only supports purchasing a single product.
- Requires an existing Amazon account.
- CAPTCHA and additional verification are not handled automatically.

## Potential Future Improvements

- Discord notifications
- Multiple product support
- Retry logic for transient failures
- Email or SMS notifications
- Docker support
- Unit tests

## Disclaimer

This project was created for educational and portfolio purposes to demonstrate browser automation using Playwright.

Users are responsible for complying with Amazon's Terms of Service and should use automation responsibly.