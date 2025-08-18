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
        self.get_rece_buttons()
        self.get_rece_edits()
        self.get_rece_comboboxes()
        
    def get_reception_tab_element_list(self):
        rece_tab = self.user_chart_page.get_chart_field("tab")
        if rece_tab:
            self.rece_element_list_arr = ElementFinder.recursive_children(rece_tab, 0,10)
            
        
    def get_rece_buttons(self):
        btn_arr = []
        
        for pane in self.rece_panel_arr:
            btn_arr.append(ElementFinder.find_buttons(pane.children()))
        self.rece_button_arr = btn_arr

    def get_rece_edits(self):
        """예약탭 Edit 리스트 반환"""
        edit_arr = []
        
        for pane in self.rece_panel_arr:
            edit_arr.append(ElementFinder.find_edits(pane.children()))

        self.rece_edit_arr = edit_arr

    def get_rece_comboboxes(self):
        """예약탭 콤보박스 리스트 반환"""
        combo_arr = []
        for pane in self.rece_panel_arr:
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
        
    def get_element_list(self):
        print(self.rece_element_list_arr)
        print(self.rece_panel_arr)
        print(self.rece_button_arr)
        print(self.rece_edit_arr)