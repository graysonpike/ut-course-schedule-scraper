# Grayson Pike, 2018

import mechanicalsoup
import json


def read_credentials(filename):
    # Return credentials in a tuple: ('username', 'password')
    credentials = json.load(open(filename))
    return (credentials['username'], credentials['password'])


def login(browser, credentials):
    # Open generic UT login page and login using given credentials
    # This function should be run with a newly created instance of a StatefulBrowser
    # Credentials should be a tuple of ('username', 'password')
    # Returns true if login is successful, false otherwise
    browser.open("https://login.utexas.edu/login/UI/Login")
    browser.select_form('form[name="Login"]')
    # print(browser.get_current_form().print_summary())
    browser["IDToken1"] = credentials[0]
    browser["IDToken2"] = credentials[1]
    response = browser.submit_selected()
    if(response.url == "https://www.utexas.edu"):
        return True
    return False


def main():

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )

    credentials = read_credentials("credentials.json")
    print("Using credentials for UTEID " + credentials[0])

    if(login(browser, credentials) is False):
        print("Login failed. Have you entered the correct credentials in credentials.json?")

    # Increase verbosity
    # browser.set_verbose(2)


main()
