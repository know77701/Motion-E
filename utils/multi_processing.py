
import time

from pywinauto import Application, Desktop

from locators.receive_locators import ReceiveLocators
from utils.app_manager import AppManger


class MultiProcess:

    @staticmethod
    def detect_and_close_popup(stop_event, max_retries=3):
        """ 팝업 창 감지 및 처리 """
        try:
            app = AppManger()
            app_title = app.version_search(ReceiveLocators.RECEIVE_POPUP_TITLE)
            print("테스트")
            side_window = Desktop(backend="uia").window(title=app_title).wrapper_object()
            print("테스트")
        except Exception as e:
            print(f"오류 발생: {e}")
            return

        attempt = 0
        while attempt < max_retries:
            try:
                window_list = side_window.children()
                for list_item in window_list:
                    if list_item.element_info.automation_id == "RadMessageBox":
                        for item in list_item.children():
                            if [item.element_info.control_type == "Button"
                                and item.element_info.name == "네"]:
                                    print(item)
                                    item.click()
                time.sleep(0.5)
                break
            except Exception as e:
                attempt += 1
                print(f"시도 {attempt + 1}: {e}")
                