from locators.dashboard_locators import DashboardLocators
from locators.side_field_locators import SideFieldLocators
from pages.base_page import *
from utils.app_manager import AppManger


class SidePage:
    def __init__(self,app):
        self.side_window = app.window(title=AppManger.version_search(self, DashboardLocators.MAIN_FORM_TITLE))
        self.base_page = BasePage(app)
        # self.dashboard_reset();
        # self.side_field = self.base_page.find_element(auto_id=SideFieldLocators.SIDE_GROUP)
        
    def dashboard_reset(self):
        self.base_page.dashboard_reset(self.side_window)
        return
    
    def set_notice(self, set_value):
        """공지사항 입력"""
        side_field = self.side_window.child_window(class_name="Chrome_RenderWidgetHostHWND")
        print(side_field.children())
        return
    
    def get_notice(self, compare_value):
        """입력된 공지사항 확인"""
        return