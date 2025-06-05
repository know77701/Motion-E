import re
import time
from concurrent.futures import ThreadPoolExecutor

from pywinauto import Desktop, keyboard

from utils.element_finder import ElementFinder


class ConsultTabPage:
    def __init__(self, user_chart_page):
        self.user_chart_page = user_chart_page
        self.consent_tab_field = self.user_chart_page.get_chart_field("tab")
        self.edit_arr = []
        self.btn_arr = []
        self.combo_arr = []
        self.check_box_arr = []
        self.table_list_arr = []
        self.__setting()
    
    def __setting(self):
        with ThreadPoolExecutor() as executor:
            future_edit_arr = executor.submit(self.__get_edit_arr_setting)
            future_btn_arr = executor.submit(self.__get_btn_arr_setting)
            future_edit_arr.result()
            future_btn_arr.result()
            
    
    def get_tab_list_itmes(self):
        return ElementFinder.recursive_children(
            element=self.consent_tab_field,
            depth=0,
            max_depth=30
            )
    
    def __get_table_arr_setting(self):
        self.table_list_arr = ElementFinder.find_tables(self.get_tab_list_itmes())
    
    def __get_edit_arr_setting(self):
        self.edit_arr = ElementFinder.find_edits(self.get_tab_list_itmes())
    
    def __get_btn_arr_setting(self):
        self.btn_arr = ElementFinder.find_buttons(self.get_tab_list_itmes())
    
    def __get_consent_time_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.edit_arr, "dtCnst")
            
    def __get_mopr_edit(self):
        return ElementFinder.find_edit_by_automation_id(self.edit_arr,"txtSrchMopr")
    
    def __get_set_mopr_btn(self):
        return ElementFinder.find_button_by_auto_id(self.btn_arr, "btnSetMopr")
    
    def __get_save_btn(self):
        return ElementFinder.find_button_by_auto_id(self.btn_arr, "btnSave")
        
    def __get_wait_save_btn(self):
        return ElementFinder.find_button_by_auto_id(self.btn_arr, "btnSaveWait")
    
    def __get_mopr_list_table(self):
        self.__get_table_arr_setting()
        return ElementFinder.find_table_by_auto_id(self.table_list_arr, "gvRegMopr")
    
    def __write_mopr_edit(self):
        edit = self.__get_mopr_edit()
        ElementFinder.input_text(edit, "/세트")
        edit.set_focus()
        keyboard.send_keys("{ENTER}")
        search_mopr_list = next(self.__get_mopr_list_table(),None)

        if search_mopr_list != None:
            edit.set_focus()
            keyboard.send_keys("{ENTER}")
    
    def __mopr_select_list_get(self):
        self.__get_table_arr_setting()
        for table_list in self.table_list_arr:
            if (table_list.element_info.automation_id != "gvMoprTicket" and 
                table_list.element_info.automation_id != "gvMoprPlan"):
                return table_list
    
    def __mopr_list_element(self):
        mopr_list = self.__mopr_select_list_get()
        if not mopr_list:
            return []

        list_items = ElementFinder.recursive_children(mopr_list.children(), depth=0, max_depth=1)
        result_arr = []
        current_name = None

        for el in list_items:
            el.set_focus()
            raw_text = el.element_info.name.strip()
            clean_row_text = re.sub(r"Row \d+ Column", "", raw_text).strip()
            clean_value_text = re.sub(r"Value", "", clean_row_text).strip()

            if "시술명" in raw_text:
                current_name = clean_value_text.replace("시술명", "").strip()

            elif "결제금액" in raw_text and current_name:
                price = clean_value_text.replace("결제금액", "").strip()
                
                price_digits = re.sub(r"[^\d]", "", price)
                
                # 숫자일경우 포멧 변경
                if price_digits.isdigit():
                    price_only = "{:,}".format(int(price_digits))
                else:
                    price_only = price

                result_arr.append({current_name: price_only})
                current_name = None
        print(result_arr)
        return result_arr
                
    def mopr_search(self):
        self.__write_mopr_edit()
        time.sleep(2)
        return self.__mopr_list_element()
        
    
    def mopr_save(self):
        save_btn = self.__get_save_btn()
        ElementFinder.click(save_btn)