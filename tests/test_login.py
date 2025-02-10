import time

from locators.login_locators import LoginLocators
from pages.login_page import *
from pages.login_page import LoginPage
from tests.test_login import *
from utils.app_manager import AppManger


class TestLogin:
    def setup_method(self):
        """테스트 실행 전 초기화 작업"""
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        self.window = self.app_manager.app_connect(retries=0)
        self.login = LoginPage(self.window)

    def test_login_process(self):
        """로그인 과정 테스트"""
        self.login.yakiho_info()
        self.login.edit_value_stting(LoginLocators.YKIHO_TEXT_ID, "22222222")
        self.login.btn_click(LoginLocators.YKIHO_SAVE_BUTTON_ID)

        self.login.edit_value_stting(LoginLocators.ID_EDIT_ID, "트라이업")
        self.login.edit_value_stting(LoginLocators.PW_EDIT_ID, "xmfkdldjq1!1")
        self.login.btn_click(LoginLocators.LOGIN_BUTTON_ID)
