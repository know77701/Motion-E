from utils.element_finder import ElementFinder


class ReservationTabPage:
    def __init__(self, app_manager,user_chart_page):
        self.app_manager = app_manager
        self.user_chart_page = user_chart_page
    
    def get_reservation_tab_element_list(self):
        """예약 탭 최상위 객체 반환"""
        rsrv_tab = self.user_chart_page.get_chart_field("tab")
        if rsrv_tab:
            return ElementFinder.recursive_children(rsrv_tab, 1,5)
    
    def get_rsrv_panel_items(self):
        """예약탭 Pane 하위 항목 리스트 반환"""
        list_items = self.get_reservation_tab_element_list()
        pane_list = []
        for items in list_items:
            pane_items = ElementFinder.find_pane_by_auto_id(items.children(), "radPanel1")
            if pane_items:
                pane_list.append(pane_items)
        return pane_list
    
    def get_rsrv_buttons(self):
        """예약탭 버튼 리스트 반환"""
        btn_arr = []
        for pane in self.get_rsrv_panel_items():
            btn_arr.append(ElementFinder.find_buttons(pane.children()))
        return btn_arr

    def get_rsrv_edits(self):
        """예약탭 Edit 리스트 반환"""
        edit_arr = []
        for pane in self.get_rsrv_panel_items():
            edit_arr.append(ElementFinder.find_edits(pane.children()))
        return edit_arr

    def get_rsrv_comboboxes(self):
        """예약탭 콤보박스 리스트 반환"""
        combo_arr = []
        for pane in self.get_rsrv_panel_items():
            combo_arr.append(ElementFinder.find_combobox(pane.children()))
        return combo_arr
    
    def get_rsrv_list_table(self, auto_id):
        """예약탭 테이블 리스트 반환"""
        table_arr = []
        list_items = self.get_reservation_tab_element_list()
        for items in list_items:
            table_items = ElementFinder.find_tables(items.children())
            if table_items:
                table_arr.extend(table_items)

        return ElementFinder.find_list_items_by_auto_id(table_arr, auto_id)
    
    def get_forward_memo_edit(self):
        return self.get_rsrv_edits()[0]
    
    def get_rsrv_memo_edit(self):
        return self.get_rsrv_edits()[1]
    
    def get_rsrv_day_edit(self):
        return self.get_rsrv_edits()[2]

    def get_rsrv_time_edit(self):
        return self.get_rsrv_edits()[3]
    
    def get_rsrv_status_edit(self):
        return self.get_rsrv_edits()[4]

    def get_forward_memo_edit(self):
        return self.get_rsrv_edits()[0]
    
    def get_calendar_button(self):
        return self.get_rsrv_buttons()[0]

    def get_today_button(self):
        return self.get_rsrv_buttons()[1]

    def get_change_rsrv_button(self):
        return self.get_rsrv_buttons()[2]

    def get_new_rsrv_button(self):
        return self.get_rsrv_buttons()[3]
    
    
    def get_rsrv_timetable(self):
        """예약 설정 타임테이블 반환"""
        return self.get_rsrv_list_table("calRsrv")
    
    def get_rsrv_list(self):
        """예약 리스트 반환"""
        return self.get_rsrv_list_table("gvRsrv")
    
    def get_ticket_list(self):
        """예약탭 티켓팅 반환"""
        return self.get_rsrv_list_table("gvMoprTicket")
    
    def get_reservation_elements(self):
        return
    