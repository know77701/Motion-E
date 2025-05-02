from datetime import datetime

from utils.element_finder import ElementFinder


class ChartPage:
    def __init__(self):
        self.element_finder = ElementFinder()
    
    def get_chart_field(self, find_name):
        parent_field = self.element_finder.get_chart_field()
        if parent_field:
            pane_list = self.element_finder.find_pane(parent_field.children())
            for pane_items in pane_list:
                for items in pane_items.children():
                    name = items.element_info.automation_id
                    if find_name == "user_info":
                        if name == "radPanel23":
                            return items
                    elif find_name == "tab":
                        if name == "radPanel10":
                            for elements in items.children():
                                return elements.children()
                    elif find_name == "side_chart":
                        if name == "radPanel8":
                            return self.element_finder.recursive_children_with_name_and_element(items, "Motion E web", "Document", 0, 10)
                    elif find_name == "header_field":
                        if name == "panel1":
                            for i in items.children():
                                print(i.children())
                    else:
                        print("테스트")
        else:
            return None
        
        
    def compare_user_info_get_data(self,chart_no):
        """차트 진입 데이터 확인"""
        user_info_field = self.get_chart_field("user_info")
        return_data = self.element_finder.find_text_by_name(user_info_field.children(), chart_no)
        if not return_data:
            return False
        return True
    

    

        