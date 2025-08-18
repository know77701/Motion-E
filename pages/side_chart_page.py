from utils.element_finder import ElementFinder


class SideChartPage:
    def __init__(self, app_manager,user_chart_page):
        self.app_manger = app_manager
        self.user_chart_page = user_chart_page
        self.side_chart_field = self.user_chart_page.get_chart_field("side_chart")
    
    def get_side_memo_list(self):
        for item_list in self.side_chart_field:
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
        self.side_chart_field
        for item_list in self.side_chart_field:
            element = ElementFinder.find_link_by_name(item_list.children(), find_field)
            if element:
                return element
        return None

    def get_side_memo_edit(self):
        """사이드메모 저장 edit 가져오기"""
        for item_list in self.side_chart_field:
            element = ElementFinder.find_edit(item_list.children())
            if element:
                return element
        return None

    def get_side_memo_button(self):
        """사이드메모 저장버튼 가져오기"""
        for item_list in self.side_chart_field:
            element = ElementFinder.find_button_by_name(item_list.children(), "저장")
            if element:
                return element
        return None
    
    def compare_side_memo(self, content, time):
        """사이드 메모 비교"""
        memo_list = self.get_side_memo_list()

        for item_list in memo_list:
            for index in range(len(item_list)):
                name = item_list[index].element_info.name
                if name == content:
                    continue
                next_item = item_list[index + 1]
                if next_item.element_info.name in time:
                    return item_list
        return None
    
    def verify_side_chart(self, list_item):
        side_mopr_list = self.get_side_chart_elements_list()
        
        if sorted(list_item, key=lambda x: list(x.keys())[0]) == sorted(side_mopr_list, key=lambda x: list(x.keys())[0]):
            return True
        else:
            print("불일치합니다.")
            print("예상값:", list_item)
            print("실제값:", side_mopr_list)
            assert False, "저장된 시술 불일치합니다."
    
    def get_side_chart_elements_list(self):
        panel_list = self.user_chart_page.get_chart_field("side_chart")
        
        for list_item in panel_list:
            table = ElementFinder.find_tables(list_item.children())
            if table:
                break
        table_items = ElementFinder.recursive_children(table, 0, 2)
        mopr_list = []
        price_seen = set()

        i = 0
        while i < len(table_items):
            item = table_items[i]
            if item.element_info.control_type == "Header":
                name = item.element_info.name.strip()
                data_items = []
                j = i + 1

                while j < len(table_items) and len(data_items) < 2:
                    if table_items[j].element_info.control_type == "DataItem":
                        data_items.append(table_items[j])
                    j += 1
                if len(data_items) >= 2:
                    
                    price = data_items[1].element_info.name.strip()
                    
                    if price == "0":
                        if name not in price_seen:
                            mopr_list.append({name: price})
                            price_seen.add(name)
                    else:
                        mopr_list.append({name: price})
                        price_seen.add(name)
                i = j
            else:
                i += 1

        return mopr_list
        
    def side_chart_change(self):
        for item_list in self.side_chart_field:
            if ElementFinder.find_link_by_name(item_list.children() ,"차트"):
                buttons = ElementFinder.find_buttons(item_list.children())
                chart_button = buttons[1] if len(buttons) > 1 else None
                chart_button.click()
                break
    
    def get_comfirm_popup(self):
        for item_list in self.side_chart_field:
            custom_popup = ElementFinder.find_custom(item_list.children())
            if custom_popup:
                break

        for items in custom_popup.children():
            btn = ElementFinder.find_button_by_name(items.children(), "예")
            if btn:
                break

        if btn:
            btn.click()
            return True
        return False
    
    def get_compare_time(self):
        """
            차트 시간 확인 및 비교
            사이드 차트 시간 = 진료탭 시간
            진료탭에 진입해서 시간을 가져오고 사이드차트 시간을 비교해야함.
        """
        return