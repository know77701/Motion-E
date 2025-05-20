import threading

from utils.app_manager import AppManger
from utils.multi_thread import ClosePopupThread


class TestBase():
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        self.start_event = threading.Event()
        self.quit_event = threading.Event()
        self.popup_thread = ClosePopupThread(self.start_event, self.quit_event)
        self.popup_thread.daemon = True
        self.popup_thread.start()
        
        self.window = self.app_manager.motion_app_connect(retries=0)
        
    def shutdown(self):
        self.quit_event.set()
        self.start_event.set()
        self.popup_thread.join()