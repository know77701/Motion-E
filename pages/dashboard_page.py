import re
import time

from utils.app_manager import AppManger
from utils.element_finder import ElementFinder
from locators.dashboard_locators import DashboardLocators



class DashBoardPage():
    def __init__(self, app_manger: AppManger):
        self.app_manger = app_manger
        self.app_title = self.app_manger.version_search(DashboardLocators.MAIN_FORM_TITLE)
        
    def find_field(self, find_name):
        name_map = {
            "예약": "부도",
            "접수": "상담",
            "수납": "완료",
            "시술": "경과시간"
        }
        parent_field = ElementFinder.get_chrome_field(self.app_title)
        dashboard_field = ElementFinder.find_documents(parent_field.children())
        keyword = name_map.get(find_name, None)
        
        for element_list in dashboard_field:
            for element in element_list.children():
                name = element.element_info.name.strip()
                
                if name == find_name:
                    continue
                
                if keyword and keyword == name:
                    return element_list
                
                if not keyword and name == find_name:
                    return element_list
                
        return None

    def time_string(self, name):
        return re.match(r"^\d{1,2}:\d{2}$", name) is not None

    def get_treatment_and_payment_field_user_list(self, find_name):
        reservation_list_field = self.find_field(find_name)
        customer_blocks,current_block,end_queue = [],[],[]
        collecting = False
        
        for el in reservation_list_field.children():
            name = el.element_info.name.strip()
            ctrl_type = el.friendly_class_name()

            if self.time_string(name):
                if current_block:
                    customer_blocks.append(current_block)
                current_block = [el]
                collecting = True
                end_queue = []
                continue

            if collecting:
                current_block.append(el)

                end_queue.append(ctrl_type)
                if len(end_queue) > 3:
                    end_queue.pop(0)

                if end_queue == ['ListBox', 'Table', 'ListBox']:
                    customer_blocks.append(current_block)
                    current_block = []
                    collecting = False
                    end_queue = []

        if current_block:
            customer_blocks.append(current_block)
        return customer_blocks
    
    def get_reservation_and_reception_field_user_list(self, find_name):
        reservation_list_field = self.find_field(find_name)
        
        if reservation_list_field != None:
            
            for el in reservation_list_field.children():
                ctrl_type = el.friendly_class_name()
                auto_id = el.element_info.automation_id
                
                if find_name == "예약":
                    if ctrl_type == "ListBox" and auto_id == "rsrv-list":
                        return el
                if find_name == "부도":
                    if ctrl_type == "ListBox" and auto_id == "nosh-list":
                        return el
                if find_name == "접수":
                    if ctrl_type == "ListBox":
                        return el
                    
    def _has_chart_no(self, elements, chart_no):
        """요소 리스트에 chart_no가 포함되어 있는지 여부 반환"""
        return any(el.element_info.name == chart_no for el in elements)

    def get_field_user_list(self, field_name, chart_no):
        target_items = []

        if field_name in ["예약", "접수", "부도"]:
            list_container = self.get_reservation_and_reception_field_user_list(field_name)
            if list_container is None:
                return []
            for item in list_container.children():
                if self._has_chart_no(item.children(), chart_no):
                    target_items.append(item)

        elif field_name in ["시술", "수납"]:
            customer_blocks = self.get_treatment_and_payment_field_user_list(field_name)
            for block in customer_blocks:
                if self._has_chart_no(block, chart_no):
                    target_items.append(block)
        else:
            print("찾으려는 대시보드 영역을 정확히 입력해주세요.")
            return None

        return target_items
    
    def get_reservation_list(self,chart_no):
        field_user_list = self.get_field_user_list("예약", chart_no)
        self.validate_user_exists(field_user_list)
        
    def get_reception_list(self,chart_no):
        field_user_list = self.get_field_user_list("접수", chart_no)
        self.validate_user_exists(field_user_list)
            
    def get_treatment_list(self,chart_no):
        field_user_list = self.get_field_user_list("시술", chart_no)
        self.validate_user_exists(field_user_list)
            
    def get_payment_list(self,chart_no):
        field_user_list = self.get_field_user_list("수납", chart_no)
        self.validate_user_exists(field_user_list)

    def get_cancle_button(self, find_name,chart_no):
        find_user = self.get_field_user_list(find_name, chart_no)
        cancle_btn = ElementFinder.list_in_find_button(find_user.children())
        
        if cancle_btn:
            ElementFinder.click(cancle_btn)
    
    def cancle_web_popup_action(self):
        parent_field = ElementFinder.get_chrome_field(self.app_title)
        custom_element = ElementFinder.find_custom(parent_field.children())
        group_list = ElementFinder.find_group_list(custom_element.children())
        for group_item in group_list:
            cancel_button = ElementFinder.find_button_by_name(group_item.children(), "예")
            if cancel_button:
                ElementFinder.click(cancel_button)
                return True
        return False
        
    def reservation_cancel(self,chart_no):
        self.get_cancle_button("예약",chart_no)
        parent_field = ElementFinder.get_chrome_field(self.app_title)
        cancel_btn = ElementFinder.find_button_by_name(parent_field.children(), "저장")
        if cancel_btn:
            ElementFinder.click(cancel_btn)
        
        self.cancle_web_popup_action()
        
    def reception_cancel(self, chart_no):
        self.get_cancle_button("접수",chart_no)
        self.cancle_web_popup_action()
        
    def validate_user_exists(self, user_list):
        if not user_list:
            return False
        return True
    
    def open_chart(self,chart_no):
        field_user_list = self.get_field_user_list("예약", chart_no)
        if field_user_list == []:
            print("해당하는 환자가 존재하지 않습니다.")
        user_chart_no_text = ElementFinder.find_text_by_name(field_user_list[0].children(), chart_no)
        user_chart_no_text.click_input()