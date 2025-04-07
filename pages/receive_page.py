from pywinauto import Desktop

from dto.user_dto import UserDTO
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
    
    def get_compare_popup_text(self, user_dto : UserDTO):
        text_elements = self.get_popup_object("get_text_data")
        result_data = False
        for el in text_elements:
            name = el.element_info.name
            if user_dto.name and user_dto.chart_no:
                if user_dto.name in name:
                    continue
                if user_dto.chart_no in name:
                    result_data = True
            elif user_dto.name:
                if user_dto.name in name:
                    result_data = True
            elif user_dto.chart_no:
                if user_dto.chart_no in name:
                    result_data =True
        return result_data


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
    