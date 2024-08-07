from seleniumbase import Driver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle
import argparse


class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[m'


def scroll_to_bottom(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')


def collect_raffle_links(driver):
    driver.get('https://scrap.tf/raffles')

    while not driver.is_element_visible('.raffle-pagination-done'):
        scroll_to_bottom(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    raffles_div = soup.find('div', id='raffles-list')
    raffles_links = set()
    if raffles_div:
        raffles = raffles_div.find_all('div', class_='panel-raffle')
        for raffle in raffles:
            if not raffle.has_attr('class') or 'raffle-entered' not in raffle[
                    'class']:
                raffle_link = raffle.find('a')['href']
                raffles_links.add('https://scrap.tf' + raffle_link)

    return raffles_links


def enter_raffle(driver, link):
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
    driver.sleep(3)


def inject_cookies(driver, cookies):
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
    if driver.is_element_visible(
        # CSS path of the login button
        'html body#pid-index.page-theme-light nav.navbar.yamm.navbar-default.'
        'navbar-fixed-top.navbar-main div.container div#navbar-main.collapse.'
        'navbar-collapse ul.nav.navbar-nav.navbar-right li a img.sits-login'
    ):
        return False
    return True


def main(monitor=False):
    url = 'https://scrap.tf'
    driver = Driver(uc=True, headed=True)
    driver.get(url)

    print(f'\n{Color.GREEN}[+] Injecting cookies for login...{Color.RESET}')
    cookies = pickle.load(open('cookies.pkl', 'rb'))
    while True:
        if inject_cookies(driver, cookies):
            print('> Successfully logged in!\n')
            break
        else:
            print('> Login unsuccessful, retrying...')
            driver.sleep(10)
            driver.refresh()

    print(
        f'{Color.GREEN}[+] Collecting all currently active raffles...{Color.RESET}'
    )
    raffles_links = collect_raffle_links(driver)

    if raffles_links:
        while True:
            print(
                f'> Open Raffles Found: {len(raffles_links)}\n')
            for link in raffles_links:
                enter_raffle(driver, link)

            print(
                f'{Color.GREEN}[+] Searching for new raffles...{Color.RESET}')
            new_raffles_links = collect_raffle_links(driver)

            if new_raffles_links:
                print('> New raffles were found!')
                raffles_links = new_raffles_links
                continue
            break

    raffles_stats = driver.find_element(
        By.CSS_SELECTOR, '.raffle-list-stat h1').text
    print(f'{Color.GREEN}[+] Successfully entered all raffles!{Color.RESET}')
    print(f'> Open Raffles Entered: {raffles_stats}\n')

    if monitor:
        print(f'{Color.GREEN}[+] Monitoring for new raffles...\n{Color.RESET}')
        while True:
            raffles_links = collect_raffle_links(driver)
            if raffles_links:
                for link in raffles_links:
                    enter_raffle(driver, link)
            driver.sleep(60)

    driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrap.tf Raffle Bot')
    parser.add_argument('--headless', action='store_true',
                        help='Run in headless mode')
    parser.add_argument('--monitor', action='store_true',
                        help='constantly monitor for new raffles')
    args = parser.parse_args()

    main(monitor=args.monitor)
