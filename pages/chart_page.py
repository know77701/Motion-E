from datetime import datetime

from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class ChartPage:
    def __init__(self):
        self.app_manager = AppManger()
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
            element = self.element_finder.find_link_by_name(item_list.children(), find_field)
            if element:
                return element
        return None

    def get_side_memo_edit(self):
        """사이드메모 저장 edit 가져오기"""
        memo_field = self.get_chart_field("side_chart")
        for item_list in memo_field:
            element =  self.element_finder.find_edit(item_list.children())
            if element:
                return element
        return None

    def get_side_memo_button(self):
        """사이드메모 저장버튼 가져오기"""
        memo_field = self.get_chart_field("side_chart")
        for item_list in memo_field:
            element = self.element_finder.find_button_by_name(item_list.children(), "저장")
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
            if self.element_finder.find_link_by_name(item_list.children() ,"차트"):
                buttons = self.element_finder.find_buttons(item_list.children())
                chart_button = buttons[1] if len(buttons) > 1 else None
                chart_button.click()
                break
    
    def get_comfirm_popup(self):
        panel_list = self.get_chart_field("side_chart")
        for item_list in panel_list:
            custom_popup = self.element_finder.find_custom(item_list.children())
            if custom_popup:
                break

        for items in custom_popup.children():
            print(items.children())
            btn = self.element_finder.find_button_by_name(items.children(), "예")
            if btn:
                break

        if btn:
            btn.click
            return True
        return False
    
    def get_compare_time(self):
        """
            차트 시간 확인 및 비교
            사이드 차트 시간 = 진료탭 시간
            진료탭에 진입해서 시간을 가져오고 사이드차트 시간을 비교해야함.
        """
        return
    
    def get_reservation_tab_element_list(self):
        rsrv_tab = self.get_chart_field("tab")
        if rsrv_tab is not None:
            return self.element_finder.recursive_children(rsrv_tab, 1,5)
            
    
    def get_rsrv_elements(self):
        list_items = self.get_reservation_tab_element_list()
        pane_list = []
        
        for items in list_items:
            pane_items = self.element_finder.find_pane_by_auto_id(items.children(), "radPanel1")
            if pane_items:
                pane_list.append(pane_items)
                
        return pane_list
    
    def get_rsrv_list_table(self):
        list_items = self.get_reservation_tab_element_list()
        table_list = []
        
        for items in list_items:
            table_items = self.element_finder.find_tables(items.children())
            if table_items:
                table_list.append(table_items)
        
        return table_list
    
    def get_reservation_elements(self, elements):
        for i in elements:
            print(i)