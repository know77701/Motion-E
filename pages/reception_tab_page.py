from utils.element_finder import ElementFinder


class ReceptionTabPage():
    def __init__(self, user_chart_page):
        self.user_chart_page = user_chart_page
        self.rece_element_list_arr = []
        self.rece_panel_arr = []
        self.rece_button_arr = []
        self.rece_edit_arr = []
        
        self.setting()
        
    def setting(self):
        self.get_reception_tab_element_list()
        self.get_rece_panel_items()
        self.get_rsrv_buttons()
        self.get_rsrv_edits()
        self.get_rsrv_comboboxes()
        
    def get_reception_tab_element_list(self):
        rcep_tab = self.user_chart_page.get_chart_field("tab")
        if rcep_tab:
            self.rcep_element_list_arr = ElementFinder.recursive_children(rcep_tab, 1,5)
        
    def get_rsrv_buttons(self):
        """예약탭 버튼 리스트 반환"""
        btn_arr = []
        
        for pane in self.rsrv_panel_arr:
            btn_arr.append(ElementFinder.find_buttons(pane.children()))
        self.rece_button_arr = btn_arr

    def get_rsrv_edits(self):
        """예약탭 Edit 리스트 반환"""
        edit_arr = []
        
        for pane in self.rsrv_panel_arr:
            edit_arr.append(ElementFinder.find_edits(pane.children()))

        self.rece_edit_arr = edit_arr

    def get_rsrv_comboboxes(self):
        """예약탭 콤보박스 리스트 반환"""
        combo_arr = []
        for pane in self.rsrv_panel_arr:
            combo_arr.append(ElementFinder.find_combobox(pane.children()))
        self.rece_comboboxe_arr = combo_arr
    
    def get_rece_panel_items(self):
        """예약탭 Pane 하위 항목 리스트 반환"""
        pane_list = []
        for items in self.rece_element_list_arr:
            pane_items = ElementFinder.find_pane_by_auto_id(items.children(), "radPanel1")
            
            if pane_items:
                pane_list.append(pane_items)

        self.rece_panel_arr = pane_list