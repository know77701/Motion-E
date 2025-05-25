import threading
import time
import traceback

from pywinauto import findwindows, Application
from pywinauto.controls.hwndwrapper import HwndWrapper
from utils.element_finder import ElementFinder



class ClosePopupThread(threading.Thread):
    def __init__(self, start_event, quit_event):
        threading.Thread.__init__(self)
        self.start_event = start_event
        self.quit_event = quit_event

    try:
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
                        continue

                    for proc_list in procs:
                        if proc_list.control_type == "Telerik.WinControls.RadMessageBoxForm":
                            popup = Application(backend="uia").window(handle=proc_list.handle)
                            # item_btn = popup.child_window(auto_id="radButton1")
                            # item_tle = popup.child_window(auto_id="radLabel1")
                            item_tle = ElementFinder.find_text(proc_list.children(),"radLabel1")
                            if item_tle:
                                item_tle = item_tle.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                            item_btn = ElementFinder.find_button_by_auto_id(proc_list.children(), "radButton1")
                    if item_btn:
                        try:
                            if item_tle:
                                print(f"[PopupThread] 팝업 클릭 시도: {item_tle}")
                            item_btn = HwndWrapper(item_btn)
                            item_btn.click()
                            break
                        except Exception as e:
                            attempt +1
                            print(f"[오류] 팝업 클릭 실패: {e}")

                    time.sleep(2)

                self.start_event.clear()
            print("[PopupThread] 종료됨")
            
    except Exception as e:
        print(f"[오류] 팝업 감지 중 예외 발생: {e}")
        traceback.print_exc()
    