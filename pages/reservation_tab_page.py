from utils.element_finder import ElementFinder
import random
import re

class ReservationTabPage:
    def __init__(self, app_manager,user_chart_page):
        self.app_manager = app_manager
        self.user_chart_page = user_chart_page
        self.rsrv_panel_arr = []
        self.rsrv_edit_arr = []
        self.rsrv_button_arr = []
        self.rsrv_comboboxe_arr = []
        self.rsrv_element_list_arr = []
        self.select_rsrv_random_time = None
        self.select_rsrv_day = None
        self.setting()
    
    def setting(self):
        self.get_reservation_tab_element_list()
        self.get_rsrv_panel_items()
        self.get_rsrv_buttons()
        self.get_rsrv_edits()
        self.get_rsrv_comboboxes()
    
    def get_reservation_tab_element_list(self):
        """예약 탭 최상위 객체 반환"""
        rsrv_tab = self.user_chart_page.get_chart_field("tab")
        if rsrv_tab:
            self.rsrv_element_list_arr = ElementFinder.recursive_children(rsrv_tab, 1,5)
    
    def get_rsrv_panel_items(self):
        """예약탭 Pane 하위 항목 리스트 반환"""
        pane_list = []
        
        for items in self.rsrv_element_list_arr:
            pane_items = ElementFinder.find_pane_by_auto_id(items.children(), "radPanel1")
            
            if pane_items:
                pane_list.append(pane_items)

        self.rsrv_panel_arr = pane_list
    
    def get_rsrv_buttons(self):
        """예약탭 버튼 리스트 반환"""
        btn_arr = []
        
        for pane in self.rsrv_panel_arr:
            btn_arr.append(ElementFinder.find_buttons(pane.children()))
        self.rsrv_button_arr = btn_arr


    def get_rsrv_edits(self):
        """예약탭 Edit 리스트 반환"""
        edit_arr = []
        
        for pane in self.rsrv_panel_arr:
            edit_arr.append(ElementFinder.find_edits(pane.children()))

        self.rsrv_edit_arr = edit_arr

    def get_rsrv_comboboxes(self):
        """예약탭 콤보박스 리스트 반환"""
        combo_arr = []
        for pane in self.rsrv_panel_arr:
            combo_arr.append(ElementFinder.find_combobox(pane.children()))
        self.rsrv_comboboxe_arr = combo_arr
    
    def get_rsrv_timetable_wrapper(self):
        for panel in self.rsrv_panel_arr:
            return ElementFinder.find_pane_by_auto_id(panel.children(), "panel30")
    
    def get_rsrv_timetable_elements(self):
        timetable_wrapper = self.get_rsrv_timetable_wrapper()
        wrapper_list = ElementFinder.recursive_children_with_control_type(timetable_wrapper, "Pane", 0, 2)
        timetalbe = ElementFinder.find_pane_by_auto_id(wrapper_list, "panel1")
        if timetalbe:
            return timetalbe
        
    def get_rsrv_list_table(self, auto_id):
        """예약탭 테이블 리스트 반환"""
        table_arr = []
        list_items = self.rsrv_element_list_arr
        for items in list_items:
            table_items = ElementFinder.find_tables(items.children())
            if table_items:
                table_arr.extend(table_items)

        return ElementFinder.find_list_items_by_auto_id(table_arr, auto_id)
    
    def get_forward_memo_edit(self):
        return self.rsrv_edit_arr[0][0]
    
    def get_rsrv_memo_edit(self):
        return self.rsrv_edit_arr[0][1]
    
    def get_rsrv_day_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.rsrv_edit_arr[0], "txtRsrvDd")

    def get_rsrv_time_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.rsrv_edit_arr[0], "txtRsrvTm")
    
    def get_rsrv_status_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.rsrv_edit_arr[0], "txtRsrvPrgrStat")
        
    def get_calendar_button(self):
        return self.rsrv_button_arr[0][1]

    def get_today_button(self):
        return ElementFinder.find_button_by_name(self.rsrv_button_arr[0], "오늘")

    def get_remove_content_rsrv_button(self):
        return ElementFinder.find_button_by_name(self.rsrv_button_arr[0], "내용 지우기")

    def get_change_rsrv_button(self):
        return ElementFinder.find_button_by_name(self.rsrv_button_arr[0], "예약 변경")

    def get_new_rsrv_button(self):
        return ElementFinder.find_button_by_name(self.rsrv_button_arr[0], "신규 예약")

    def get_cancle_rsrv_button(self):
        return ElementFinder.find_button_by_name(self.rsrv_button_arr[0], "예약 취소")
    
    def get_rsrv_timetable(self):
        """예약 설정 타임테이블 반환"""
        return self.get_rsrv_list_table("calRsrv")
    
    def get_rsrv_list(self):
        """예약 리스트 반환"""
        return self.get_rsrv_list_table("gvRsrv")
    
    def get_ticket_list(self):
        """예약탭 티켓팅 반환"""
        return self.get_rsrv_list_table("gvMoprTicket")
    
    def rsrv_random_time_select(self):
        timetbale_list = self.get_rsrv_timetable_elements()
        self.select_rsrv_random_time = random.choice(timetbale_list.children())
        if self.select_rsrv_random_time:
            self.select_rsrv_random_time.click_input()
        else:
            raise Exception("타임테이블 클릭 실패 확인 필요")
    
    
    def select_rsrv_time_verify(self):
        edit_time = self.get_rsrv_time_edit()
        edit_day = self.get_rsrv_day_edit()

        if edit_time:
            edit_time_str = re.sub(r"[^\d]", "", edit_time.element_info.name)

        if self.select_rsrv_random_time:
            selected_time_str = re.sub(r"[^\d]", "", self.select_rsrv_random_time.element_info.name)

        if edit_time_str == selected_time_str:
            self.select_rsrv_random_time = selected_time_str
            self.select_rsrv_day = re.sub(r"[^\d]", "", edit_day.element_info.name)
            return True
        else:
            return False
    
    def rsrv_time_setting(self):
        select_result = False
        while not select_result:
            self.rsrv_random_time_select()
            if self.select_rsrv_time_verify():
                
                select_result = True
    
    def get_rsrv_list_time(self):
        rsrv_arr = []
        temp_pair = []
        rsrv_list = self.get_rsrv_list()
        for list_items in rsrv_list.children():
            for el in list_items.children():
                el.set_focus()
                raw = re.sub(r"[^\d]", "", el.element_info.name)
                trimmed = raw[1:] if len(raw) > 1 else ""
                if trimmed:
                    temp_pair.append(trimmed)
                    if len(temp_pair) == 2:
                        rsrv_arr.append(temp_pair)
                        temp_pair = []
        return rsrv_arr
            
    def verify_rsrv_list(self):
        arr = self.get_rsrv_list_time()
        found = any(self.select_rsrv_day in item and self.select_rsrv_random_time in item for item in arr)
        print(found)
        if found:
            return True
        else:
            return False
    
    def write_rsrv_memo(self, content):
        edit = self.get_rsrv_memo_edit()
        edit.set_focus()
        edit.set_text("")
        edit.set_text(content)
    
    def write_forward_memo(self, content):
        edit = self.get_forward_memo_edit()
        edit.set_focus()
        edit.set_text("")
        edit.set_text(content)
    
    