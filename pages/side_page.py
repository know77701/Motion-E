from pywinauto import Desktop

from locators.dashboard_locators import DashboardLocators
from locators.side_field_locators import SideFieldLocators
from pages.base_page import *
from utils.app_manager import AppManger


class SidePage:
    def __init__(self,app):
        app = AppManger()
        app_title = app.version_search(DashboardLocators.MAIN_FORM_TITLE)
        self.side_window = Desktop(backend="uia").window(title=app_title)
        self.base_page = BasePage(app)
        # self.dashboard_reset();
        # self.side_field = self.base_page.find_element(auto_id=SideFieldLocators.SIDE_GROUP)
        
    def dashboard_reset(self):
        self.base_page.dashboard_reset(self.side_window)
        return
    def side_find_field(self, find_name):
        side_field = self.side_window.child_window(class_name="Chrome_RenderWidgetHostHWND").wrapper_object()
        side_list = side_field.children()
        
        list_boxes = [item for item in side_list if item.element_info.control_type == "List"]
        button_boxes = [item for item in side_list if item.element_info.control_type == "Button"]
        today_btn = [item for item in side_list if item.element_info.control_type == "Button"
                        and item.element_info.name == "오늘"]
        search_btn = [item for item in side_list if item.element_info.control_type == "Button"
                        and item.element_info.name == "검색"]
        Edit_boxes = [item for item in side_list if item.element_info.control_type == "Edit" 
                        and item.element_info.automation_id == "srch-val"]
        doc_boxes = [item for item in side_list if item.element_info.control_type == "Document"]
        reservation_doc_boxes = [item for item in side_list if item.element_info.control_type == "Document"
                                    and item.element_info.automation_id == "reservation"]
        if find_name == "bookmark_btn":
            return button_boxes[0]
        if find_name == "doctor_filter_list":
            return list_boxes[0]
        if find_name == "insurance_filter_list":
            return list_boxes[1]
        if find_name == "search_edit":
            return Edit_boxes[0]
        if find_name == "notice_group":
            return doc_boxes[0].children()
        if find_name == "reservation_list":
            return doc_boxes[1].children()
        if find_name == "search_btn":
            return search_btn
        if find_name == "today_btn":
            return today_btn
        if find_name == "reservation_group":
            return reservation_doc_boxes
        
    def get_side_user_fliter(self):
        return
    
    def set_notice(self, set_value):
        """공지사항 입력"""
        notice_group = self.side_find_field("notice_group")
        for group_items in notice_group:
            print(group_items)
        return
    
    def get_notice(self, compare_value):
        """입력된 공지사항 확인"""
        return