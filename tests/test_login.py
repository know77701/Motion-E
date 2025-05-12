import time

from locators.login_locators import LoginLocators
from pages.login_page import *
from pages.login_page import LoginPage
from tests.test_login import *
from utils.app_manager import AppManger


class TestLogin:
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        self.window = self.app_manager.app_connect(retries=0)
        self.login = LoginPage(self.window)
        self.test_login_process()

    """로그인 테스트"""
    def test_login_process(self):
        self.login.hospital_info_view()
        self.login.hospital_yakiho_setting(LoginLocators.YAKIHO_VALUE)
        self.login.user_id_setting("ADMIN")
        self.login.user_pw_setting("xmfkdldjq1!1")
        self.login.login_btn_click()
        