from utils.element_finder import ElementFinder


class ReceptionTabPage():
    def __init__(self, user_chart_page):
        self.user_chart_page = user_chart_page
        self.rece_element_list_arr = []
        self.setting()
        
    def setting(self):
        self.get_reception_tab_element_list
        
    def get_reception_tab_element_list(self):
        rcep_tab = self.user_chart_page.get_chart_field("tab")
        if rcep_tab:
            self.rcep_element_list_arr = ElementFinder.recursive_children(rcep_tab, 1,5)