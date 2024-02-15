"""
Module providing the core functions to the package.
It is a small project with one specific task.
"""
# pylint: disable=line-too-long
# pylint: disable=redefined-outer-name

import datetime
from os import getcwd
import time

from decimal import Decimal
from loguru import logger

import utils as u
import locators as loc
from argum import args


# DRIVER
def driver_init():
    """Webdriver initiation - browser settings"""
    chrome_options = u.webdriver.ChromeOptions()

    if args.nohead:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-extensions")
    driver = u.webdriver.Chrome(options=chrome_options, service=u.ChromeService(u.ChromeDriverManager().install()))

    driver.maximize_window()
    driver.get("https://www.max.co.il/")

    return driver


def driver():
    """Calling webdriver"""
    u.logger.info("initiating bot....")
    get_driver = driver_init()
    return get_driver


def close_driver(driver) -> None:
    """Closing webdriver"""
    driver.close()


# LOGIN
def max_login(driver, email: str, password: str) -> None:
    """
    Login to your MAX account.
    :param driver:
    :param email:
    :param password:
    :return:
    """

    # login
    tries = 0
    while tries < 2:
        try:
            u.WDW(driver, 5).until(u.EC.visibility_of_element_located(loc.max_loc['personal_zone'])).click()
            u.logger.info('clicked on personal zone')

            u.WDW(driver, 5).until(u.EC.visibility_of_element_located(loc.max_loc['login_with_password'])).click()

            u.logger.info("entering your email")
            email_input = u.WDW(driver, 5).until(u.EC.visibility_of_element_located(loc.max_loc['input_username']))
            email_input.send_keys(email)

            u.logger.info("entering your password")
            pass_input = u.WDW(driver, 5).until(u.EC.visibility_of_element_located(loc.max_loc['input_password']))
            pass_input.send_keys(password)

            u.logger.info("clicking on login to the site")
            u.WDW(driver, 5).until(u.EC.visibility_of_element_located(loc.max_loc['login_button_login'])).click()

            time.sleep(3)
            validate_max_login(driver)
            break

        except u.TimeoutException:
            u.logger.error("An error related to the website page has occurred, trying one more time...")
            tries += 1


def validate_max_login(driver) -> None:
    """Validates login to max"""

    # case where login failed
    try:
        if u.WDW(driver, 3).until(u.EC.visibility_of_element_located((loc.max_loc['login_error_msg']))):
            logger.error("Login failed due wrong credentials")
            raise SystemExit("Error with credentials at Max. Please check your email or password and try again")

    except u.TimeoutException:
        logger.success("Logged in successfully")            # element of login box not found


# INSIDE
def get_transactions(driver, max_request: str, credx: dict) -> str:
    """
    driver process the request and outputs a csv file with the transactions.
    :param driver: the driver, who is not drunk I hope
    :param max_request: the request from the arguments
    :param credx: contains the information from the arguments parameters
    :return:
    """
    # redirection to the transactions page
    driver.get("https://www.max.co.il/transaction-details/personal")

    today_date = datetime.date.today()
    this_year = today_date.year
    today = str(today_date)          # string year-month-day

    if max_request == 'ytd':
        start_date = f'{this_year}-01-01'
        today_date = f'{today}'
        logger.info(f"getting transaction from start of this year to {today}")
        driver.get(f"https://www.max.co.il/transaction-details/personal?sourceGA=CommonActions&filter=-1_-1_0_{this_year}-01-01_{start_date}_{today_date}_-1&sort=1a_1a_1a_1a_1a_1a")

    elif max_request == 'this_month':
        start_date = f'{this_year}-{today_date.month}-01'
        today_date = f'{today}'
        logger.info("getting transactions from this month")
        driver.get(f"https://www.max.co.il/transaction-details/personal?sourceGA=CommonActions&filter=-1_-1_0_{this_year}-01-01_{start_date}_{today_date}_-1&sort=1a_1a_1a_1a_1a_1a")

    elif max_request == 'range':
        logger.info(f"getting transactions from {credx['start_date']} until {credx['end_date']}")
        driver.get(f"https://www.max.co.il/transaction-details/personal?sourceGA=CommonActions&filter=-1_-1_0_{this_year}-01-01_{credx['start_date']}_{credx['end_date']}_-1&sort=1a_1a_1a_1a_1a_1a")

    elif max_request == 'month':
        year_month = credx['year'] + "-" + credx['month']
        logger.info(f"getting transactions from month {credx['month']} and year {credx['year']}")
        driver.get(f"https://www.max.co.il/transaction-details/personal?sourceGA=CommonActions&filter=-1_-1_0_{year_month}-01_-1&sort=1a_1a_1a_1a_1a_1a")

    else:
        return "didn't get your request hon"

    data = data_scrape_from_table(driver)
    convert_to_table(data, max_request)

    message = "these are your requested transactions \n"
    for i in range(len(data['amounts'])):
        message += f"transaction {i}: {data['amounts'][i]} at {data['places'][i]} on {data['dates'][i]} with card {data['cards'][i]} \n"

    return message


