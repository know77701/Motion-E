
from utils.element_finder import ElementFinder

class ConsentTabPage:
    def __init__(self, user_chart_page):
        self.user_chart_page = user_chart_page
        self.consent_tab_field = self.user_chart_page.get_chart_field("tab")
        self.edit_arr = []
        self.btn_arr = []
        self.combo_arr = []
        self.check_box_arr = []
        self.setting()
    
    def setting(self):
        self.get_edit_arr_setting()
        self.get_btn_arr_setting()
    
    def get_tab_list_itmes(self):
        return ElementFinder.recursive_children(
            element=self.consent_tab_field,
            depth=0,
            max_depth=30
            )
        
    def get_edit_arr_setting(self):
        self.edit_arr = ElementFinder.find_edits(self.get_tab_list_itmes())
    
    def get_consent_time_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.edit_arr, "dtCnst")
        
    def get_btn_arr_setting(self):
        self.btn_arr = ElementFinder.find_buttons(self.get_tab_list_itmes())
            
    def get_mopr_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.edit_arr,"txtSrchMopr")
    
    def get_set_mopr_btn(self):
        return ElementFinder.find_button_by_auto_id(self.btn_arr, "btnSetMopr")
    
    def get_save_btn(self):
        return ElementFinder.find_button_by_auto_id(self.btn_arr, "btnSave")
        
    def get_wait_save_btn(self):
        return ElementFinder.find_button_by_auto_id(self.btn_arr, "btnSaveWait")
    
    def get_mopr_list(self):
        return ElementFinder.find_tables()
    
    def write_mopr_edit(self):
        edit = self.get_mopr_edit()
        ElementFinder.input_text(edit, "/세트")
        ElementFinder.send_key("{Enter}")
        
    def mopr_search(self):
        return