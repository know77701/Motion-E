import random
import time
from datetime import datetime

from pywinauto import Desktop
from pywinauto.keyboard import send_keys

from dto.user_dto import UserDTO
from locators.dashboard_locators import DashboardLocators
from locators.side_field_locators import SideFieldLocators
from pages.base_page import *
from utils.app_manager import AppManger
from utils.element_finder import *


class SidePage:
    def __init__(self):
        self.finder = ElementFinder()

        
        # self.dashboard_reset();
        # self.side_field = self.base_page.find_element(auto_id=SideFieldLocators.SIDE_GROUP)
        
    # def dashboard_reset(self):
    #     self.base_page.dashboard_reset(self.side_window)
    #     return

    def side_find_field(self, find_name):
        """사이드 영역 객체 찾기"""
        side_field = self.finder.get_chrome_field()
        side_list = side_field.children()
    
        if find_name in ["bookmark_btn", "search_btn", "today_btn"]:
            button_boxes = ElementFinder.find_buttons(side_list)
            if find_name == "bookmark_btn":
                return button_boxes[0]
            if find_name == "search_btn":
                return ElementFinder.find_button_by_name(side_list, "검색")
            if find_name == "today_btn":
                return ElementFinder.find_button_by_name(side_list, "오늘")
        
        if find_name in ["doctor_filter_list", "insurance_filter_list"]:
            list_boxes = ElementFinder.find_lists(side_list)
            if find_name == "doctor_filter_list":
                return list_boxes[0]
            if find_name == "insurance_filter_list":
                return list_boxes[1]
        
        if find_name == "search_edit":
            return ElementFinder.find_edit_by_automation_id(side_list, "srch-val")
        
        if find_name in ["notice_group", "reservation_list", "reservation_group", "search-list"]:
            doc_boxes = ElementFinder.find_documents(side_list)
            if find_name in ["notice_group", "search-list"]:
                return doc_boxes[0].children()
            if find_name == "reservation_list":
                return doc_boxes[1].children()
            if find_name == "reservation_group":
                return ElementFinder.find_documents_by_automation_id(side_list,"reservation")
    
        if find_name in ["reserve_list"]:
            return ElementFinder.find_group_by_automation_id(side_list,"scTab")
    
    
    def get_popup_field(self):
        """대시보드 웹 팝업 찾기"""
        side_field = self.side_window.child_window(class_name="Chrome_RenderWidgetHostHWND").wrapper_object()
        return_data = side_field.children()
        custom_wrapper = None
        popup_btn_list = []
        
        for el in return_data:
            if el.element_info.control_type == "Custom":
                custom_wrapper = el
                
        for wrapper_item in custom_wrapper.children():
            if wrapper_item.element_info.control_type == "Group":
                for items in wrapper_item.children():
                    if items.element_info.control_type == "Button":
                        popup_btn_list.append(items)
        
        return popup_btn_list


    def save_notice(self, set_value):
        """공지사항 입력"""
        notice_group = self.side_find_field("notice_group")
        if notice_group:
            for group_items in notice_group:
                if group_items.element_info.control_type == "Edit":
                    group_items.set_text("")
                    group_items.set_text(set_value)
                    time.sleep(0.5)
                    group_items.set_focus()
                    send_keys("{ENTER}")
                    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        else:
            print("공지사항 등록 폼을 찾을 수 없습니다.")
        
        
    def get_notice(self):
        """모든 공지사항 가져오기"""
        return_arr = []
        result = self.side_find_field("notice_group")
        if result:
            for group_item in result:
                if group_item.element_info.control_type == "List":
                    return_arr.extend([items.children() for items in group_item.children()])
            return return_arr
        else:
            print("등록 된 공지사항이 없습니다.")
    
    
    def get_single_notice(self,notice_content, create_time):
        """특정 공지사항 객체 찾기"""
        return_data = self.get_notice()
        filtered_data = []
        time_format = "%Y-%m-%d %H:%M:%S"
        create_dt = datetime.strptime(create_time, time_format)

        for sub_list in return_data:
            has_notice_content = False
            has_create_time = False

            for item in sub_list:
                item_name = getattr(item.element_info, "name", "")
                if notice_content in item_name:
                    has_notice_content = True
                try:
                    item_dt = datetime.strptime(item_name, time_format)
                    time_diff = abs((create_dt - item_dt).total_seconds())

                    if time_diff <= 2:
                        has_create_time = True
                except ValueError:
                    continue
            if has_notice_content and has_create_time:
                filtered_data.append(sub_list)
        return filtered_data
    

    def compare_notice(self, notice_content, compare_time):
        """공지사항 비교 확인"""
        result = self.get_single_notice(notice_content, compare_time)
        result_value = True
        if not result == []:
            if hasattr(result[0][0], 'window_text'):
                result_time = result[0][0].window_text()
            else:
                result_time = result[0][0]
            
            time_format = "%Y-%m-%d %H:%M:%S"
            compare_dt = datetime.strptime(compare_time, time_format)
            result_dt = datetime.strptime(result_time, time_format)

            time_diff = abs((compare_dt - result_dt).total_seconds())
            
            if not time_diff <= 2:
                print(f"작성 된 시간이 일치하지 않습니다. {time_diff}")
                result_value = False
                return  result_value
            return result_value

    def get_notice_update_form(self):
        """업데이트 폼 가져오기"""
        return_data = self.get_notice()
        for data_list in return_data:
            for item in data_list:
                if item.element_info.control_type == "Edit":
                    return data_list

    def update_notice(self, notice_content,create_time,update_content):
        """공지사항 수정"""
        result = self.get_single_notice(notice_content,create_time)
        update_save_btn = None
        if result is not []:
            for el in result:
                for item in el:
                    if item.element_info.control_type == "Text" and item.element_info.name == notice_content:
                        item.click_input()
                        time.sleep(0.5)
                        break
                    
        update_notice_form = self.get_notice_update_form()
        if update_notice_form is not [] and update_notice_form is not None:
            for element_list in update_notice_form:
                if (element_list.element_info.control_type == "Button"
                    and element_list.element_info.name == "저장"):
                    update_save_btn = element_list
        time.sleep(0.5)
        send_keys("^a{BACKSPACE}")
        send_keys(update_content)
        time.sleep(0.5)
        update_save_btn.click_input()
        
        
    # 삭제객체 다건있을경우 시간비교 추가 필요    
    def delete_notice(self, notice_content,create_time):
        """공지사항 삭제"""
        result = self.get_single_notice(notice_content, create_time)
        close_btn = None
        time_text = None
        content_text = None
        
        if not result == []:
            for sub_list in result:
                for item in sub_list:
                    if (item.element_info.control_type == "Button" 
                        and item.element_info.name == "닫기"):
                            close_btn = item
                    if (item.element_info.control_type == "Text"):
                        if item.element_info.name == notice_content:
                            time_text = item.window_text()
                        else:
                            content_text = item.window_text()
            
            close_btn.click()
            return_children = self.get_popup_field()
            if return_children:
                if (return_children[0].element_info.control_type == "Button"
                    and return_children[0].element_info.name == "예"):
                        return_children[0].click()
            else:
                print("삭제 버튼을 찾을 수 없습니다.")
        else:
            print("등록된 공지사항이 없습니다.")
        
    def search_user(self, search_text):
        """유저 검색하기"""
        search_edit = self.side_find_field("search_edit")
        search_button = self.side_find_field("search_btn")
        
        if search_edit:
            search_edit.set_focus()
            search_edit.set_text("")
            search_edit.set_text(search_text)
            if search_button:
                search_button.click()
    
    def get_child_list(self, object_list):
        """검색영역 리스트 가져오기"""
        list_items = []
        for list_item in object_list:
            for items in list_item.children():
                list_items.append(items)
        return list_items
    
    def get_search_user_list(self):
        """검색영역 유저리스트 가져오기"""
        search_user_list = self.side_find_field("search-list")
        list_object = self.get_child_list(search_user_list)
        return list_object

    def compare_user_list(self, user_list, UserDTO : UserDTO):
        """검색 유저 비교 및 결과 리턴"""
        for list_item in user_list:
            for item in list_item.children():
                if item.element_info.control_type != "Text":
                    continue

                name = item.element_info.name
                if UserDTO.name and UserDTO.chart_no:
                    if UserDTO.name in name:
                        continue
                    if UserDTO.chart_no in name:
                        return list_item
                elif UserDTO.name:
                    if UserDTO.name in name:
                        return list_item
                elif UserDTO.chart_no:
                    if UserDTO.chart_no in name:
                        return list_item
                    
    def compare_search_user(self,UserDTO : UserDTO):
        """검색 환자 리턴"""
        user_list = self.get_search_user_list()
        
        if UserDTO.name is not None or UserDTO.chart_no is not None:
            compare_user =  self.compare_user_list(user_list, UserDTO)
            if compare_user is []:
                print("등록된 유저를 찾을 수 없습니다.")
            else:
                return compare_user
        else:
            print(f"환자명 / 차트번호가 입력되지 않았습니다.")
            
    def search_get_button(self, UserDTO : UserDTO):
        """검색 환자 버튼 가져오기"""
        select_user = self.compare_search_user(UserDTO)
        return ElementFinder.find_buttons(select_user.children())
            
    def search_user_reserve(self,UserDTO : UserDTO):
        """검색 환자 예약화면 진입"""
        buttons = self.search_get_button(UserDTO) 
        for el in buttons:
            if el.element_info.name == "예약하기":
                el.click()
    
    def search_user_receive(self, UserDTO : UserDTO):
        """검색 환자 접수화면 진입"""
        buttons = self.search_get_button(UserDTO)
        for el in buttons:
            if el.element_info.name == "접수하기":
                el.click()
    
    def save_user_popup(self):
        """유저 저장 팝업 진입"""
        search_user_list = self.side_find_field("search_list")
        for items in search_user_list:
            if items.element_info.control_type == "Button" and items.element_info.name == "환자 등록 후 예약":
                items.click()
       
    def combo_item_retrun(self, combo_list):
        """예약시간 랜덤 선택"""
        combo_list.set_focus()
        time.sleep(0.5)
        combo_list.expand()
        time.sleep(0.5)
        
        list_items = combo_list.children()
        combo_items = list_items[0].children()
        label, real_items = combo_items[0].element_info.name, combo_items[1:]

        now = datetime.now()
        current_hour = now.hour
        
        while True:
            random_item = random.choice(real_items)
            select_time = random_item.element_info.name

            if not select_time.isdigit():
                continue
            if label == "시간":
                if int(select_time) <= current_hour:
                    continue
            break
        send_keys(select_time)
        
                
    def get_reserve_elements(self, find_type: str):
        """
            해당 타입의 예약 요소들을 리턴
            ComboBox, Edit, List, Text, Button
        """
        reserve_list = self.side_find_field("reservation_group")
        return [
            item for item in reserve_list.children()
            if item.element_info.control_type == find_type
        ]

        
    def reserve_user(self, UserDTO: UserDTO):
        """유저 예약"""
        combo_list = self.get_reserve_elements("ComboBox")
        text_list = self.get_reserve_elements("Text")
        btn_list = self.get_reserve_elements("Button")
        
        if all(
            element.element_info.name not in [UserDTO.chart_no, UserDTO.name, UserDTO.mobile_no]
            for element in text_list
        ):print("예약 환자의 정보를 확인하세요")
        
        self.combo_item_retrun(combo_list[0])
        self.combo_item_retrun(combo_list[1])
        
        reserve_btn = btn_list[0]
        reserve_btn.click()
    
    def reserve_user_with_time(self):
        return 