import time
from multiprocessing import Process

from pywinauto import Desktop

from locators.receive_locators import ReceiveLocators
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class popupHandler:
    def __init__(self, app_manger : AppManger):
        self.app_manger = app_manger
        

    def get_popup_elements(self):
        return
    
    def get_receive_popup_window(self):
        popup_window_title = self.app_manger.version_search(ReceiveLocators.RECEIVE_POPUP_TITLE, auto_id=None)
        return Desktop(backend="uia").window(title=popup_window_title)

    def get_popup_object(self):
        receive_window = self.get_receive_popup_window()        
        return ElementFinder.find_list_items_by_auto_id(receive_window.children(), auto_id="RadMessageBox")

    def confirm_receive_popup(self, confirm_text):
        message_box = self.get_popup_object()
        close_btn = ElementFinder.find_button_by_name(message_box.children(), confirm_text)
        if close_btn:
            ElementFinder.click(close_btn)

    def close_receive_popup(self):
        return

    # def close_popup(self):
    #     receive_process = Desktop(backend="uia").window(auto_id="RadMessageBox").wrapper_object()
    #     print(receive_process.children())
        
    def close_receive_popup_handler(self, timeout=30, interval=1):
        """지정된 시간 동안 반복적으로 팝업 감지 후 닫기"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                popup_object = self.get_popup_object()
                if popup_object.exists(timeout=1):
                    print("[팝업 감지됨] 닫기 시도")
                    self.confirm_receive_popup("네")
                    self.confirm_receive_popup("확인")
                    print("[팝업 닫기 완료]")
                    return
            except Exception as e:
                pass 
            time.sleep(interval)
        print("[팝업 없음] 타임아웃")

    # def close_receive_popup_handler(self,func):
    #     def wrapper(*args, **kwargs):
    #         result = func(*args, **kwargs)
    #         p = Process(target=self.confirm_receive_popup)
    #         p.start()
    #         p.join()
            
    #         return result
    #     return wrapper
    
    def close_popup_handler(self,func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            p = Process(target=self.close_popup)
            p.start()
            p.join()
            
            return result
        return wrapper