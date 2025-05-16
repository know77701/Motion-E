import time
from multiprocessing import Event, Process

from pywinauto import Application, Desktop

from locators.receive_locators import ReceiveLocators
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


def get_popup_elements():
    return

def get_receive_popup_window(app):
    popup_window_title = app.version_search(ReceiveLocators.RECEIVE_POPUP_TITLE)
    return Desktop(backend="uia").window(title=popup_window_title)

def get_popup_object(app):
    print("get_popup_object")
    receive_window = get_receive_popup_window(app)
    return ElementFinder.find_list_items_by_auto_id(receive_window.children(), auto_id="RadMessageBox")

def confirm_receive_popup(app, confirm_text):
    print("confirm_receive_popup")
    message_box = get_popup_object(app)
    close_btn = ElementFinder.find_button_by_name(message_box.children(), confirm_text)
    if close_btn:
        ElementFinder.click(close_btn)

def close_receive_popup():
    return

# def close_popup(self):
#     receive_process = Desktop(backend="uia").window(auto_id="RadMessageBox").wrapper_object()
#     print(receive_process.children())
    
def close_receive_popup_handler(start_event : Event, timeout=30, interval=1):
    print("[서브 프로세스] 팝업 감지 대기 시작")
    app = Application(backend="win32").connect(title_re="접수")
    main_window = app.window(title_re="접수")
    start_time = time.time()
    while True:
        try:

            for app_items in main_window.children():
                if (app_items.element_info.control_type == "Window" and
                    app_items.element_info.automation_id == "RadMessageBox"):
                    for btn in app_items.children():
                        if (btn.element_info.control_type == "Button" and
                            btn.element_info.name in ["네", "확인"]):
                            print("[팝업 감지됨] 닫기 시도")
                            btn.click()
                            print("[팝업 닫기 완료]")
                            return
        except Exception as e:
            pass  # 프로세스가 꺼졌거나 아직 연결 안 된 경우 무시

        if time.time() - start_time > timeout:
            print("[팝업 없음] 타임아웃")
            break
                
        time.sleep(interval)
    
def close_popup_handler(self,func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        p = Process(target=self.close_popup)
        p.start()
        p.join()
        return result
    return wrapper
        

