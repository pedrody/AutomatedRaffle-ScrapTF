from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pickle


class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[m'
    BOLD = '\033[1m'


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
    return Color.BOLD + logo + Color.RESET


def scroll_to_bottom(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.sleep(2)


def collect_raffle_links(driver):
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

    print(f'    {Color.YELLOW}> Raffle:{Color.RESET} '
          f'{raffle_name}')
    print(f'    {Color.YELLOW}> Link:{Color.RESET} {link}')

    print(f'    {Color.YELLOW}> Going to next...\n{Color.RESET}')
    print('-\n')
    driver.sleep(5)


def inject_cookies(driver, cookies):
    try:
        for cookie in cookies:
            cookie['domain'] == 'scrap.tf'
            driver.add_cookie(cookie)
        driver.refresh()
        return check_cookie_injection(driver)

    except Exception as e:
        print(f'{Color.RED}[!] Error when injecting cookies: {e}{Color.RESET}')
        return False


def check_cookie_injection(driver):
    try:
        avatar_container = driver.find_element(
            By.CSS_SELECTOR, '.avatar-container')
        return True
    except NoSuchElementException:
        return False


def main():
    url = 'https://scrap.tf'
    driver = Driver(uc=True)
    driver.get(url)

    print(f'{Color.BLUE}[*] Injecting cookies for login...{Color.RESET}')
    cookies = pickle.load(open('cookies.pkl', 'rb'))

    while True:
        if inject_cookies(driver, cookies):
            print(f'{Color.GREEN}[+] Successfully logged in!\n{Color.RESET}')
            break
        else:
            print(
                f'{Color.RED}[-] Login unsuccessful, retrying...{Color.RESET}')
            driver.sleep(10)
            driver.refresh()

    print(
        f'{Color.GREEN}[+] Collecting all currently active raffles...\n{Color.RESET}')
    raffles_links = collect_raffle_links(driver)

    while True:
        print(
            f'{Color.GREEN}[+] Open Raffles Found: {len(raffles_links)}\n{Color.RESET}')
        for link in raffles_links:
            enter_raffle(driver, link)

        print(f'{Color.BLUE}[*] Searching for new raffles...')
        new_raffles_links = collect_raffle_links(driver)

        if new_raffles_links:
            print(f'[!] New raffles were found!{Color.RESET}\n')
            raffles_links = new_raffles_links
            continue
        break

    raffles_stats = driver.find_element(
        By.CSS_SELECTOR, '.raffle-list-stat h1').text
    print(f'{Color.GREEN}[+] Successfully entered all raffles!')
    print(f'[+] Open Raffles Entered: {raffles_stats}\n{Color.RESET}')

    driver.quit()


if __name__ == '__main__':
    print(logo())
    main()
