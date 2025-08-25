import re

import pytest

from locators.dashboard_locators import DashboardLocators
from utils.element_finder import ElementFinder


class DashBoardPage():
    def __init__(self, app_manger):
        self.app_manger = app_manger
        self.app_title = self.app_manger.version_search(DashboardLocators.MAIN_FORM_TITLE)
        self.parent_field = ElementFinder.get_chrome_field(self.app_title)
        
    
    def find_field(self, find_name):
        name_map = {
            DashboardLocators.RESERVATION_FIELD_NAME: DashboardLocators.CANCEL_FIELD_NAME,
            DashboardLocators.RECEPTION_FIELD_NAME: DashboardLocators.CONSULTATION_FIELD_NAME,
            DashboardLocators.PAYMENT_FIELD_NAME: DashboardLocators.COMPLETION_FIELD_NAME,
            DashboardLocators.TREATMENT_FIELD_NAME: DashboardLocators.ELAPSED_TIME_FIELD_NAME
        }
        
        dashboard_field = ElementFinder.find_documents(self.parent_field.children())
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
    
    def find_user_search(self, user_name):
        try:
            self.parent_field.set_focus()
        except Exception as e:
            print(f"포커싱을 할수 없습니다. : {e}")
        
        user_find_window = self.open_user_search_popup()
        search_edit, search_btn =self.get_user_search_controls(user_find_window)
        self.perform_user_search(search_edit, search_btn,user_name)
    
    def open_user_search_popup(self):
        ElementFinder.send_key("^F")
        return ElementFinder.get_find_user_field(self.app_title)

    def get_user_search_controls(self, user_find_window):
        window_items = ElementFinder.recursive_children(user_find_window.children(), 0, 2)
        search_edit = ElementFinder.find_edit_by_automation_id(window_items,DashboardLocators.SEARCH_BOX_AUTOMATION_ID)
        search_btn = ElementFinder.find_button_by_auto_id(window_items, DashboardLocators.SEARCH_BUTTON_AUTOMATION_ID)
        return search_edit, search_btn

    def perform_user_search(self, search_edit, search_btn, user_name):
        if search_edit:
            ElementFinder.input_text(search_edit, user_name)
        if search_btn:
            ElementFinder.click(search_btn)
    

    def get_treatment_and_payment_field_user_list(self, find_name):
        reservation_list_field = self.find_field(find_name)
        customer_blocks = []
        current_block = []
        
        if not reservation_list_field:
            return []

        for el in reservation_list_field.children():
            name = el.element_info.name.strip()

            if self.time_string(name):
                if current_block:
                    customer_blocks.append(current_block)
                current_block = [el]
                continue
            current_block.append(el)

        if current_block:
            customer_blocks.append(current_block)
        return customer_blocks
    
    def get_reservation_and_reception_field_user_list(self, find_name):
        reservation_list_field = self.find_field(find_name)
        
        if reservation_list_field != None:
            
            for el in reservation_list_field.children():
                ctrl_type = el.friendly_class_name()
                auto_id = el.element_info.automation_id
                if find_name == DashboardLocators.RESERVATION_FIELD_NAME:
                    
                    if ctrl_type == "ListBox" and auto_id == DashboardLocators.RESERVATION_LIST_AUTO_ID:
                        return el
                if find_name == DashboardLocators.CANCEL_FIELD_NAME:
                    if ctrl_type == "ListBox" and auto_id == DashboardLocators.NOSHOW_LIST_AUTO_ID:
                        return el
                if find_name == DashboardLocators.RECEPTION_FIELD_NAME:
                    if ctrl_type == "ListBox":
                        return el
                    
    def _has_chart_no(self, elements, chart_no):
        """요소 리스트에 chart_no가 포함되어 있는지 여부 반환"""
        return any(el.element_info.name == chart_no for el in elements)

    def get_field_user_list(self, field_name, chart_no):
        target_items = []

        if field_name in [DashboardLocators.RESERVATION_FIELD_NAME, DashboardLocators.RECEPTION_FIELD_NAME, DashboardLocators.CANCEL_FIELD_NAME]:
            list_container = self.get_reservation_and_reception_field_user_list(field_name)
            if list_container is None:
                return []
            for item in list_container.children():
                if self._has_chart_no(item.children(), chart_no):
                    target_items.append(item)

        elif field_name in [DashboardLocators.TREATMENT_FIELD_NAME, DashboardLocators.PAYMENT_FIELD_NAME]:
            customer_blocks = self.get_treatment_and_payment_field_user_list(field_name)
            for block in customer_blocks:
                if self._has_chart_no(block, chart_no):
                    target_items.append(block)
        else:
            print("찾으려는 대시보드 영역을 정확히 입력해주세요.")
            return None
        return target_items
    
    def get_reservation_list(self,chart_no):
        field_user_list = self.get_field_user_list(DashboardLocators.RESERVATION_FIELD_NAME, chart_no)
        return self.validate_user_exists(field_user_list)
        
    def get_reception_list(self,chart_no):
        field_user_list = self.get_field_user_list(DashboardLocators.RECEPTION_FIELD_NAME, chart_no)
        return self.validate_user_exists(field_user_list)
            
    def get_treatment_list(self,chart_no):
        field_user_list = self.get_field_user_list(DashboardLocators.TREATMENT_FIELD_NAME, chart_no)
        return self.validate_user_exists(field_user_list)
            
    def get_payment_list(self,chart_no):
        field_user_list = self.get_field_user_list(DashboardLocators.PAYMENT_FIELD_NAME, chart_no)
        return self.validate_user_exists(field_user_list)

    def get_cancle_button(self, find_name,chart_no):
        find_user = self.get_field_user_list(find_name, chart_no)
        cancle_btn = ElementFinder.list_in_find_button_by_name(find_user, DashboardLocators.CLOSE_BUTTON_NAME)
        if cancle_btn:
            ElementFinder.click(cancle_btn)
            return True
        else:
            return False
    
    def cancle_web_popup_action(self):
        custom_element = ElementFinder.find_custom(self.parent_field.children())
        group_list = ElementFinder.find_group_list(custom_element.children())
        result = False
        if group_list:
            for group_item in group_list:
                cancel_button = ElementFinder.find_button_by_name(group_item.children(), DashboardLocators.YES_BUTTON_NAME)
                if cancel_button:
                    ElementFinder.click(cancel_button)
                    result = True
                    return result
            return result
        else:
            return result
    
    def reservation_cancel_popup_control(self):
        cancel_btn = ElementFinder.find_button_by_name(self.parent_field.children(), "저장") # This should be a locator
        if cancel_btn:
            ElementFinder.click(cancel_btn)
        
    def reception_cancel(self, chart_no):
        self.get_cancle_button(DashboardLocators.RECEPTION_FIELD_NAME,chart_no)
        self.cancle_web_popup_action()
        
    def validate_user_exists(self, user_list):
        if user_list:
            return True
        return False
    
    def open_chart(self,field_name,chart_no, time):
        field_user_list = self.get_field_user_list(field_name, chart_no)
        arr = []
        
        for el in field_user_list:
            if ElementFinder.find_text_by_name(el.children(), time):
                arr = el
                break
            
        print(arr)
        if not arr: 
            print("해당하는 환자가 존재하지 않습니다.")
            return None
        else: 
            user_chart_no_text = ElementFinder.find_text_by_name(arr.children(), chart_no)

            if user_chart_no_text:
                user_chart_no_text.click_input()
                return user_chart_no_text