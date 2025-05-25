import time

from locators.login_locators import LoginLocators
from pages.login_page import *
from pages.login_page import LoginPage
from tests.test_base import TestBase
from tests.test_login import *


class TestLogin(TestBase):
    def __init__(self):
        super.__init__()
        
        self.login = LoginPage(self.window)
        self.test_login_process()

    """로그인 테스트"""
    def test_login_process(self):
        self.login.hospital_info_view()
        self.login.hospital_yakiho_setting(LoginLocators.YAKIHO_VALUE)
        self.login.user_id_setting("ADMIN")
        self.login.user_pw_setting("xmfkdldjq1!1")
        self.login.login_btn_click()
        