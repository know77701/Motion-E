from pywinauto import Desktop
from pywinauto.findwindows import ElementAmbiguousError, find_element

from locators.chart_locators import ChartLocators
from locators.dashboard_locators import DashboardLocators
from utils.app_manager import AppManger


class ElementFinder:
    """UI 요소를 찾는 유틸 클래스"""
    def __init__(self):
        self.app = AppManger()
    
    def recursive_children_with_name_and_element(self,element, find_name, find_element,depth, max_depth):
        """지정한 깊이까지 모든 하위 자식 노드 재귀 순회"""
        result = []
        if depth > max_depth:
            return result

        for child in element.children():
            name = child.element_info.name
            ctrl_type = child.element_info.control_type
            
            if name in find_name and ctrl_type == find_element:
                result.append(child)
                
            result.extend(self.recursive_children_with_name_and_element(child, find_name, find_element ,depth + 1, max_depth))
            
        return result
    
    def recursive_children_with_control_type(self,element, find_element,depth, max_depth):
        """지정한 깊이까지 모든 하위 자식 노드 재귀 순회"""
        result = []
        if depth > max_depth:
            return result

        for child in  element.children():
            ctrl_type = child.element_info.control_type
            if ctrl_type == find_element:
                result.append(child)
                
            result.extend(self.recursive_children_with_control_type(child, find_element ,depth + 1, max_depth))
            
        return result
    
    def recursive_children(self, element, depth, max_depth):
        result = []
        if depth > max_depth:
            return result
        
        if isinstance(element, list):
            for el in element:
                result.extend(self.recursive_children(el, depth, max_depth))
            return result
        else:
            for child in element.children():
                result.append(child)
                result.extend(self.recursive_children(child, depth + 1, max_depth))
        return result
            
    @staticmethod        
    def get_chrome_field(app_title):
        """크롬 필드 객체 가져오기"""
        side_window = Desktop(backend="uia").window(title=app_title)
        return side_window.child_window(class_name="Chrome_RenderWidgetHostHWND").wrapper_object()

    @staticmethod
    def get_chart_field(app_title, assert_alert_fn):
        """차트 상위 필드 객체 가져오기"""
        try:
            side_window = Desktop(backend="uia").window(title=app_title)
            pane_list = ElementFinder.find_pane(side_window.children())
            return ElementFinder.find_pane_by_auto_id(pane_list[0].children(), "pnlRightAll")
        except ElementAmbiguousError:
            assert_alert_fn("차트가 열려있지 않습니다.")
            return None

    @staticmethod
    def find_text(elements):
        return [item for item in elements if item.element_info.control_type == "Text"]

    @staticmethod
    def find_buttons(elements):
        return [item for item in elements if item.element_info.control_type == "Button"]

    @staticmethod
    def find_button(elements):
        return (item for item in elements if item.element_info.control_type == "Button")
 
    @staticmethod
    def list_in_find_button(elements):
        return (element for item in elements for element in item.children()
                if element.element_info.control_type == "Button")

    @staticmethod
    def find_button_by_name(elements, name):
        return next((item for item in elements if item.element_info.control_type == "Button" 
                    and item.element_info.name == name),None)
    @staticmethod
    def find_button_by_auto_id(elements, auto_id):
        return next((item for item in elements if item.element_info.control_type == "Button" 
                    and item.element_info.automation_id == auto_id),None)
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
        return next((item for item in elements if item.element_info.control_type == "Edit"), None)
    
    @staticmethod
    def find_edits(elements):
        return [item for item in elements if item.element_info.control_type == "Edit"]
    
    @staticmethod
    def find_edit_by_name(elements, name):
        return next(item for item in elements if item.element_info.control_type == "Edit" 
                    and name in item.element_info.name)
    
    @staticmethod
    def find_pane(elements):
        return [item for item in elements if item.element_info.control_type == "Pane"]
    
    @staticmethod
    def find_group_by_automation_id(elements, id):
        return next((item for item in elements if item.element_info.control_type == "Group"
                 and item.element_info.automation_id == id), None)
    @staticmethod
    def find_group(elements):
        return next((item for item in elements if item.element_info.control_type == "Group"), None)
    
    @staticmethod
    def find_group_list(elements):
        return [item for item in elements if item.element_info.control_type == "Group"]
        
    @staticmethod
    def find_custom(elements):
        return next((item for item in elements if item.element_info.control_type == "Custom"), None)
    
    @staticmethod
    def find_text_by_name(elements,name):
        return next((item for item in elements if item.element_info.control_type == "Text"
                     and item.element_info.name == name), None)
    @staticmethod
    def find_text_with_name_in(elements,name):
        return next((item for item in elements if item.element_info.control_type == "Text"
                     and name in item.element_info.name), None)
    @staticmethod
    def find_pane_by_auto_id(elements,id):
        return next((item for item in elements if item.element_info.control_type == "Pane"
                     and item.element_info.automation_id == id), None)
    @staticmethod
    def find_link_by_name(elements,name):
        return next((item for item in elements if item.element_info.control_type == "Hyperlink"
                     and name in item.element_info.name), None)
    @staticmethod
    def find_links(elements):
        return [(item for item in elements if item.element_info.control_type == "Hyperlink"), None]
    
    @staticmethod
    def find_tables(elements):
        return [item for item in elements if item.element_info.control_type == "Table"]
    
    @staticmethod
    def find_combobox(elements):
        return [item for item in elements if item.element_info.control_type == "ComboBox"]
    
    @staticmethod
    def find_list_items_by_auto_id(elements, auto_id):
        return next((item for item in elements if item.element_info.automation_id == auto_id), None)
    
    
    @staticmethod
    def find_element(element_window, auto_id=None, class_name=None, control_type=None, title=None):
        return element_window.child_window(auto_id=auto_id, class_name=class_name, control_type=control_type, title=title)
    
    @staticmethod
    def click(element):
        """클릭 액션"""
        if element:
            element.click()
        else:
            raise Exception(f"요소를 찾을 수 없음: {element}")

    @staticmethod
    def input_text(element, text):
        """텍스트 입력"""
        if element:
            element.set_focus()
            element.set_text(text)
        else:
            raise Exception(f"입력할 수 없음: {element}")
        