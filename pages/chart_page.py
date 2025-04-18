from datetime import datetime

from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class ChartPage:
    def __init__(self):
        self.app_manager = AppManger()
        self.element_finder = ElementFinder()
        
    
    def get_chart_field(self, find_name):
        parent_field = self.element_finder.get_chart_field()
        pane_list = ElementFinder.find_pane(parent_field.children())
        for pane_items in pane_list:
            for items in pane_items.children():
                name = items.element_info.automation_id
                if find_name == "user_info":
                    if name == "radPanel23":
                        return items
                elif find_name == "reservation":
                    if name == "radPanel10":
                        for elements in items.children():
                            return elements.children()
                elif find_name == "side_chart":
                    if name == "radPanel8":
                        return self.element_finder.recursive_children(items, "Motion E web", "Document", 0, 10)
                elif find_name == "header_field":
                    if name == "panel1":
                        for i in items.children():
                            print(i.children())
                else:
                    print("테스트")
    
    def compare_user_info_get_data(self,chart_no):
        """차트 진입 데이터 확인"""
        user_info_field = self.get_chart_field("user_info")
        return_data = ElementFinder.find_text_by_name(user_info_field.children(), chart_no)
        if not return_data:
            return False
        return True
    
    def get_side_memo_list(self):
        memo_field = self.get_chart_field("side_chart")
        for item_list in memo_field:
            memo_list = self.group_memo_items(item_list.children())
            if memo_list:
                return memo_list
        return None
    
    def group_memo_items(self, elements):
        """작성된 사이드메모 리스트 찾기"""
        grouped = []
        start_index = None
        for i in range(len(elements)):
            if (
                elements[i].element_info.name == "출력" and
                elements[i+1].element_info.control_type == "Edit" and
                elements[i+2].element_info.name == "저장"
            ):
                start_index = i + 3
                break;
            
        if start_index:
            i = start_index
            while i + 4 < len(elements):
                group = [
                    elements[i], elements[i+1], elements[i+2], elements[i+3], elements[i+4]
                ]
                grouped.append(group)
                i += 5
            return grouped
    
    def get_side_field_link(self, find_field):
        """사이드메모 링크 가져오기"""
        memo_field = self.get_chart_field("side_chart")
        for item_list in memo_field:
            element = ElementFinder.find_link_by_name(item_list.children(), find_field)
            if element:
                return element
        return None

    def get_side_memo_edit(self):
        """사이드메모 저장 edit 가져오기"""
        memo_field = self.get_chart_field("side_chart")
        for item_list in memo_field:
            element =  ElementFinder.find_edit(item_list.children())
            if element:
                return element
        return None

    def get_side_memo_button(self):
        """사이드메모 저장버튼 가져오기"""
        memo_field = self.get_chart_field("side_chart")
        for item_list in memo_field:
            element = ElementFinder.find_button_by_name(item_list.children(), "저장")
            if element:
                return element
        return None

    
    def compare_side_memo(self, content, time):
        memo_list = self.get_side_memo_list()

        for item_list in memo_list:
            for i in range(len(item_list)):
                name = item_list[i].element_info.name
                if name == content:
                    continue
                next_item = item_list[i + 1]
                if next_item.element_info.name in time:
                    return item_list
        return None

    def get_side_chart(self):
        panel_list = self.get_chart_field("side_chart")
        for item_list in panel_list:
            if ElementFinder.find_link_by_name(item_list.children() ,"차트"):
                buttons = ElementFinder.find_buttons(item_list.children())
                chart_button = buttons[1] if len(buttons) > 1 else None
                chart_button.click()
                break
        

    def get_comfirm_popup(self):
        panel_list = self.get_chart_field("side_chart")
        for item_list in panel_list:
            custom_popup = ElementFinder.find_custom(item_list.children())
            if custom_popup:
                break
                
        for items in custom_popup.children():
            print(items.children())
            btn = ElementFinder.find_button_by_name(items.children(), "예")
            if btn:
                break

        if btn:
            btn.click
            return True
        return False
    
        
