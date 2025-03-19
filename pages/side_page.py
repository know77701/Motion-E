from datetime import datetime

from pywinauto import Desktop
from pywinauto.keyboard import send_keys

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
            return doc_boxes[0]
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
    
    def save_notice(self, set_value):
        """공지사항 입력"""
        notice_group = self.side_find_field("notice_group")
        for group_items in notice_group.children():
            if group_items.element_info.control_type == "Edit":
                group_items.set_text(set_value)
                time.sleep(0.5)
                group_items.set_focus()
                send_keys("{ENTER}")
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        
    def get_notice(self):
        """입력된 공지사항 확인"""
        return_arr = []
        notice_list = self.side_find_field("notice_group")
        for group_item in notice_list.children():
            if group_item.element_info.control_type == "List":
                for items in group_item.children():
                    return_arr.append(items.children())
        return return_arr
    
    def compare_notice(self, notice, compare_time):
        """공지사항 비교 확인"""
        return_data = self.get_notice()
        result = [sub_list for sub_list in return_data if any(notice in str(item) for item in sub_list)]
        result_time = result[0][0].window_text()
        
        time_format = "%Y-%m-%d %H:%M:%S"
        compare_dt = datetime.strptime(compare_time, time_format)
        result_dt = datetime.strptime(result_time, time_format)

        time_diff = abs((compare_dt - result_dt).total_seconds())
        
        if not time_diff <= 2:
            print(f"작성 된 시간이 일치하지 않습니다. {time_diff}")
        
        if not result:
            print("작성 된 공지사항이 존재하지 않습니다.")
    
    def delete_notice(self, notice):
        return_data = self.get_notice()
        result = [sub_list for sub_list in return_data if any(notice in str(item) for item in sub_list)]
        
        for sub_list in result:
            for item in sub_list:
                if (item.element_info.control_type == "Button" 
                    and item.element_info.name == "닫기"):
                    item.click()