class ElementFinder:
    """UI 요소를 찾는 유틸리티 클래스"""

    @staticmethod
    def find_text(elements):
        return [item for item in elements if item.element_info.control_type == "Text"]

    @staticmethod
    def find_buttons(elements):
        return [item for item in elements if item.element_info.control_type == "Button"]

    @staticmethod
    def find_button_by_name(elements, name):
        return next(
            (item for item in elements if item.element_info.control_type == "Button" and item.element_info.name == name),
            None
        )

    @staticmethod
    def find_lists(elements):
        return [item for item in elements if item.element_info.control_type == "List"]

    @staticmethod
    def find_edit_by_automation_id(elements, automation_id):
        return next(
            (item for item in elements if item.element_info.control_type == "Edit" and item.element_info.automation_id == automation_id),
            None
        )

    @staticmethod
    def find_documents(elements):
        return [item for item in elements if item.element_info.control_type == "Document"]
    
    @staticmethod
    def find_edit(elements):
        return [item for item in elements if item.element_info.control_type == "Edit"]
    
    @staticmethod
    def find_pane(elements):
        return [item for item in elements if item.element_info.control_type == "Pane"]