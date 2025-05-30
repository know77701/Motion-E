import pytest

from locators.login_locators import LoginLocators
from pages.login_page import LoginPage


@pytest.mark.skip(reason="현재 로그인 테스트 비활성화 중")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, app_manager):
        """pytest가 매 테스트 전에 실행하는 setup"""
        window = app_manager.app_connect(retries=0).window(title=LoginLocators.LOGIN_FORM_TITLE)
        self.login = LoginPage(window)

    def test_login_process(self):
        """로그인 테스트"""
        self.login.hospital_info_view()
        self.login.hospital_yakiho_setting(LoginLocators.YAKIHO_VALUE)
        self.login.user_id_setting("ADMIN")
        self.login.user_pw_setting("xmfkdldjq1!1")
        self.login.login_btn_click()
