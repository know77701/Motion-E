
import time

from pywinauto import Application, Desktop, findwindows
from pywinauto.controls.hwndwrapper import HwndWrapper

from locators.receive_locators import ReceiveLocators
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


def app_connect():
    motion_starter = AppManger()
    return motion_starter.app_connect()

def close_popup_handler(start_event):
    app_connect()
    print("subprocess connect")
    start_event.wait()

    for attempt in range(30):
        item_tle = None
        item_btn = None

        procs = findwindows.find_elements()
        for proc_list in procs:
            if proc_list.automation_id == "":
                if proc_list.control_type == "Telerik.WinControls.RadMessageBoxForm":
                    for item in proc_list.children():
                        if item.automation_id == "radLabel1":
                            item_tle = item.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                        if item.automation_id == "radButton1":
                            item_btn = item
            else:
                if proc_list.control_type == "Telerik.WinControls.RadMessageBoxForm":
                    for item in proc_list.children():
                        if item.automation_id == "radLabel1":
                            item_tle = item.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                        if item.automation_id == "radButton1":
                            item_btn = item
        if item_btn:
            try:
                print(f"[{attempt + 1}회차] 팝업 발견: {item_tle}")
                btn_wrapper = item_btn.wrapper_object()
                btn_wrapper.click_input()
                break
            except Exception as e:
                print(f"[오류] 팝업 클릭 실패: {e}")
        else:
            print(f"[{attempt + 1}회차] 팝업 없음 또는 버튼 없음")

        start_event.clear()
        time.sleep(2)


def rad_button_click(start_sub_process_event, sub_process_done_event):
    item_tle = None
    item_btn = None
    while True:
        procs = findwindows.find_elements()
        for proc_list in procs:
            if proc_list.automation_id == "":
                proc_cancle_window = proc_list.children()
                for i in proc_cancle_window:
                    print(i)
                if proc_list.control_type == "Telerik.WinControls.RadMessageBoxForm":
                    proc = proc_list.children()
                    for item in proc:
                        if item.automation_id == "radLabel1":
                            item_tle = item.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                        if item.automation_id == "radButton1":
                            item_btn = item
            else:
                if proc_list.control_type == "Telerik.WinControls.RadMessageBoxForm":
                    proc = proc_list.children()
                    for item in proc:
                        if item.automation_id == "radLabel1":
                            item_tle = item.name.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                        if item.automation_id == "radButton1":
                            item_btn = item
            return
        if item_tle is None:
            time.sleep(1)
            break

        if "삭제할환자를선택해주세요." in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
        elif "이름을 입력하세요" in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
        elif "삭제되었습니다." in item_tle or "저장되었습니다" in item_tle or "예약이완료되었습니다!" in item_tle or "접수완료되었습니다." in item_tle or "완료되었습니다." in item_tle or "예약되었습니다." in item_tle or "DUR완료" in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
            start_sub_process_event.clear()
        elif "접수하시겠습니까?" in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
            start_sub_process_event.set()
            time.sleep(2)
            sub_process_done_event.wait()
        elif "예약을취소하시겠습니까?" in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
            start_sub_process_event.set()
            time.sleep(2)
            sub_process_done_event.wait()
        elif "삭제에대한모든책임은병원에있습니다.삭제하시겠습니까?" in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
            start_sub_process_event.set()
            time.sleep(2)
            sub_process_done_event.wait()
        elif "해당고객을삭제하시겠습니까?해당고객의처방및모든데이터가삭제됩니다." in item_tle:
            item_btn = HwndWrapper(item_btn)
            item_btn.click()
            start_sub_process_event.set()
            time.sleep(2)
            sub_process_done_event.wait()
        else:
            raise Exception('팝업 확인필요')

        # def chart_sub_process(self, start_sub_process_event, sub_process_done_event):
        # print("테스트")

def notice_popup_close(self,motion_app):
    procs = findwindows.find_elements()
    notice_procs = None
    for pro in procs:
        if pro.name == "안내사항" and pro.automation_id == "PopEventViewer":
            notice_procs = pro
            break

    if notice_procs is not None:
        notice_window = motion_app.window(
            title=self.motion_starter.version_search(self.notice_value))
        notice_list = notice_window.children()
        for item_list in notice_list:
            if item_list.element_info.control_type == "TitleBar":
                for item in item_list.children():
                    if item.element_info.control_type == "Button" and item.element_info.name == "닫기":
                        item.click()
                        break          
                

