import ctypes
import sys
import time
from datetime import datetime

import pyautogui
from pywinauto import Desktop, application, timings
from pywinauto.findwindows import ElementNotFoundError

from locators.chart_locators import ChartLocators
from locators.login_locators import LoginLocators
from locators.receive_locators import ReceiveLocators
from locators.util_locators import UtilLocators
from utils.app_screen_shot import window_screen_shot


class AppManger:
    def __init__(self):
        self.win_32_backend = "win32"
        self.win32_app = application.Application(backend=self.win_32_backend)
        
        self.backend = "uia"
        self.motion_app = application.Application(backend=self.backend)
        
        self.is_admin = self.check_admin()
   
    def version_search(self, search_title=None, auto_id=None):
        """특정 윈도우 프로세스 확인용"""
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
                
    def login_form_connect(self, retries = 3, interval = 1):
        for i in range(retries):
            try:
                app = self.win32_app.connect(title=LoginLocators.LOGIN_FORM_TITLE)
                app.top_window().set_focus()
                return app
            except ElementNotFoundError:
                print(f"로그인 창을 찾을 수 없습니다. 재시도 중... ({i+1}/{retries})")
                time.sleep(interval)
        print("로그인 창 연결에 실패했습니다.")
        return None
            
    def motion_app_connect(self, retries = 3, interval = 1):
        for i in range(retries):
            version_text = self.version_search(UtilLocators.MOTION_VERSION_TITLE, auto_id=None)
            if version_text:
                try:
                    app = self.motion_app.connect(title=version_text)
                    app.top_window().set_focus()
                    return app
                except ElementNotFoundError:
                    print(f"모션 앱에 연결할 수 없습니다. 재시도 중... ({i+1}/{retries})")
                    time.sleep(interval)
            else:
                print(f"모션 앱 버전 창을 찾을 수 없습니다. 재시도 중... ({i+1}/{retries})")
                time.sleep(interval)
        print("모션 앱 연결에 실패했습니다.")
        return None
                
    def receive_connect(self):
        if self.version_search(ReceiveLocators.RECEIVE_POPUP_TITLE, auto_id=None):
            return self.motion_app_connect()
        return None
        
    def chart_connect(self):
        if self.version_search(search_title=None, auto_id=ChartLocators.CHART_AUTO_ID):
            return self.motion_app_connect()
        return None
    
    def app_connect(self, retries=3, interval=1):
        for i in range(retries):
            try:
                # Case 1: Motion application is already running
                if self.version_search(UtilLocators.MOTION_VERSION_TITLE, auto_id=None):
                    print("모션 앱이 이미 실행 중입니다. 연결 시도...")
                    connected_app = self.motion_app_connect()
                    if connected_app: return connected_app

                # Case 2: Login form is visible (application might be running, but main window not yet)
                if self.version_search(LoginLocators.LOGIN_FORM_TITLE, auto_id=None):
                    print("로그인 폼이 감지되었습니다. 연결 시도...")
                    connected_app = self.login_form_connect()
                    if connected_app: return connected_app

                # Case 3: Application is not running, start it
                print(f"애플리케이션이 실행 중이지 않습니다. 시작 시도... ({i+1}/{retries})")
                self.win32_app.start(UtilLocators.APP_PATH)
                
                # Wait for the login window to appear explicitly
                try:
                    login_window = self.win32_app.window(title=LoginLocators.LOGIN_FORM_TITLE)
                    timings.wait_until_passes(30, 0.5, lambda: login_window.is_visible())
                    login_window.set_focus()
                    return self.login_form_connect() # Try to connect after start and wait
                except ElementNotFoundError:
                    print("로그인 창이 예상 시간 내에 나타나지 않았습니다.")
                    time.sleep(interval) # Wait before next retry
                    continue

            except application.ProcessNotFoundError as e:
                print(f"앱 프로세스 찾기 실패: {e}. 재시도 중... ({i+1}/{retries})")
                time.sleep(interval) # Wait before next retry
                continue
            except application.AppStartError:
                print("앱 미설치 또는 앱 미존재.")
                return None # Fatal error, cannot start app
            except Exception as e:
                print(f"예기치 않은 오류 발생: {e}. 재시도 중... ({i+1}/{retries})")
                time.sleep(interval) # Wait before next retry
                continue
        
        print("애플리케이션 연결 및 시작에 실패했습니다. 최대 재시도 횟수에 도달했습니다.")
        window_screen_shot("app_connect_fail")
        return None
        
    def check_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()
        return True
            
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
    