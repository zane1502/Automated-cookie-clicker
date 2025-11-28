import undetected_chromedriver as uc
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys

chrome_driver_path = r'.\chromedriver-win64\chromedriver-win64\chromedriver.exe'
cookie_site = 'https://orteil.dashnet.org/cookieclicker/'


def get_cps(web_driver):
    for _ in range(3):  # retry up to 3 times
        try:
            elem = web_driver.find_element(
                by='xpath',
                value='//*[@id="cookiesPerSecond"]'
            )
            return elem.text.split()[-1]
        except StaleElementReferenceException:
            time.sleep(0.01)  # tiny delay before retry

    return None  # failed after 3 attempts

def main():

    # service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Using Undetected Chrome Web Driver to prevent Cloudflare from recognising the Selenium bot
    driver = uc.Chrome(options=options, use_subprocess=False)
    driver.get(cookie_site)

    # 15 Seconds delay for the site to load before proceeding to next steps
    time.sleep(15)

    # Pick language choice on first click
    language_choice = driver.find_element(by='xpath', value='//*[@id="langSelect-EN"]')
    language_choice.click()

    # Add 5 seconds delay for site to load
    time.sleep(5)

    cookie_button = driver.find_element(by='xpath', value='//*[@id="bigCookie"]')
    time.sleep(5)

    # Set Initial time the cookie clicker commences, a timeout timer and a two-minute timer
    initial_time = time.time()
    timeout = time.time() + 5
    two_min = time.time() + 60 * 2  # 2 minutes

    while True:

        # Click on the cookie icon until the timeout timer is triggered by the if statement below
        cookie_button.click()
        time.sleep(0.1)

        if time.time() > timeout:

            # Get the current number of cookies for each iteration
            cookie_counter = driver.find_element(by='id', value='cookies').text
            cookie_counter = int(cookie_counter.split()[0])

            # Check the current price of each element
            cursor_clicker_price = int(driver.find_element(by= 'xpath', value= '//*[@id="productPrice0"]').text)
            granny_price = int(driver.find_element(by= 'xpath', value= '//*[@id="productPrice1"]').text)

            print(f"Cookies available: {cookie_counter}\n")
            print(f"Cursor clicker price: {cursor_clicker_price}\n")
            print(f"Granny Price: {granny_price}\n\n")

            # Compare price of each element to the amount of cookies available to determine whether buy is possible
            if cookie_counter >= granny_price:
                driver.find_element(by= 'xpath', value= '//*[@id="product1"]').click()

            elif cookie_counter >= cursor_clicker_price:
                driver.find_element(by= 'xpath', value= '//*[@id="product0"]').click()

            timeout = time.time() + 5
            print(f"Time passed: {int(timeout - initial_time)} seconds.")

        if time.time() > two_min:
            cookie_per_s = get_cps(driver)
            print(cookie_per_s)
            break


if __name__ == "__main__":
    main()