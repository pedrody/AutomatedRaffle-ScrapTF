from seleniumbase import Driver
import pickle


def main():
    driver = Driver(uc=True)

    driver.get('https://scrap.tf')

    cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in cookies:
        cookie['domain'] == 'scrap.tf'

        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)

    driver.get('https://scrap.tf/raffles')

    driver.sleep(900)

    driver.quit()


if __name__ == '__main__':
    main()
