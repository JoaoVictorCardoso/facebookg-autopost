import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from win10toast import ToastNotifier

toaster = ToastNotifier()


class GroupAuto():
    """Auto post on all facebook groups using
    selenium python.

    Attributes:
        browser (TYPE): webdrive.Chrome
        URL (str): mbasic URL of facebook
        group_elem (TYPE): group elements by xpath
        login_elem (TYPE): login elements by xpath
    """

    def __init__(self, hide=False):
        """Initialize webdriver

        Args:
            hide (bool, optional): Display or hide
                browser
        """
        super(GroupAuto, self).__init__()
        self.browser = webdriver.Chrome()

        self.URL = "https://mbasic.facebook.com"

        # login xpath collection
        self.login_elem = {
            "user_input": "//input[@id='m_login_email']",
            "pass_input": "//input[@name='pass']",
            "login_btn": "//input[@value='Log In']",
        }

        # group xpath collection
        self.group_elem = {
            "post_textarea": "//textarea[@id='u_0_0']",
            "post_btn": "//input[@value='Post']"
        }

    def login(self, username, password):
        """Login facebook account

        Args:
            username (STRING): fb username
            password (STRING): fb password
        """
        self.browser.get(self.URL)

        usr = self.browser.find_element_by_xpath(
            self.login_elem['user_input']
        )

        pwd = self.browser.find_element_by_xpath(
            self.login_elem['pass_input']
        )

        btn = self.browser.find_element_by_xpath(
            self.login_elem['login_btn']
        )

        # login user

        usr.send_keys(username)
        pwd.send_keys(password)
        btn.click()

        # wait for login button to disappear
        try:
            WebDriverWait(self.browser, 15).until_not(
                EC.presence_of_element_located((
                    By.XPATH,
                    self.login_elem['login_btn'])
                ))

            toaster.show_toast(
                "Menudo.Space: FBAuto",
                "Sucessfully logged in.",
                duration=3
            )

        except TimeoutException:
            print("Error: Invalid Credentials.")
            self.browser.quit()

    def get_groups(self, limit=None):
        """Get all groups in your facebook

        Args:
            limit (None, optional): Number of groups
                to be returned

        Returns:
            LIST: A list of group URLs
        """
        self.browser.get(self.URL + "/groups/?seemore")

        try:
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//h3[@class='br']")
                ))
        except TimeoutException as e:
            # print("Error: Can't go to 'see all groups'")
            # toaster.show_toast(
            #     "Menudo.Space: FBAuto",
            #     "No groups found.",
            #     duration=3
            # )
            # self.browser.quit()
            raise e

        # extract all groups
        soup = BeautifulSoup(self.browser.page_source,
                             "html.parser")

        groups = soup.find_all(
            "a", href=re.compile(r"groups/\d"))

        # return all group URLs
        if groups:
            toaster.show_toast(
                "Menudo.Space: FBAuto",
                f"{len([x['href'] for x in groups[:limit]])}. Grups",
                duration=3
            )
            return [x['href'] for x in groups[:limit]]

    def post(self, groups, description, interval, debug=False):
        """Post to groups in facebook. Use at your own risk.

        Args:
            groups (List): A list of group URLs
            description (String): Words to post in group
            interval (Int): Time interval to post
        """
        for idx, group in enumerate(groups):
            self.browser.get(self.URL + group)

            # Wait for text area to appear
            try:
                WebDriverWait(self.browser, 15).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        self.group_elem['post_textarea'])
                    ))
            except TimeoutException:
                continue  # Skip if not found

            post = self.browser.find_element_by_xpath(
                self.group_elem['post_textarea']
            )

            btn = self.browser.find_element_by_xpath(
                self.group_elem['post_btn']
            )

            post.send_keys(description)
            toaster.show_toast(
                "Menudo.Space: FBAuto",
               f"Posted in group {idx+1} of {len(groups)+1}",
                duration=3
            )

            time.sleep(interval)

            if not debug:
                btn.click()
