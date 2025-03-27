from collections import deque

from pywinauto import Desktop

from locators.dashboard_locators import DashboardLocators
from utils.app_manager import AppManger


class UserSavePage():
    def __init__(self):
        app = AppManger()
        app_title = app.version_search(DashboardLocators.MAIN_FORM_TITLE)
        self.side_window = Desktop(backend="uia").window(title=app_title)
    

    def get_popup_field(self):
        popup_field = self.side_window.child_window(title="고객등록", auto_id="FrmRegPatInfo", control_type="Window").wrapper_object()
        queue = deque([popup_field])
        edit_arr = []
        checkbox_arr = []
        combobox_arr = []
        button_arr = []


        while queue:
            element = queue.popleft()
            if (element.element_info.control_type == "Edit"):
                edit_arr.append(element)
            elif (element.element_info.control_type == "CheckBox"):
                checkbox_arr.append(element)      
            elif (element.element_info.control_type == "ComboBox"):
                combobox_arr.append(element)
            elif (element.element_info.control_type == "Button"):
                button_arr.append(element)
            queue.extend(element.children())
            
            
        for i,el in enumerate(edit_arr):
            el.set_text(i)
        print(checkbox_arr)
        print(combobox_arr)
    
    