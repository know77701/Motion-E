import ctypes
import sys
import time

from pywinauto import Desktop, application

import config
from locators.login_locators import LoginLocators
from utils.app_screen_shot import window_screen_shot


class AppManger:
    def __init__(self):
        self.backend = "uia"
        self.win_32_backend = "win32"
        self.win32_app = application.Application()
        self.motion_app = application.Application(backend=self.backend)
        
   
    def version_search(self, search_title):
        
        """특정 창이 열려있는지 확인"""
        windows = Desktop(backend=self.backend).windows()
        try:
            for window in windows:
                if search_title in window.window_text():
                    return window.window_text()
        except Exception as e:
            print("버전 찾기 실패", e)
            window_screen_shot("version_search_fail")
            
                
    def login_form_connect(self,win32_app):
        app = win32_app.connect(title=config.PROCESS_TITLE)
        app.top_window().set_focus()
        return app
            
    def motion_app_connect(self, motion_app):
        version_text = self.version_search(config.MOTION_VERSION_TITLE)
        app = motion_app.connect(title=version_text)
        app.top_window().set_focus()
        return app
            
    def app_connect(self, retries=0):
        try:
            if self.version_search(config.MOTION_VERSION_TITLE):
                return self.motion_app_connect(self.motion_app)
            elif self.version_search(LoginLocators.LOGIN_FORM_TITLE):
                return self.login_form_connect(self.win32_app)
            else:
                self.win32_app.start(config.APP_PATH)
                time.sleep(3)
                motion_window = self.motion_app_connect(self.motion_app)
                return motion_window
                
        except application.ProcessNotFoundError as e:
            print("앱 찾기 실패 :", e)
            window_screen_shot("app_connect_fail")
            if retries < config.MAX_RETRY:
                retries += 1
                print(f"재시도 횟수: {retries}")
                self.app_connect(retries)
            else:
                print("최대 재시도 횟수에 도달했습니다. 프로그램을 종료합니다.")
        except application.AppStartError:
            print("앱 미설치 또는 앱 미존재")
            window_screen_shot("app_connect_fail")
            
    def check_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()