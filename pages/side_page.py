import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from pywinauto import Desktop
from pywinauto.keyboard import send_keys

from dto.user_dto import UserDTO
from locators.dashboard_locators import DashboardLocators
from pages.base_page import *
from utils.app_manager import AppManger
from utils.element_finder import *


class SidePage:
    def __init__(self, app_manger : AppManger):
        self.app_manger = app_manger
        self.app_title = self.app_manger.version_search(DashboardLocators.MAIN_FORM_TITLE,auto_id=None)
        
    # def dashboard_reset(self):
    #     self.base_page.dashboard_reset(self.side_window)
    #     return

    def side_find_field(self, find_name):
        """사이드 영역 객체 찾기"""
        side_field = ElementFinder.get_chrome_field(self.app_title)
        side_list = side_field.children()
        
        if find_name in ["bookmark_btn", "search_btn", "today_btn"]:
            button_boxes = ElementFinder.find_buttons(side_list)
            if find_name == "bookmark_btn":
                return button_boxes[0]
            if find_name == "search_btn":
                return ElementFinder.find_button_by_name(side_list, "검색")
            if find_name == "today_btn":
                return ElementFinder.find_button_by_name(side_list, "오늘")
        
        elif find_name in ["doctor_filter_list", "insurance_filter_list"]:
            list_boxes = ElementFinder.find_lists(side_list)
            if find_name == "doctor_filter_list":
                return list_boxes[0]
            if find_name == "insurance_filter_list":
                return list_boxes[1]
        
        elif find_name == "search_edit":
            return ElementFinder.find_edit_by_automation_id(side_list, "srch-val")
        
        elif find_name in ["notice_group", "reservation_list", "reservation_group", "search_list"]:
            doc_boxes = ElementFinder.find_documents(side_list)

            if find_name in ["notice_group", "search_list"]:
                return doc_boxes[0].children()
            elif find_name == "reservation_list":
                return doc_boxes[1].children()
            elif find_name == "reservation_group":
                return ElementFinder.find_documents_by_automation_id(side_list,"reservation")
    
        elif find_name in ["reserve_list"]:
            return ElementFinder.find_group_by_automation_id(side_list,"scTab")
    
    
    def get_popup_field(self):
        """대시보드 웹 팝업 찾기"""
        side_field = ElementFinder.get_chrome_field(self.app_title)
        custom_wrapper = ElementFinder.find_customs(side_field.children())
        for item in custom_wrapper:
            group_list = ElementFinder.find_group_list(item.children())
        
        return group_list

    def save_notice(self, set_value):
        """공지사항 입력"""
        notice_group = self.side_find_field("notice_group")
        if notice_group:
            edit_item = ElementFinder.find_edit(notice_group)
            edit_item.set_text("")
            edit_item.set_text(set_value)
            time.sleep(1)
            edit_item.set_focus()
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
            if ElementFinder.find_edit(data_list):
                return data_list

    def update_notice(self, notice_content,create_time,update_content):
        """공지사항 수정"""
        result = self.get_single_notice(notice_content,create_time)
        update_save_btn = None
        if result is not []:
            
            for el in result:
                item = ElementFinder.find_text_by_name(el, notice_content)
                if item:
                    item.click_input()
                    time.sleep(0.5)
                    break
                    
        update_notice_form = self.get_notice_update_form()
        if update_notice_form is not [] and update_notice_form is not None:
            update_save_btn = ElementFinder.find_button_by_name(update_notice_form, "저장")
        time.sleep(0.5)
        send_keys("^a{BACKSPACE}")
        send_keys(update_content)
        time.sleep(0.5)
        if update_save_btn:
            ElementFinder.click(update_save_btn)
        
    def delete_notice(self, notice_content,create_time):
        """공지사항 삭제"""
        result = self.get_single_notice(notice_content, create_time)
        close_btn = None
        time_text = None
        content_text = None
        
        time.sleep(1)
        if not result == []:
            for sub_list in result:
                close_btn = ElementFinder.find_button_by_name(sub_list, "닫기")
                time_text = ElementFinder.find_text_by_name(sub_list, notice_content)
                content_text = ElementFinder.find_text(sub_list)
                break

            if close_btn:
                ElementFinder.click(close_btn)
                
            time.sleep(1)
            web_popup_group_list = self.get_popup_field()

            if web_popup_group_list:
                for items in web_popup_group_list:
                    delete_btn = ElementFinder.find_button_by_name(items.children(), "예")
                    if delete_btn:
                        delete_btn.click()
                        break
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
                ElementFinder.click(search_button)
    
    def get_child_list(self, object_list):
        """검색영역 리스트 가져오기"""
        list_items = []
        for list_item in object_list:
            for items in list_item.children():
                list_items.append(items)
        return list_items
    
    def get_search_user_list(self):
        """검색영역 유저리스트 가져오기"""
        search_user_list = self.side_find_field("search_list")
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
        for button in buttons:
            if button.element_info.name == "예약하기":
                ElementFinder.click(button)
    
    def search_user_receive(self, UserDTO : UserDTO):
        """검색 환자 접수화면 진입"""
        buttons = self.search_get_button(UserDTO)
        for button in buttons:
            if button.element_info.name == "접수하기":
                ElementFinder.click(button)
    
    def get_save_user_popup(self):
        """유저 저장 팝업 진입"""
        search_user_list = self.side_find_field("search_list")
        save_reservation_btn = ElementFinder.find_button_by_name(search_user_list, "환자 등록 후 예약")
        if save_reservation_btn:
            ElementFinder.click(save_reservation_btn)
       
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
                
    def combo_item_retrun_test(self, combo_list):
        """예약시간 랜덤 선택"""
        combo_list.set_focus()
        time.sleep(0.5)
        combo_list.expand()
        time.sleep(0.5)
        list_items = combo_list.children()
        combo_items = list_items[0]
        label, real_items = combo_items.element_info.name, combo_items[1:]

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
    
    def reserve_user(self, UserDTO: UserDTO):
        """유저 예약"""
        time.sleep(1.5)
        reserve_list = self.side_find_field("reservation_group")
        if reserve_list:
            with ThreadPoolExecutor() as executor:
                combo_list = executor.submit(ElementFinder.find_combobox, reserve_list.children())
                text_list = executor.submit(ElementFinder.find_text, reserve_list.children())
                btn_list = executor.submit(ElementFinder.find_buttons, reserve_list.children())

                combo_arr = combo_list.result()
                text_arr = text_list.result()
                btn_arr = btn_list.result()
            
            if all(
                element.element_info.name not in [UserDTO.chart_no, UserDTO.name, UserDTO.mobile_no]
                for element in text_arr
            ):print("예약 환자의 정보를 확인하세요")
            
            time.sleep(0.5)
            
            for combo_item in combo_arr:
                self.combo_item_retrun_test(combo_item)
            
            reserve_btn = btn_arr[0]
            if reserve_btn:
                ElementFinder.click(reserve_btn)
                
            
    def reserve_user_with_time(self):
        return 