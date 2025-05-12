import ctypes
import sys
import time
from datetime import datetime

import pyautogui
from pywinauto import Desktop, application

from locators.chart_locators import ChartLocators
from locators.login_locators import LoginLocators
from locators.receive_locators import ReceiveLocators
from locators.util_locators import UtilLocators
from utils.app_screen_shot import window_screen_shot


class AppManger:
    def __init__(self):
        self.backend = "uia"
        self.win_32_backend = "win32"
        self.win32_app = application.Application()
        self.motion_app = application.Application(backend=self.backend)
        
   
    def version_search(self, search_title=None, auto_id=None):
        """특정 창이 열려있는지 확인"""
        if auto_id:
            windows = Desktop(backend=self.backend).windows()
            try:
                for window in windows:
                    if window.automation_id() == auto_id:
                        return window.window_text()
            except Exception as e:
                print("버전 찾기 실패", e)
            
        else:
            windows = Desktop(backend=self.backend).windows()
            try:
                for window in windows:
                    if search_title in window.window_text():
                        return window.window_text()
            except Exception as e:
                print("버전 찾기 실패", e)
                window_screen_shot("version_search_fail")
                
    def login_form_connect(self, retries = 0):
        if retries <= 3:
            app = self.win32_app.connect(title=LoginLocators.LOGIN_FORM_TITLE)
            
            if app:    
                app.top_window().set_focus()
                return app
            else:
                return self.login_form_connect(retries + 1)
            
    def motion_app_connect(self, retries = 0):
        if retries <= 3:
            version_text = self.version_search(UtilLocators.MOTION_VERSION_TITLE, auto_id=None)
            if version_text:
                app = self.motion_app.connect(title=version_text)
                app.top_window().set_focus()
                return app
            else:
                return self.motion_app_connect(retries + 1)
                
    def receive_connect(self):
        if self.version_search(ReceiveLocators.RECEIVE_POPUP_TITLE, auto_id=None):
            return self.motion_app_connect(self.motion_app)
        
    def chart_connect(self):
        if self.version_search(search_title=None, auto_id=ChartLocators.CHART_AUTO_ID):
            return self.motion_app_connect(self.motion_app)
    
    def app_connect(self, retries=0):
        try:
            if self.version_search(UtilLocators.MOTION_VERSION_TITLE, auto_id=None):
                return self.motion_app_connect()
            elif self.version_search(LoginLocators.LOGIN_FORM_TITLE, auto_id=None):
                return self.login_form_connect()
            else:
                self.win32_app.start(UtilLocators.APP_PATH)
                time.sleep(3)
                return self.login_form_connect()
                
        except application.ProcessNotFoundError as e:
            print("앱 찾기 실패 :", e)
            if retries < 3:
                retries += 1
                print(f"재시도 횟수: {retries}")
                self.app_connect(retries)
            else:
                window_screen_shot("app_connect_fail")
                print("최대 재시도 횟수에 도달했습니다. 프로그램을 종료합니다.")
        except application.AppStartError:
            print("앱 미설치 또는 앱 미존재")
        
    def check_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()
            
    def mobile_number_change_fromat(self, mobile_no):
        """모바일 번호 형식 맞추기"""
        mobile_no = mobile_no.strip().replace("-", "")
        
        if not mobile_no.isdigit():
            print("숫자가 아닌 문자가 포함되어 있습니다.")
            return False

        length = len(mobile_no)
        if length not in [10, 11]:
            if length == 8:
                mobile_no = "010" + mobile_no
                return mobile_no
            else:
                print("입력한 테스트 번호를 다시 확인해주세요")
        return mobile_no
    
    def chart_number_change_format(self, chart_no):
        try:
            new_chart_no = chart_no.strip().replace(" ", "")
            formatted_chart_no = new_chart_no.zfill(10)
            return formatted_chart_no
        except Exception as e:
            print(e)
                
    def get_now_time(self):
        now = datetime.now()
        am_pm = "오전" if now.hour < 12 else "오후"
        hour = now.hour if 0 < now.hour <= 12 else (now.hour - 12 if now.hour > 12 else 12)
        formatted_time = f"{now.strftime('%Y-%m-%d')} {am_pm} {hour}:{now.strftime('%M:%S')}"
        return formatted_time
    
    def assert_alert(self, alert_text):
        return pyautogui.alert(alert_text)
    