def convert_to_table(data: dict, max_request: str) -> None:
    """
    converts the data dictionary into table
    :param data: the dictionary containing the transaction data
    :param max_request: the request itself
    :return:
    """
    u.logger.info('converts data into dataframe table')
    df = u.pd.DataFrame(data)
    df.sort_values(by=['dates'])
    df.loc['Total'] = df.sum(numeric_only=True)

    u.logger.info('converting dataframe into csv file')
    file_name = f'{max_request}_transactions_{round(time.time())}.csv'
    df.to_csv(file_name, encoding='utf-8-sig')
    u.logger.success('data converted to CSV file successfully')
    u.logger.success(f'file can be found right here: {getcwd() + "/" +file_name}')


def data_scrape_from_table(driver) -> dict:
    """Scraping data from transaction table in Max"""
    logger.info("Starting scraping data from transactions table")
    # DATA SCRAPE
    list_date = u.WDW(driver, 30).until(u.EC.visibility_of_all_elements_located(loc.max_loc['transactions_date']))
    list_place = u.WDW(driver, 30).until(u.EC.visibility_of_all_elements_located(loc.max_loc['transactions_place']))
    list_card = u.WDW(driver, 30).until(u.EC.visibility_of_all_elements_located(loc.max_loc['transactions_card']))
    list_amount = u.WDW(driver, 30).until(u.EC.visibility_of_all_elements_located(loc.max_loc['transactions_amount']))

    # filtering text from selenium elements
    data = {"dates": [x.text.replace('.', '/') for x in list_date],
            "places": [str(x.text) for x in list_place],
            "cards_raw": [str(x.text) for x in list_card if x.text.isdigit()],
            "amounts_raw": [x.text for x in list_amount]
            }

    u.logger.success("CONVERTED ALL")

    # formatting the dictionaries:
    # amounts:
    u.logger.info("formatting amounts...")
    data["amounts"] = list(map(format_amounts, data["amounts_raw"]))

    # currency
    u.logger.info("formatting currency...")
    data["currency"] = list(map(format_currency, data["amounts_raw"]))

    return data


def format_amounts(data: str):
    """Cleaning the data from the shekel sign and then reformatting it to be a decimal"""
    map_chars = str.maketrans({'₪': '', '$': '', '€': '', '£': '', ',': ''})
    amount_stripped = data.translate(map_chars)
    amount = Decimal(amount_stripped)
    amount *= -1

    return amount


def format_currency(data: str) -> str:
    """Takes common currency symbol and translate it to currency code"""
    for rec in data:
        if '₪' in rec:
            return 'ILS'
        if '$' in rec:
            return 'USD'
        if '€' in rec:
            return 'EUR'
        if '£' in rec:
            return 'GBP'

        return "-"
