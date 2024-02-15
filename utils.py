"""Module providing all major imports"""
# pylint: disable=unused-import
# pylint: disable=useless-import-alias
# selenium
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions as ChromeOptions
from selenium.webdriver import ChromeService as ChromeService
from selenium.webdriver import ActionChains as AC
from selenium.common.exceptions import TimeoutException

# webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager

# logging
from loguru import logger

# pandas
import pandas as pd
