import threading
import time

from pywinauto import findwindows
from pywinauto.controls.hwndwrapper import HwndWrapper

from utils.element_finder import ElementFinder


class ClosePopupThread(threading.Thread):
    def __init__(self, start_event, quit_event):
        threading.Thread.__init__(self)
        self.start_event = start_event
        self.quit_event = quit_event

    def run(self):
        print("[PopupThread] Started")
        while not self.quit_event.is_set():
            self.start_event.wait()

            for attempt in range(15):
                if self.quit_event.is_set():
                    break

                item_tle = None
                item_btn = None

                try:
                    procs = findwindows.find_elements()
                except Exception as e:
                    print(f"[오류] find_elements 실패: {e}")
                    break

                for proc_list in procs:
                    if proc_list.control_type == "Telerik.WinControls.RadMessageBoxForm":
                        item_tle = ElementFinder.find_text(proc_list.children(),"radLabel1")
                        if item_tle:
                            item_tle = item_tle.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                        item_btn = ElementFinder.find_button_by_auto_id(proc_list.children(), "radButton1")
                        # for item in proc_list.children():
                        #     if item.automation_id == "radLabel1":
                        #         item_tle = item.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                        #     if item.automation_id == "radButton1":
                        #         item_btn = item
                if item_btn:
                    try:
                        if item_tle:
                            print(f"[PopupThread] 팝업 클릭 시도: {item_tle}")
                        btn = HwndWrapper(item_btn)
                        btn.click()
                        break
                    except Exception as e:
                        attempt +1
                        print(f"[오류] 팝업 클릭 실패: {e}")

                time.sleep(2)

            self.start_event.clear()
        print("[PopupThread] 종료됨")

