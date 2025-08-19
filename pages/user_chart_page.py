from datetime import datetime

from utils.element_finder import ElementFinder


class UserChartPage:
    def __init__(self, app_manager):
        self.app_manager = app_manager
        self.app_title = self.app_manager.version_search(auto_id="tBeautyChartForm")
        self.parent_field = ElementFinder.get_user_chart_parent_field(self.app_title)

    def get_rsrv_cancel_popup(self):
        return ElementFinder.find_element(self.parent_field.children(), auto_id="PopReservationCancel", title="예약취소 사유")
        

    def get_chart_title_bar(self):
        parent_field = self.parent_field
        if parent_field:
            title_bar = ElementFinder.find_element(parent_field.children(), auto_id="TitleBar")
            
        if title_bar:
            close_btn = ElementFinder.find_button_by_auto_id(title_bar.children(), "Close")
    
        if close_btn:
            return close_btn            
    
    def get_chart_field(self, find_name):
        parent = self.parent_field
        if not parent:
            return None

        parent.set_focus()
        pane_list = ElementFinder.find_pane(parent.children())

        panel_mapping = {
            "user_info": "radPanel23",
            "tab": "radPanel10",
            "side_chart": "radPanel8",
            "header_field": "panel1",
        }

        for pane in pane_list:
            for item in pane.children():
                name = item.element_info.automation_id
                if name != panel_mapping.get(find_name):
                    continue

                if find_name == "tab":
                    return next(iter(item.children())).children()
                elif find_name == "side_chart":
                    return ElementFinder.recursive_children_with_name_and_element(
                        item, "Motion E web", "Document", 0, 10
                    )
                elif find_name == "header_field":
                    for child in item.children():
                        print(child.children())
                    return None
                else:
                    return item

        print("find_name 입력되지 않음")
        return None
        
    def compare_user_info_get_data(self,chart_no):
        """차트 진입 데이터 확인"""
        user_info_field = self.get_chart_field("user_info")
        return_data = ElementFinder.find_text_by_name(user_info_field.children(), chart_no)
        if not return_data:
            return False
        return True
    
    

    

        