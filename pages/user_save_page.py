import time

from pywinauto import Desktop

from dto.user_dto import UserDTO
from locators.dashboard_locators import DashboardLocators
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class UserSavePage():
    def __init__(self, app_manger = AppManger):
        self.app_manger = app_manger

    def get_save_user_field(self):
        """고객 등록 팝업 가져오기"""
        app_title = self.app_manger.version_search(DashboardLocators.MAIN_FORM_TITLE)
        side_window = Desktop(backend="uia").window(title=app_title)
        popup_field = ElementFinder.find_element(side_window, title="고객등록", auto_id="FrmRegPatInfo",control_type="Window")
        
        time.sleep(1.5)
        popup_field.children()[0].set_focus()
        return popup_field.children()[0]
    
    def get_popup_button_field(self, find_name):
        """고객등록 팝업 버튼 가져오기"""
        pane_list = self.get_save_user_field()
        button_field = pane_list.children()[2]
        if find_name in ["저장", "저장+예약", "저장+접수"]:
            btn = ElementFinder.find_button_by_name(button_field.children(), find_name)
            return btn
        
    def get_popup_edit_field(self):
        """고객등록 팝업 input 가져오기"""
        pane_list = self.get_save_user_field()
        pane_field = pane_list.children()[0]

        edit_fields = ["TxtChartNo", "TxtPatNm"]
        jno_fields = ["TxtPatJno1", "TxtPatJno2"]
        mobile_fields = ["TxtMobileNo1", "TxtMobileNo2", "TxtMobileNo3"]

        edit_arr = [ElementFinder.find_edit_by_automation_id(pane_field.children(), field) for field in edit_fields]
        jno_arr = [ElementFinder.find_edit_by_automation_id(pane_field.children(), field) for field in jno_fields]
        mobile_number_arr = [ElementFinder.find_edit_by_automation_id(pane_field.children(), field) for field in mobile_fields]

        edit_arr.append(jno_arr)
        edit_arr.append(mobile_number_arr)
        return edit_arr

    def user_info_write(self, userDto : UserDTO):
        """고객등록 유저 정보 입력"""
        edit_list = self.get_popup_edit_field()
        
        chart_no = edit_list[0].element_info.name
        name = userDto.name
        jno = userDto.jno
        mobile_no = userDto.mobile_no
        
        save_user_dto = UserDTO(chart_no=chart_no, name=name, jno=jno, mobile_no=mobile_no)
        
        if name: edit_list[1].set_text(name)
        
        if jno: 
            edit_list[2][0].set_text(jno[0:6])
            edit_list[2][1].set_text(jno[7:14])
        
        if mobile_no:
            if len(mobile_no) == 13:
                edit_list[3][0].set_text(mobile_no[0:3])
                edit_list[3][1].set_text(mobile_no[4:8])
                edit_list[3][2].set_text(mobile_no[9:13])
                
            elif len(mobile_no) == 11:
                edit_list[3][0].set_text(mobile_no[0:3])
                edit_list[3][1].set_text(mobile_no[4:8])
                edit_list[3][2].set_text(mobile_no[9:11])
        
        if save_user_dto:
            return save_user_dto
        
        return None
        
    
    def user_save_and_proceed(self, receive=False, reserve=False):
        """고객등록 저장"""
        if receive:
            save_button = self.get_popup_button_field("저장+접수")
        elif reserve:
            save_button = self.get_popup_button_field("저장+예약")
        else:
            save_button = self.get_popup_button_field("저장")
            
        if save_button:
            ElementFinder.click(save_button)