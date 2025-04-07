import re

from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class DashBoardPage():
    def __init__(self):
        self.finder = ElementFinder()
        
    
    def find_field(self, find_name):
        name_map = {
            "예약": "부도",
            "접수": "상담",
            "수납": "완료",
            "시술": "경과시간"
        }
        parent_field = self.finder.get_chrome_field()
        dashboard_field = ElementFinder.find_documents(parent_field.children())
        keyword = name_map.get(find_name, None)
        for element_list in dashboard_field:
            for element in element_list.children():
                name = element.element_info.name.strip()

                if name == find_name:
                    continue

                if keyword and keyword == name:
                    return element_list

                if not keyword and name == find_name:
                    return element_list
                
        print("입력된 탭을 찾을 수 없습니다.")
    

    def time_string(self, name):
        return re.match(r"^\d{1,2}:\d{2}$", name) is not None

    def get_field_user_list(self, find_name):
        reservation_list_field = self.find_field(find_name)
        customer_blocks = []
        current_block = []
        collecting = False
        end_queue = []
        for el in reservation_list_field.children():
            name = el.element_info.name.strip()
            ctrl_type = el.friendly_class_name()

            if self.time_string(name):
                if current_block:
                    customer_blocks.append(current_block)
                current_block = [el]
                collecting = True
                end_queue = []
                continue

            if collecting:
                current_block.append(el)

                end_queue.append(ctrl_type)
                if len(end_queue) > 3:
                    end_queue.pop(0)

                if end_queue == ['ListBox', 'Table', 'ListBox']:
                    customer_blocks.append(current_block)
                    current_block = []
                    collecting = False
                    end_queue = []

        if current_block:
            customer_blocks.append(current_block)
        return customer_blocks
    
    def get_reservation_list(self):
        retun_data =  self.find_field("예약")
        
    def get_reception_list(self):
        retun_data = self.get_field_user_list("접수")
    
    def get_treatment_list(self):
        retun_data =  self.get_field_user_list("시술")
        
    def get_payment_list(self):
        retun_data =  self.get_field_user_list("수납")
    