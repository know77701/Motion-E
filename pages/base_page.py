import time

from pywinauto import keyboard
from pywinauto.application import Application

from locators.dashboard_locators import DashboardLocators
from utils.element_finder import ElementFinder


class BasePage:
    def __init__(self, app: Application, app_manager):
        self.app = app
        self.app_manager = app_manager

    def find_element_by_automation_id(self, automation_id: str):
        return ElementFinder.find_element(self.app.top_window(), auto_id=automation_id)

    def dashboard_reset(self, window):
        compare_window = window.children()

        for w in compare_window:
            if w.element_info.name == DashboardLocators.CUSTOMER_REGISTRATION_WINDOW_NAME:
                for item in w.children():
                    if item.element_info.control_type == "TitleBar":
                        for title_bar in item.children():
                            if title_bar.element_info.name == DashboardLocators.CLOSE_BUTTON_NAME and title_bar.element_info.control_type == "Button":
                                ElementFinder.click(title_bar)
                                ElementFinder.wait_for_element_not_visible(w) # Wait for the window to close
                            if title_bar.element_info.name == DashboardLocators.MAXIMIZE_BUTTON_NAME and title_bar.element_info.control_type == "Button":
                                ElementFinder.click(title_bar)
                break
        if self.app_manager.version_search(DashboardLocators.RECEIPT_WINDOW_TITLE):
            receipt_window = self.app.window(
                title=DashboardLocators.RECEIPT_WINDOW_TITLE, control_type="Window", auto_id="PopAcpt")
            if ElementFinder.wait_for_element_visible(receipt_window):
                for item in receipt_window.children():
                    if item.element_info.control_type == "TitleBar":
                        for title_bar in item.children():
                            if title_bar.element_info.name == DashboardLocators.CLOSE_BUTTON_NAME and title_bar.element_info.control_type == "Button":
                                ElementFinder.click(title_bar)
                                ElementFinder.wait_for_element_not_visible(receipt_window) # Wait for the receipt window to close
                                break
        for windows in compare_window:
            for window_list in windows.children():
                if window_list.element_info.automation_id == "menuBar":
                    for item in window_list.children():
                        if item.element_info.control_type == "MenuItem" and item.element_info.name == DashboardLocators.DASHBOARD_MENU_ITEM_NAME:
                            ElementFinder.click(item)
            if windows.element_info.control_type == "TitleBar":
                for item in windows.children():
                    if item.element_info.name == DashboardLocators.MAXIMIZE_BUTTON_NAME and item.element_info.control_type == "Button":
                        ElementFinder.click(item)
                        break
        ElementFinder.send_key("{F5}")
        # Consider adding a wait for an element on the dashboard to be visible/enabled after refresh
        # For example: ElementFinder.wait_for_element_visible(self.app.window(title=DashboardLocators.MAIN_FORM_TITLE))