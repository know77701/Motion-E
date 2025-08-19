import pytest

from locators.login_locators import LoginLocators
from pages.login_page import LoginPage


# @pytest.mark.skip(reason="현재 로그인 테스트 비활성화 중")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, app_manager):
        """pytest가 매 테스트 전에 실행하는 setup"""
        connected_app = app_manager.app_connect()
        if connected_app is None:
            pytest.skip("애플리케이션에 연결할 수 없습니다. 테스트를 건너뜁니다.")
        self.login = LoginPage(connected_app)
        
    @pytest.mark.order(0)
    def test_login_process(self):
        """로그인 테스트"""
        self.login.login_full_process("ADMIN", "xmfkdldjq1!1", LoginLocators.YAKIHO_VALUE)
        # Add assertion here to verify successful login, e.g., check for main window visibility
        # assert self.login.app.window(title=LoginLocators.MAIN_FORM_TITLE, auto_id=LoginLocators.MAIN_FORM_AUTOMATION_ID).exists()
