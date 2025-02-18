import time
import sentry_sdk
import os
import sys
import logging
import json
from selenium.webdriver.chrome.options import Options
from agti import central_banks
from agti.utilities.settings import PasswordMapLoader
from selenium import webdriver
from sentry_sdk.integrations.sys_exit import SysExitIntegration
from sentry_sdk.integrations.logging import LoggingIntegration



BANK_NAMES_MAPPER = {bank.split('Bank')[0].lower(): bank for bank in  central_banks.BaseBankScraper.registry.keys()}
psLoader = None

# TODO Move env to one big dict usiong decouple
SENTRY_DSN = os.environ.get('SENTRY_DSN')
DEBUG = os.environ.get('DEBUG', False)
SLEEP = int(os.environ.get('SLEEP', "60"))
TABLE_NAME = os.environ.get('TABLE_NAME')
DB_USER_NAME = os.environ.get('DB_USER_NAME')
RUN_ONLY_BANKS = json.loads(os.environ.get('RUN_ONLY_BANKS', '[]'))


logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to stdout for Docker compatibility
    ]
)
logging.captureWarnings(True)
logger = logging.getLogger(__name__)  # Main logger

"""
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception
"""


if SENTRY_DSN:
    logger.info("SENTRY_DSN is set, enabling error monitoring")
    SENTRY_LOG_LEVEL = os.environ.get('SENTRY_LOG_LEVEL', 'WARNING')
    ENVIRONMENT = os.environ.get('ENVIRONMENT')
    if ENVIRONMENT is None:
        logger.critical("ENVIRONMENT is required, please set the ENVIRONMENT variable for Sentry")
        exit(1)
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # No performance monitoring
        traces_sample_rate=0.0,
        integrations=[
            SysExitIntegration(),
            LoggingIntegration(level=None, event_level=SENTRY_LOG_LEVEL),
        ],
        send_default_pii=True,
        debug=DEBUG,
        environment=ENVIRONMENT,
        in_app_include=["agti"],
    )
else:
    logger.warning("SENTRY_DSN is not set, no error monitoring will be done")








class HeadlessManager:
    def __init__(self, run_headless):
        self.run_headless = run_headless

    def __enter__(self):
        if self.run_headless:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')

            self._driver = webdriver.Chrome(options=options)
        else:
            self._driver = webdriver.Firefox()
        return self._driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()
        time.sleep(0.1)







def run(run_headless, supported_banks):
    logger.info(f"Supported banks: {supported_banks}")
    while True:
        for supported_bank in supported_banks:
            logger.info(f"Processing bank: {supported_bank}")
            with HeadlessManager(run_headless) as driver:
                scrapperCls = central_banks.BaseBankScraper.registry[BANK_NAMES_MAPPER[supported_bank]]
                scrapper = scrapperCls(driver, psLoader.pw_map, DB_USER_NAME, TABLE_NAME)
                try:
                    scrapper.process_all_years()
                except Exception as e:
                    logger.exception(f"Error processing bank: {supported_bank}",
                        extra={
                            "bank": supported_bank,
                            "HEADLESS": run_headless,
                            "DB_USER_NAME": DB_USER_NAME,
                            "TABLE_NAME": TABLE_NAME
                            }
                    )
        if SLEEP >= 0:
            time.sleep(SLEEP)
        else:
            break


def main(run_headless=True):
    global psLoader, RUN_ONLY_BANKS
    # verify input and initialize password loader
    password = os.environ.get('PASSWORD')
    if not password:
        logger.critical("PASSWORD is required, please set the PASSWORD environment variable")
        exit(1)
    psLoader = PasswordMapLoader(password=password)

    if not DB_USER_NAME:
        logger.critical("DB_USER_NAME is required, please set the DB_USER_NAME environment variable")
        exit(1)
    if not TABLE_NAME:
        logger.critical("TABLE_NAME is required, please set the TABLE_NAME environment variable")
        exit(1)
    if len(RUN_ONLY_BANKS) > 0:
        for bank in RUN_ONLY_BANKS:
            if bank not in BANK_NAMES_MAPPER.keys():
                print(f"\"{bank}\" not in supoprted banks")
                print("Supported banks are:")
                print(list(BANK_NAMES_MAPPER.keys()))
                exit(1)
    else:
        # use all banks
        RUN_ONLY_BANKS = list(BANK_NAMES_MAPPER.keys())
    run(run_headless, RUN_ONLY_BANKS)


if __name__ == '__main__':
    main(True)
