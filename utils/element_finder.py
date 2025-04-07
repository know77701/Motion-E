from pywinauto import Desktop

from locators.dashboard_locators import DashboardLocators
from utils.app_manager import AppManger


class ElementFinder:
    """UI 요소를 찾는 유틸 클래스"""
    def __init__(self):
        app = AppManger()
        app_title = app.version_search(DashboardLocators.MAIN_FORM_TITLE)
        self.side_window = Desktop(backend="uia").window(title=app_title)
            
    def get_chrome_field(self):
        """사이드 필드 객체 가져오기"""
        return self.side_window.child_window(class_name="Chrome_RenderWidgetHostHWND").wrapper_object()

    @staticmethod
    def find_text(elements):
        return [item for item in elements if item.element_info.control_type == "Text"]

    @staticmethod
    def find_buttons(elements):
        return [item for item in elements if item.element_info.control_type == "Button"]

    @staticmethod
    def find_button_by_name(elements, name):
        return next((item for item in elements if item.element_info.control_type == "Button" 
                    and item.element_info.name == name),None)
    @staticmethod
    def find_lists(elements):
        return [item for item in elements if item.element_info.control_type == "List"]

    @staticmethod
    def find_edit_by_automation_id(elements, automation_id):
        return next((item for item in elements if item.element_info.control_type == "Edit" 
                    and item.element_info.automation_id == automation_id),None)

    @staticmethod
    def find_documents(elements):
        return [item for item in elements if item.element_info.control_type == "Document"]
    
    @staticmethod
    def find_documents_by_automation_id(elements, automation_id):
        return next((item for item in elements if item.element_info.control_type == "Document" 
                             and item.element_info.automation_id == automation_id), None)
    
    @staticmethod
    def find_edit(elements):
        return [item for item in elements if item.element_info.control_type == "Edit"]
    
    @staticmethod
    def find_pane(elements):
        return [item for item in elements if item.element_info.control_type == "Pane"]
    
    @staticmethod
    def find_group_by_automation_id(elements, automation_id):
        return next((item for item in elements if item.element_info.control_type == "Group"
                 and item.element_info.automation_id == automation_id), None)