# Grayson Pike, 2018

import mechanicalsoup
import json


# Semester schedule ID, used by UT systems
UT_SCHEDULE_ID = 20182


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
    browser["IDToken1"] = credentials[0]
    browser["IDToken2"] = credentials[1]
    response = browser.submit_selected()
    if(response.url == "https://www.utexas.edu"):
        return True
    return False


def get_course_status(browser, unique):
    # Return a string of the course status if the course exists in this semseter schedule,
    # returns None otherwise
    browser.open("https://utdirect.utexas.edu/apps/registrar/course_schedule/" + str(UT_SCHEDULE_ID) + "/" + str(unique) + "/")
    # UT's systems (built on Sun's Open SSO?) use a form with something called 'LARES data' which is automatically submitted
    # on pageload by browsers, followed by a second auto-submitted form, and then the final webpage. The Browser in mechanicalsoup
    # doesn't auto load these two forms, so we must do it manually.
    browser.select_form()
    browser.submit_selected()
    browser.select_form()
    browser.submit_selected()

    # Now, the final webpage is loaded and ready for parsing
    page = browser.get_current_page()
    result_tag = page.find(attrs={"data-th": "Status"})
    if(result_tag is None):
        return None
    return result_tag.string


def main():

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
    )

    credentials = read_credentials("credentials.json")
    print("Using credentials for UTEID " + credentials[0])

    if(login(browser, credentials) is False):
        print("Login failed. Have you entered the correct credentials in credentials.json?")

    print(get_course_status(browser, 12345))


main()
