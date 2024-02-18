from seleniumbase import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pickle


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
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.sleep(2)


def main():
    url = 'https://scrap.tf'
    url_raffles = f'{url}/raffles'
    driver = Driver(uc=True)
    driver.get(url)

    cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in cookies:
        cookie['domain'] == 'scrap.tf'

        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f'[!] Error when injecting cookies: {e}')

    driver.get(url_raffles)

    raffles_links = []

    print('[+] Collecting all currently active raffles...\n')
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
        raffles_stats = driver.find_element(
            By.CSS_SELECTOR, '.raffle-list-stat h1').text
        for raffle in raffles:
            if not raffle.has_attr('class') or 'raffle-entered' not in raffle['class']:
                raffle_link = raffle.find('a')['href']
                raffles_links.append(url + raffle_link)

        print(f'[+] Open Raffles Entered: {raffles_stats}\n')

        for link in raffles_links:
            driver.get(link)
            raffle_name = driver.find_element(
                By.CSS_SELECTOR, 'h3.subtitle').text

            print('[>] Acessing the raffle:', raffle_name)
            print(f'[>] Link: {link}\n')

            print('[*] Trying to enter the raffle...\n')
            try:
                raffle_enter_button = driver.find_element(
                    By.XPATH, "(//button[contains(text(),'Enter Raffle')])[2]")

                driver.execute_script(
                    "arguments[0].click();", raffle_enter_button)
                print('[+] Successfully entered the raffle!')
            except Exception as e:
                print(f'[-] Failed to enter the raffle: {e}')

            print('[>] Going to next...\n')
            driver.sleep(3)

        driver.get(url_raffles)
        print('[+] Successfully entered all raffles!')
        print(f'[+] Open Raffles Entered: {raffles_stats}\n')

    driver.sleep(9999)
    driver.quit()


if __name__ == '__main__':
    print(logo())
    main()
