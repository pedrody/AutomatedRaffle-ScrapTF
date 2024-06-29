from seleniumbase import Driver
import platform
import pickle
import argparse

instruction_msg = """
[+] This script automates the process of collecting cookies from a login
    session on "https://scrap.tf", allowing the cookies to be used in the main
    script (main.py).

[+] Instructions:
    > Log in with your Steam account;
    > After logging in, go to the main page ("https://scrap.tf");
    > Wait 5 seconds;
    > Your cookies ('cookies.pkl') will appear in the directory
      where this script is located.
"""


def main():
    driver = Driver(uc=True, headed=True)
    driver.get('https://scrap.tf/login')

    while True:
        if driver.current_url == 'https://scrap.tf/':
            driver.sleep(5)
            cookies = driver.get_cookies()
            pickle.dump(cookies, open('cookies.pkl', 'wb'))

            print('Cookies collected successfully!')

            driver.quit()
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=instruction_msg)
    args = parser.parse_args()

    main()
