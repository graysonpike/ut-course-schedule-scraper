# Grayson Pike, 2018

import mechanicalsoup
import json


def read_credentials(filename):
    # Return credentials in a tuple: ('username', 'password')
    credentials = json.load(open(filename))
    return (credentials['username'], credentials['password'])


def main():

    credentials = read_credentials("credentials.json")
    print("Using credentials for UTEID " + credentials[0])

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )

    # Increase verbosity
    browser.set_verbose(2)

    # Open generic UT login page
    browser.open("https://login.utexas.edu/login/UI/Login")
    browser.select_form('form[name="Login"]')
    # print(browser.get_current_form().print_summary())
    browser["IDToken1"] = credentials[0]
    browser["IDToken2"] = credentials[1]
    resp = browser.submit_selected()
    browser.open("https://utdirect.utexas.edu/apps/registrar/course_schedule/20182/")
    browser.launch_browser()


main()
