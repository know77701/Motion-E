import time

from pywinauto import keyboard
from pywinauto.application import Application


class BasePage:
    def __init__(self, app: Application):
        self.app = app

    def dashboard_reset(self, window):
        compare_window = window.children()

        for window in compare_window:
            if window.element_info.name == "고객등록":
                for item in window.children():
                    if item.element_info.control_type == "TitleBar":
                        for title_bar in item.children():
                            if title_bar.element_info.name == "닫기" and title_bar.element_info.control_type == "Button":
                                title_bar.click()
                            if title_bar.element_info.name == "최대화" and title_bar.element_info.control_type == "Button":
                                title_bar.click()
                break
        if self.motion_starter.version_search('접수'):
            receipt_window = self.app.window(
                title="접수", control_type="Window", auto_id="PopAcpt")
            for item in receipt_window.children():
                if item.element_info.control_type == "TitleBar":
                    for title_bar in item.children():
                        if title_bar.element_info.name == "닫기" and title_bar.element_info.control_type == "Button":
                            title_bar.click()
                            break
        for windows in compare_window:
            for window_list in windows.children():
                if window_list.element_info.automation_id == "menuBar":
                    for item in window_list.children():
                        if item.element_info.control_type == "MenuItem" and item.element_info.name == "Dashboard":
                            item.click_input()
            if windows.element_info.control_type == "TitleBar":
                for item in windows.children():
                    if item.element_info.name == "최대화" and item.element_info.control_type == "Button":
                        item.click()
                        break
        time.sleep(0.5)
        keyboard.send_keys("{F5}")
        time.sleep(0.5)