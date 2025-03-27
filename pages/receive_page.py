from pywinauto import Desktop

from locators.receive_locators import ReceiveLocators
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class ReceivePage:
    def __init__(self):
        app = AppManger()
        app_title = app.version_search(ReceiveLocators.RECEIVE_POPUP_TITLE)
        self.side_window = Desktop(backend="uia").window(title=app_title).wrapper_object()
    
    def get_popup_object(self, find_name):
        window_list = self.side_window.children()
        elements = [child for element in window_list for child in element.children()]
        
        if find_name in ["get_text_data"]:
            return ElementFinder.find_text(elements)
        if find_name in ["get_receive_btn"]:
            return ElementFinder.find_buttons(elements)
        if find_name in ["get_memo_edit"]:
            return ElementFinder.find_edit(elements)
        if find_name in ["get_dropbox"]:
            return ElementFinder.find_text(elements)
    
    def get_verify_popup_text(self, username=None, chart_number=None):
        text_elements = self.get_popup_object("get_text_data")
        result_data = False
        for el in text_elements:
            name = el.element_info.name
            if username and chart_number:
                if username in name:
                    continue
                if chart_number in name:
                    result_data = True
            elif username:
                if username in name:
                    result_data = True
            elif chart_number:
                if chart_number in chart_number:
                    result_data =True
        return result_data

    def verify_receive_info(self, username=None, chart_number=None):
        if not self.get_verify_popup_text(username, chart_number):
            print("접수팝업 환자 정보를 확인해주세요")

    def get_memo_edit(self):
        window_list = self.side_window.children()
        elements = [child for element in window_list for child in element.children()]
        edit_arr = []
        for i in elements:
            if i.element_info.control_type == "Pane":
                for el in i.children():
                    if el.element_info.control_type == "Edit" and el.element_info.automation_id != "txtAcpt_Dd":
                        edit_arr.append(el)
        return edit_arr

    def write_receive_memo(self, user_memo, receive_memo):
        edit_list = self.get_memo_edit()
        if edit_list:
            edit_list[0].set_text(user_memo)
            edit_list[1].set_text(receive_memo)
    
    def submit_receive(self):
        btn_list = self.get_popup_object("get_receive_btn")
        for btn in btn_list:
            if btn.element_info.name == "접수":
                btn.click()
                break
    