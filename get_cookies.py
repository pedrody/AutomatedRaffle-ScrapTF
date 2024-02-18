from seleniumbase import Driver
import pickle

driver = Driver(uc=True)
driver.get('https://scrap.tf/login')

while True:
    if driver.current_url == 'https://scrap.tf/':
        driver.sleep(5)
        cookies = driver.get_cookies()
        pickle.dump(cookies, open('cookies.pkl', 'wb'))

        print('Cookies collected successfully!')

        driver.quit()
        break
