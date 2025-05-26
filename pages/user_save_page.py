import time
from concurrent.futures import ThreadPoolExecutor

from pywinauto import Desktop
from pywinauto.timings import TimeoutError, wait_until_passes

from dto.user_dto import UserDTO
from locators.dashboard_locators import DashboardLocators
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class UserSavePage():
    def __init__(self, app_manger = AppManger):
        self.app_manger = app_manger
        self.user_save_popup_field = None

    def get_save_user_field(self):
        app_title = self.app_manger.version_search(DashboardLocators.MAIN_FORM_TITLE)
        side_window = Desktop(backend="uia").window(title=app_title)
        try:
            time.sleep(1.5)
            popup_list = ElementFinder.find_element(side_window, title="고객등록", auto_id="FrmRegPatInfo",control_type="Window").wrapper_object()
        except TimeoutError:
            raise Exception("고객등록 팝업을 찾을 수 없습니다.")

        popup_list.children()[0].set_focus()
        time.sleep(1)
        self.user_save_popup_field = popup_list.children()[0]
        
    
    def get_popup_button_field(self, find_name):
        """고객등록 팝업 버튼 가져오기"""
        button_field = self.user_save_popup_field.children()[2]
        if find_name in ["저장", "저장+예약", "저장+접수"]:
            btn = ElementFinder.find_button_by_name(button_field.children(), find_name)
            return btn
    
    def get_chart_fields(self, pane_field):
        return ElementFinder.find_edits_by_automation_id(pane_field.children(), ["TxtChartNo"])

    def get_name_fields(self, pane_field):
        return ElementFinder.find_edits_by_automation_id(pane_field.children(), ["TxtPatNm"])

    def get_jno_fields(self, pane_field):
        return ElementFinder.find_edits_by_automation_id(pane_field.children(), ["TxtPatJno1", "TxtPatJno2"])

    def get_mobile_fields(self, pane_field):
        return ElementFinder.find_edits_by_automation_id(pane_field.children(), ["TxtMobileNo1", "TxtMobileNo2", "TxtMobileNo3"])

    def get_popup_edit_field(self):
        time.sleep(0.5)
        pane_field = self.user_save_popup_field.children()[0]
        with ThreadPoolExecutor() as executor:
            future_chart = executor.submit(self.get_chart_fields, pane_field) 
            future_name = executor.submit(self.get_name_fields, pane_field) 
            future_jno = executor.submit(self.get_jno_fields, pane_field)
            future_mobile = executor.submit(self.get_mobile_fields, pane_field)

            chart_fields = future_chart.result()
            name_fields = future_name.result()
            jno_fields = future_jno.result()
            mobile_fields = future_mobile.result()

        return chart_fields, name_fields,jno_fields, mobile_fields
    
    def input_name_info(self, edit_list, name):
        if name:
            ElementFinder.input_text(edit_list[0], name)
        else:
            assert False, "환자이름이 입력되지 않았습니다."

    def input_jno_info(self, edit_list, jno):
        if jno:
            ElementFinder.input_text(edit_list[0], jno[0:6])
            ElementFinder.input_text(edit_list[1], jno[7:14])
        else:
            assert False, "환자 주민번호가 입력되지않았습니다."

    def input_mobile_info(self, edit_list, mobile_no):
        if mobile_no:
            if len(mobile_no) == 13:
                ElementFinder.input_text(edit_list[0], mobile_no[0:3])
                ElementFinder.input_text(edit_list[1], mobile_no[4:8])
                ElementFinder.input_text(edit_list[2], mobile_no[9:13])
            elif len(mobile_no) == 11:
                ElementFinder.input_text(edit_list[0], mobile_no[0:3])
                ElementFinder.input_text(edit_list[1], mobile_no[4:7])
                ElementFinder.input_text(edit_list[2], mobile_no[7:11])
        else:
            assert False, "환자 핸드폰번호가 입력되지 않았습니다."
    
    def user_info_write(self, userDto: UserDTO):
        chart_fields, name_fields,jno_fields, mobile_fields = self.get_popup_edit_field()

        chart_no = chart_fields[0].element_info.name
        self.input_name_info(name_fields, userDto.name)
        self.input_jno_info(jno_fields, userDto.jno)
        self.input_mobile_info(mobile_fields, userDto.mobile_no)

        return UserDTO(
            chart_no=chart_no,
            name=userDto.name,
            jno=userDto.jno,
            mobile_no=userDto.mobile_no
        )
    
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