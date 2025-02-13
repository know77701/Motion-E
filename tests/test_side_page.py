from pages.side_page import SidePage
from utils.app_manager import AppManger


class TestSidePage:
    
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        self.window = self.app_manager.app_connect(retries=0)
        self.side_page = SidePage(self.window)
        self.test_set_notice()
    
    def test_set_notice(self):
        self.side_page.set_notice("테스트")
        return
    