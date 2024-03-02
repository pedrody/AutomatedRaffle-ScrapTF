from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pickle
import argparse
import platform



class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[m'


def logo():
    logo = """
@@@@@@@   @@@@@@@@  @@@@@@@   @@@@@@@    @@@@@@   @@@@@@@   @@@ @@@  
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@ @@@  
@@!  @@@  @@!       @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@! !@@  
!@!  @!@  !@!       !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@! @!!  
@!@@!@!   @!!!:!    @!@  !@!  @!@!!@!   @!@  !@!  @!@  !@!   !@!@!   
!!@!!!    !!!!!:    !@!  !!!  !!@!@!    !@!  !!!  !@!  !!!    @!!!   
!!:       !!:       !!:  !!!  !!: :!!   !!:  !!!  !!:  !!!    !!:    
:!:       :!:       :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!    :!:    
::        :: ::::   :::: ::  ::   :::  ::::: ::   :::: ::     ::    
:        : :: ::   :: :  :    :   : :   : :  :   :: :  :      : 

                    github.com/pedrody

"""
    return logo


def scroll_to_bottom(driver):
    """
    The function `scroll_to_bottom` scrolls the webpage to the bottom using
    JavaScript in a Python Selenium script.

    :param driver: The `driver` parameter in the `scroll_to_bottom` function is
    typically an instance of a web driver, such as Selenium WebDriver, that allows
    you to interact with a web browser in an automated way. This parameter is used
    to scroll to the bottom of a web page by executing a JavaScript code that
    """
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.sleep(2)


def collect_raffle_links(driver):
    """
    The function `collect_raffle_links` collects links to raffles from the website
    scrap.tf by scrolling through the page and extracting the links.

    :param driver: The `driver` parameter in the `collect_raffle_links` function is
    typically an instance of a WebDriver, such as Selenium's WebDriver, that allows
    you to automate interactions with a web browser. In this case, it is used to
    navigate to a webpage, scroll to the bottom of the page
    :return: The `collect_raffle_links` function returns a list of URLs for raffles
    on the website "https://scrap.tf/raffles" that the user can enter.
    """
    raffles_links = []

    driver.get('https://scrap.tf/raffles')

    while True:
        scroll_to_bottom(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if "That's all, no more!" in soup.get_text():
            scroll_to_bottom(driver)
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    raffles_div = soup.find('div', id='raffles-list')
    if raffles_div:
        raffles = raffles_div.find_all('div', class_='panel-raffle')
        for raffle in raffles:
            if not raffle.has_attr('class') or 'raffle-entered' not in raffle['class']:
                raffle_link = raffle.find('a')['href']
                raffles_links.append('https://scrap.tf' + raffle_link)

    return raffles_links


def enter_raffle(driver, link):
    """
    The function `enter_raffle` navigates to a given link, attempts to enter a
    raffle by clicking a specific button, and prints the raffle name and link before
    moving on to the next action.

    :param driver: The `driver` parameter is typically an instance of a web driver,
    such as Selenium WebDriver, that allows you to interact with a web browser in an
    automated way. It is used to navigate to web pages, interact with elements on
    the page, and perform various actions like clicking buttons or entering text
    :param link: The `link` parameter in the `enter_raffle` function is the URL of
    the webpage where the raffle is being held. This function uses Selenium to
    navigate to the provided link and attempt to enter the raffle by clicking on the
    "Enter Raffle" button on the page
    """
    driver.get(link)

    try:
        raffle_name = driver.find_element(
            By.CSS_SELECTOR, 'h3.subtitle').text

        raffle_enter_button = driver.find_element(
            By.XPATH, "(//button[contains(text(),'Enter Raffle')])[2]")
        driver.execute_script(
            "arguments[0].click();", raffle_enter_button)
        print(
            f'{Color.GREEN}[+] Successfully entered the raffle!{Color.RESET}')
    except Exception as e:
        print(
            f'{Color.RED}[-] Failed to enter the raffle: {e}{Color.RESET}')

    print(f'> Raffle: {raffle_name}')
    print(f'> Link: {link}')

    print(f'> Going to next...\n')
    print('-\n')
    driver.sleep(5)


def inject_cookies(driver, cookies):
    """
    The function injects cookies into a web driver and checks if the injection was
    successful.

    :param driver: The `driver` parameter in the `inject_cookies` function is
    typically an instance of a web driver, such as Selenium WebDriver, used for
    automating web browser interactions. It allows you to control the browser,
    navigate to different pages, interact with elements on the page, and perform
    various actions like clicking
    :param cookies: The `cookies` parameter is a list of dictionaries containing
    information about cookies to be injected into the browser. Each dictionary in
    the list represents a single cookie with key-value pairs such as 'name',
    'value', 'domain', 'path', 'expiry', etc. These cookies are added to the browser
    :return: The function `inject_cookies` is returning the result of the function
    `check_cookie_injection(driver)`.
    """
    try:
        for cookie in cookies:
            cookie['domain'] == 'scrap.tf'
            driver.add_cookie(cookie)
        driver.refresh()
        return check_cookie_injection(driver)

    except Exception as e:
        print(f'{Color.RED}[-] Error when injecting cookies: {e}{Color.RESET}')
        return False


def check_cookie_injection(driver):
    """
    The function `check_cookie_injection` checks for the presence of an avatar
    container element on a web page using a CSS selector.

    :param driver: The `driver` parameter is typically an instance of a web driver,
    such as Selenium WebDriver, that allows you to interact with a web browser in an
    automated way. In this context, it seems like the function
    `check_cookie_injection` is checking for the presence of an element with the CSS
    class
    :return: The function `check_cookie_injection` is returning a boolean value. It
    returns `True` if the avatar container element with the CSS selector
    '.avatar-container' is found in the web page using the provided `driver`, and it
    returns `False` if the element is not found (NoSuchElementException is raised).
    """
    try:
        avatar_container = driver.find_element(
            By.CSS_SELECTOR, '.avatar-container')
        return True
    except NoSuchElementException:
        return False


def main(headless=False):
    """
    The main function automates the process of logging in, collecting and entering
    raffles on a website using Selenium WebDriver in Python.
    """

    # Initialization and setup
    url = 'https://scrap.tf'
    driver = Driver(uc=True, headed=True) if platform.system() == 'Linux' else Driver(uc=True)
    driver.get(url)

    # Injecting cookies for login
    print(f'{Color.GREEN}[+] Injecting cookies for login...{Color.RESET}')
    cookies = pickle.load(open('cookies.pkl', 'rb'))
    while True:
        if inject_cookies(driver, cookies):
            print('> Successfully logged in!\n')

            break
        else:
            print('> Login unsuccessful, retrying...')
            driver.sleep(10)
            driver.refresh()

    # Collecting raffle links
    print(
        f'{Color.GREEN}[+] Collecting all currently active raffles...{Color.RESET}')
    raffles_links = collect_raffle_links(driver)

    # Entering raffles
    while True:
        print(
            f'> Open Raffles Found: {len(raffles_links)}\n')
        for link in raffles_links:
            enter_raffle(driver, link)

        # Checking for new raffles
        print(f'{Color.GREEN}[+] Searching for new raffles...{Color.RESET}')
        new_raffles_links = collect_raffle_links(driver)

        # If new raffles are found, continue entering them
        if new_raffles_links:
            print('> New raffles were found!')
            raffles_links = new_raffles_links
            continue
        break

    # Displaying raffle statistics
    raffles_stats = driver.find_element(
        By.CSS_SELECTOR, '.raffle-list-stat h1').text
    print(f'{Color.GREEN}[+] Successfully entered all raffles!{Color.RESET}')
    print(f'> Open Raffles Entered: {raffles_stats}\n')

    # Quitting the driver
    driver.quit()


if __name__ == '__main__':
    # Setting up the parser and adding headless mode argument
    parser = argparse.ArgumentParser(description='Scrap.tf Raffle Bot')
    parser.add_argument('--headless', action='store_true',
                        help='Run in headless mode')
    args = parser.parse_args()

    print(logo())
    main(headless=args.headless)
