from seleniumbase import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pickle


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
            print(e)

    driver.get(url_raffles)

    raffles_links = []

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
            raffle_link = raffle.find('a')['href']
            raffles_links.append(url + raffle_link)

        print('Open Raffles Entered:', raffles_stats)

    driver.sleep(9999)
    driver.quit()


if __name__ == '__main__':
    main()
