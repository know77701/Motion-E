from datetime import datetime

from pywinauto import Desktop
from pywinauto.keyboard import send_keys

from locators.dashboard_locators import DashboardLocators
from locators.side_field_locators import SideFieldLocators
from pages.base_page import *
from utils.app_manager import AppManger
from utils.element_finder import *


class SidePage:
    def __init__(self):
        app = AppManger()
        app_title = app.version_search(DashboardLocators.MAIN_FORM_TITLE)
        self.side_window = Desktop(backend="uia").window(title=app_title)
        self.base_page = BasePage(app)
        
        # self.dashboard_reset();
        # self.side_field = self.base_page.find_element(auto_id=SideFieldLocators.SIDE_GROUP)
        
    # def dashboard_reset(self):
    #     self.base_page.dashboard_reset(self.side_window)
    #     return
    
    def get_side_field(self):
        """사이드 필드 객체 가져오기"""
        return self.side_window.child_window(class_name="Chrome_RenderWidgetHostHWND").wrapper_object()

    def side_find_field(self, find_name):
        """사이드 영역 객체 찾기"""
        side_field = self.get_side_field()
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
                return doc_boxes[0]
            if find_name == "reservation_list":
                return doc_boxes[1].children()
            if find_name == "reservation_group":
                return next((item for item in side_list if item.element_info.control_type == "Document" 
                             and item.element_info.automation_id == "reservation"), None)
    
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
            for group_items in notice_group.children():
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
        """입력된 공지사항 확인"""
        return_arr = []
        result = self.side_find_field("notice_group")
        if result:
            for group_item in result.children():
                if group_item.element_info.control_type == "List":
                    return_arr.extend([items.children() for items in group_item.children()])
            return return_arr
        else:
            print("등록 된 공지사항이 없습니다.")
    
    # 타임비교 코드 공통함수로 변경
    def compare_notice(self, notice, compare_time):
        """공지사항 비교 확인"""
        result = self.get_single_notice(notice)
        if not result == []:
            result_time = result[0][0].window_text()
            
            time_format = "%Y-%m-%d %H:%M:%S"
            compare_dt = datetime.strptime(compare_time, time_format)
            result_dt = datetime.strptime(result_time, time_format)

            time_diff = abs((compare_dt - result_dt).total_seconds())
            
            if not time_diff <= 2:
                print(f"작성 된 시간이 일치하지 않습니다. {time_diff}")
                return False
            return True

    def get_single_notice(self,notice):
        """작성된 공지사항 객체 찾기"""
        return_data = self.get_notice()
        return [sub_list for sub_list in return_data if any(notice in str(item) for item in sub_list)]

    def get_notice_update_form(self):
        """업데이트 폼 가져오기"""
        return_data = self.get_notice()
        for data_list in return_data:
            for item in data_list:
                if item.element_info.control_type == "Edit":
                    return data_list

    def update_notice(self, notice):
        """공지사항 수정"""
        result = self.get_single_notice(notice)
        edit_form = None
        update_save_btn = None
        if result is not []:
            for el in result:
                for item in el:
                    if item.element_info.control_type == "Text" and item.element_info.name == notice:
                        item.click_input()
                        time.sleep(0.5)
                        break
                    
        update_notice_form = self.get_notice_update_form()
        if update_notice_form is not []:
            for element_list in update_notice_form:
                if element_list.element_info.control_type == "Edit":
                    edit_form = element_list
                if (element_list.element_info.control_type == "Button"
                    and element_list.element_info.name == "저장"):
                    update_save_btn = element_list
                            
        edit_form.click_input()  # 클릭
        edit_form.set_focus()  # 포커스 맞추기
        edit_form.type_keys("^a{BACKSPACE}")  # 기존 내용 삭제
        edit_form.type_keys("업데이트", with_spaces=True)  # 새로운 내용 입력
        time.sleep(0.5)
        update_save_btn.click_input()  # 저장 버튼 클릭
        
    # 삭제객체 다건있을경우 시간비교 추가 필요    
    def delete_notice(self, notice):
        """공지사항 삭제"""
        result = self.get_single_notice(notice)
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
                        if item.element_info.name == notice:
                            time_text = item.window_text()
                        else:
                            content_text = item.window_text()
            
            close_btn.click()
            return_children = self.get_popup_field()
            if return_children:
                if (return_children[0].element_info.control_type == "Button"
                    and return_children[0].element_info.name == "예"):
                        return_children[0].click()
                        if self.compare_notice(content_text, time_text):
                            print("공지사항이 삭제되지 않았습니다.")
            else:
                print("삭제 버튼을 찾을 수 없습니다.")
        else:
            print("등록된 공지사항이 없습니다.")
        
    def search_user(self, username):
        """유저 검색하기"""
        search_edit = self.side_find_field("search_edit")
        search_button = self.side_find_field("search_btn")
        
        if search_edit:
            search_edit.set_focus()
            search_edit.set_text("")
            search_edit.set_text(username)
            if search_button:
                search_button.click()
    
    def get_search_field(self):
        """검색영역 가져오기"""
        get_srh_list = self.side_find_field("search-list")
        return get_srh_list.children()
        
    def get_child_list(self, object_list):
        """검색영역 리스트 가져오기"""
        list_items = []
        for list_item in object_list:
            for items in list_item.children():
                list_items.append(items)
        return list_items
    
    def get_search_user_list(self):
        """검색영역 유저리스트 가져오기"""
        search_user_list = self.get_search_field()
        list_object = self.get_child_list(search_user_list)
        return list_object

    def compare_user_list(self, user_list, username=None, chart_number=None):
        """검색 유저 비교 및 결과 리턴"""
        for list_item in user_list:
            for item in list_item.children():
                if item.element_info.control_type != "Text":
                    continue

                name = item.element_info.name
                if username and chart_number:
                    if username in name:
                        continue
                    if chart_number in name:
                        return list_item
                elif username:
                    if username in name:
                        return list_item
                elif chart_number:
                    if chart_number in name:
                        return list_item
                    
    def compare_search_user(self, username=None, chart_number=None):
        """검색 환자 리턴"""
        user_list = self.get_search_user_list()
        if username is not None or chart_number is not None:
            compare_user =  self.compare_user_list(user_list, username, chart_number)
            if compare_user is []:
                print("등록된 유저를 찾을 수 없습니다.")
            else:
                return compare_user
        else:
            print(f"환자명 / 차트번호가 입력되지 않았습니다.")
            
    def search_get_button(self,username, chart_number):
        """검색 환자 버튼 가져오기"""
        select_user = self.compare_search_user(username, chart_number)
        return ElementFinder.find_buttons(select_user.children())
            
    def search_user_reserve(self,username=None, chart_number=None):
        """검색 환자 예약화면 진입"""
        buttons = self.search_get_button(username,chart_number) 
        for el in buttons:
            if el.element_info.name == "예약하기":
                el.click()
    
    def search_user_receive(self, username=None, chart_number=None):
        """검색 환자 접수화면 진입"""
        buttons = self.search_get_button(username, chart_number)
        for el in buttons:
            if el.element_info.name == "접수하기":
                el.click()
    
    def save_user_popup(self):
        return