import ctypes
import sys
import time
from datetime import datetime
import logging

import pyautogui
from pywinauto import Desktop, application, timings
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.controls import uia_controls # Added for ElementFinder

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
        self.current_app = None # Add this line

        self.is_admin = self.check_admin()

    def version_search(self, search_title=None, auto_id=None):
        """특정 윈도우 프로세스 확인용"""
        if auto_id:
            windows = Desktop(backend=self.backend).windows()
            try:
                for window in windows:
                    if hasattr(window, 'automation_id') and window.automation_id() == auto_id: # Added hasattr check
                        return window.window_text()
            except Exception as e:
                logging.error(f"버전 찾기 실패 (automation_id): {e}") # Changed print to logging
                window_screen_shot("version_search_fail_automation_id") # Added screenshot
        else:
            windows = Desktop(backend=self.backend).windows()
            try:
                for window in windows:
                    if search_title in window.window_text():
                        return window.window_text()
            except Exception as e:
                logging.error(f"버전 찾기 실패 (search_title): {e}") # Changed print to logging
                window_screen_shot("version_search_fail_title") # Added screenshot
        return None # Explicitly return None if not found

    def login_form_connect(self, retries = 3, interval = 1):
        for i in range(retries):
            try:
                app = self.win32_app.connect(title=LoginLocators.LOGIN_FORM_TITLE)
                app.top_window().set_focus()
                return app
            except ElementNotFoundError:
                logging.warning(f"로그인 창을 찾을 수 없습니다. 재시도 중... ({i+1}/{retries})") # Changed print to logging
                time.sleep(interval)
        logging.error("로그인 창 연결에 실패했습니다.") # Changed print to logging
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
                    logging.warning(f"모션 앱에 연결할 수 없습니다. 재시도 중... ({i+1}/{retries})") # Changed print to logging
                    time.sleep(interval)
            else:
                logging.warning(f"모션 앱 버전 창을 찾을 수 없습니다. 재시도 중... ({i+1}/{retries})") # Changed print to logging
                time.sleep(interval)
        logging.error("모션 앱 연결에 실패했습니다.") # Changed print to logging
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
                    logging.info("모션 앱이 이미 실행 중입니다. 연결 시도...") # Changed print to logging
                    connected_app = self.motion_app_connect()
                    if connected_app:
                        self.current_app = connected_app
                        return connected_app

                # Case 2: Login form is visible (application might be running, but main window not yet)
                if self.version_search(LoginLocators.LOGIN_FORM_TITLE, auto_id=None):
                    logging.info("로그인 폼이 감지되었습니다. 연결 시도...") # Changed print to logging
                    connected_app = self.login_form_connect()
                    if connected_app:
                        self.current_app = connected_app
                        return connected_app

                # Case 3: Application is not running, start it
                logging.info(f"애플리케이션이 실행 중이지 않습니다. 시작 시도... ({i+1}/{retries})") # Changed print to logging
                self.win32_app.start(UtilLocators.APP_PATH)

                # Wait for the login window to appear explicitly
                try:
                    login_window = self.win32_app.window(title=LoginLocators.LOGIN_FORM_TITLE)
                    timings.wait_until_passes(30, 0.5, lambda: login_window.is_visible())
                    login_window.set_focus()
                    connected_app = self.login_form_connect()
                    if connected_app:
                        self.current_app = connected_app
                        return connected_app # Try to connect after start and wait
                except ElementNotFoundError:
                    logging.warning("로그인 창이 예상 시간 내에 나타나지 않았습니다.") # Changed print to logging
                    time.sleep(interval) # Wait before next retry
                    continue

            except application.ProcessNotFoundError as e:
                logging.warning(f"앱 프로세스 찾기 실패: {e}. 재시도 중... ({i+1}/{retries})") # Changed print to logging
                time.sleep(interval) # Wait before next retry
                continue
            except application.AppStartError:
                logging.error("앱 미설치 또는 앱 미존재.") # Changed print to logging
                return None # Fatal error, cannot start app
            except Exception as e:
                logging.error(f"예기치 않은 오류 발생: {e}. 재시도 중... ({i+1}/{retries})") # Changed print to logging
                time.sleep(interval) # Wait before next retry
                continue

        logging.error("애플리케이션 연결 및 시작에 실패했습니다. 최대 재시도 횟수에 도달했습니다.") # Changed print to logging
        window_screen_shot("app_connect_fail")
        return None

    def motion_app_connect_and_login(self, retries=3, interval=1):
        for i in range(retries):
            connected_app = self.app_connect()
            if connected_app:
                # Assuming successful connection leads to the main app window eventually
                # You might need to add specific login steps here if your app requires it
                # For now, let's assume app_connect handles the initial window.
                return connected_app
            logging.warning(f"App connection failed. Retrying... ({i+1}/{retries})") # Changed print to logging
            time.sleep(interval)
        logging.error("Failed to connect to and log into the application after multiple retries.") # Changed print to logging
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
            logging.warning("숫자가 아닌 문자가 포함되어 있습니다.") # Changed print to logging
            return False

        length = len(mobile_no)
        if length not in [10, 11]:
            if length == 8:
                mobile_no = "010" + mobile_no
                return mobile_no
            else:
                logging.warning("입력한 테스트 번호를 다시 확인해주세요") # Changed print to logging
        return mobile_no

    def chart_number_change_format(self, chart_no):
        try:
            new_chart_no = chart_no.strip().replace(" ", "")
            formatted_chart_no = new_chart_no.zfill(10)
            return formatted_chart_no
        except Exception as e:
            logging.error(e) # Changed print to logging

    def get_now_time(self):
        now = datetime.now()
        am_pm = "오전" if now.hour < 12 else "오후"
        hour = now.hour if 0 < now.hour <= 12 else (now.hour - 12 if now.hour > 12 else 12)
        formatted_time = f"{now.strftime('%Y-%m-%d')} {am_pm} {hour}:{now.strftime('%M:%S')}"
        return formatted_time

    @staticmethod
    def assert_alert(alert_text):
        logging.info(f"Alert: {alert_text}") # Changed print to logging
        # return pyautogui.alert(alert_text)

    def connect_to_tbeauty_chart_form(self, retries=3, interval=1):
        for i in range(retries):
            try:
                # tBeautyChartForm 윈도우가 나타날 때까지 대기
                def find_tbeauty_form_robust():
                    for w in Desktop(backend=self.backend).windows():
                        try:
                            if hasattr(w, 'automation_id') and w.automation_id() == "tBeautyChartForm":
                                return w
                        except Exception as e:
                            logging.debug(f"Error getting automation_id for window '{w.window_text()}': {e}")
                    raise ElementNotFoundError("tBeautyChartForm window not found in desktop windows")

                tbeauty_window = timings.wait_until_passes(20, 0.5, find_tbeauty_form_robust) # Increased timeout to 20 seconds
                tbeauty_window.set_focus()
                return tbeauty_window
            except (ElementNotFoundError, timings.TimeoutError) as e:
                logging.warning(f"'tBeautyChartForm' 창을 찾을 수 없습니다. 재시도 중... ({i+1}/{retries}). Error: {e}") # Changed print to logging
                time.sleep(interval)
            except Exception as e:
                logging.error(f"An unexpected error occurred in connect_to_tbeauty_chart_form: {e}. Retrying... ({i+1}/{retries})") # Changed print to logging
                time.sleep(interval)
        logging.error("Failed to connect to 'tBeautyChartForm' after multiple retries.") # Changed print to logging
        return None
    