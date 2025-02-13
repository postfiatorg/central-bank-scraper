from selenium import webdriver
from agti.utilities.settings import PasswordMapLoader
from agti.central_banks import EnglandBankScrapper
from selenium.webdriver.chrome.options import Options
import logging


# setup simple logging for INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    psLoader = PasswordMapLoader('aaa')
    print(psLoader.pw_map)

    #driver = webdriver.Firefox()
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

    driver = webdriver.Chrome(options=options)
    scrapper = EnglandBankScrapper(driver, psLoader.pw_map, 'postgres', 'central_banks_g10')
    scrapper.process_all_years()
    #scrapper.process_archive()

    driver.quit()


if __name__ == '__main__':
    main()
