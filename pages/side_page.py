from locators.dashboard_locators import DashboardLocators
from locators.side_field_locators import SideFieldLocators
from pages.base_page import *
from utils.app_manager import AppManger


class SidePage:
    def __init__(self,app):
        self.side_window = app.window(title=DashboardLocators.MAIN_FORM_TITLE)
        self.base_page = BasePage(app)
        # self.side_field = self.base_page.find_element(auto_id=SideFieldLocators.SIDE_GROUP)
        
    def dashboard_reset(self):
        self.base_page.dashboard_reset(self.side_window)
        return
    
    """공지사항 입력"""
    def set_notice(self, set_value):
        self.side_field = self.side_window.child_window(class_name="Chrome_RenderWidgetHostHWND", control_type="Document")
        for i in self.side_field.children():
            print(i.element_info.name)
            print(i.element_info.control_type)
        return
    
    """입력된 공지사항 확인"""
    def get_notice(self, compare_value):
        return