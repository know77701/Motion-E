import time

from locators.login_locators import LoginLocators
from pages.login_page import *
from pages.login_page import LoginPage
from tests.test_login import *
from utils.app_manager import AppManger


class TestLogin:
    """테스트 실행 전 초기화 작업"""
    def setup_method(self, app):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        self.window = self.app_manager.app_connect(retries=0)
        self.login = LoginPage(self.window)

    """로그인 과정 테스트"""
    def test_login_process(self):
        self.login.hospital_info_view()
        self.login.hospital_yakiho_setting()
        self.login.user_id_setting()
        self.login.user_pw_setting()
        self.login.login_btn_click()
        