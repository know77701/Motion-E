from PIL import ImageGrab
from functools import partial
from pywinauto import application, Desktop, keyboard
import time
import ctypes
import sys
import os
import multiprocessing



MAX_RETRY = 3
screenshot_save_dir = "fail" 

# 스크린샷 함수 사용 시 확장자명까지 모두 작성(예시 : fail.jpg)
def window_screen_shot(save_file_name):
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    screenshot_path = os.path.join(screenshot_save_dir, save_file_name)
    save_image = ImageGrab.grab()
    save_image.save(screenshot_path)
    
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        window_screen_shot("login_click_fail.jpg")
        return False


class MotionStarter():
    def version_search(search_title):
        windows = Desktop(backend="uia").windows()

        for window in windows:
            try:
                window_text = window.window_text()
                if search_title in window_text:
                    motion_title = window_text
                    return motion_title
            except Exception as e:
                print('버전 찾기 실패', e)
                window_screen_shot("version_search_fail.jpg")

    @staticmethod
    def login_click(title, id):
        try:
            login_window = win32_app.window(title=title)
            login_window.child_window(auto_id=id).click()
        except Exception as e:
            print("로그인 클릭 실패")
            window_screen_shot("login_click_fail.jpg")

    @staticmethod
    def app_title_connect(title, btnName):
        try:
            win32_app.connect(path="Motion_E.exe")
            MotionStarter.login_click(title, btnName)
            win32_app.kill()
            time.sleep(5)
            motion_app.connect(path="Motion_E.exe")
        except Exception as e:
            print("타이틀 찾기 실패")
            window_screen_shot("app_title_connect_fail.jpg")

    @staticmethod
    def app_connect(retries=0):
        try:
            if MotionStarter.version_search('모션.ver'):
                motion_app.connect(
                    path="Motion_E.exe")
                print('기존 앱 연결')
            elif MotionStarter.version_search('로그인'):
                MotionStarter.app_title_connect('로그인', 'btnLogin')
                print('로그인 성공')
            else:
                win32_app.start("C:\\Motion\\Motion_E\\Motion_E.exe")
                time.sleep(1)
                MotionStarter.login_click('로그인', 'btnLogin')
                time.sleep(1)
                motion_app.connect(
                    path="Motion_E.exe")

        except application.ProcessNotFoundError as e:
            print("앱 찾기 실패 :", e)
            window_screen_shot("app_connect_fail.jpg")
            if retries < MAX_RETRY:
                retries += 1
                print(f"재시도 횟수: {retries}")
                win32_app.start("C:\\Motion\\Motion_E\\Motion_E.exe")
                MotionStarter.app_connect(retries)
            else:
                print("최대 재시도 횟수에 도달했습니다. 프로그램을 종료합니다.")
        except application.AppStartError:
            print("앱 미설치 또는 앱 미존재")
            window_screen_shot("app_connect_fail.jpg")


class DashBoard():
    search_window = None
    register_btn = None
    search_btn = None
    register_btn = None
    registration_window = None
    edit_window = None
    fst_mobile_edit2 = None
    sec_mobile_edit3 = None

    @staticmethod
    def search_user(search_name):
        DashBoard.search_window = motion_window.child_window(
            auto_id="srch-val",  control_type="Edit")
        DashBoard.search_window.set_edit_text("")
        DashBoard.search_window.set_edit_text(search_name)
        DashBoard.search_btn = motion_window.child_window(
            title="검색", control_type="Button")
        DashBoard.search_btn.click()

    def popup_view(search_name):
        DashBoard.search_user(search_name)
        DashBoard.register_btn = motion_window.child_window(
            title="환자 등록 후 예약", control_type="Button", first_only=True)
        DashBoard.register_btn.wait(wait_for='exists enabled', timeout=30)
        DashBoard.register_btn.click()

    def text_edit_popup(serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id):
        DashBoard.popup_view(serach_name)
        registration_window = motion_app.window(
            title=MotionStarter.version_search('고객등록'))
        edit_window = registration_window.child_window(
            control_type="Edit", auto_id="txtPat_Nm")
        edit_window.set_edit_text(serach_name)
        if phone_number:
            DashBoard.fst_mobile_edit2 = registration_window.child_window(
                control_type="Edit", auto_id="txtMobile_No2")
            DashBoard.sec_mobile_edit3 = registration_window.child_window(
                control_type="Edit", auto_id="txtMobile_No3")
            match len(phone_number):
                case 13:
                    DashBoard.fst_mobile_edit2.set_edit_text(phone_number[4:8])
                    DashBoard.sec_mobile_edit3.set_edit_text(
                        phone_number[10:13])
                case 11:
                    DashBoard.fst_mobile_edit2.set_edit_text(phone_number[3:7])
                    DashBoard.sec_mobile_edit3.set_edit_text(
                        phone_number[7:11])
                case 8:
                    DashBoard.fst_mobile_edit2.set_edit_text(phone_number[1:4])
                    DashBoard.sec_mobile_edit3.set_edit_text(phone_number[4:8])
        save_btn = registration_window.child_window(
            control_type="Button", auto_id="btn_auto_id")
        start_sub_process_event.set()
        save_btn.click()
        sub_process_done_event.wait()

    def save_receipt_popup(serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id):
        try:
            DashBoard.text_edit_popup(
                serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id)
            receipt_window = motion_app.window(
                title=MotionStarter.version_search('접수'))
            edit_field = receipt_window.child_window(auto_id="radPanel6")
            receipt_memo = edit_field.child_window(control_type="Edit")
            user_memo = edit_field.child_window(control_type="Edit")
            receipt_memo.set_text("테스트")
            user_memo.set_text("테스트")
            receipt_btn = receipt_window.child_window(
                auto_id="btnAcpt", control_type="Button")
            start_sub_process_event.set()
            receipt_btn.click()
            sub_process_done_event.wait()

            web_window = motion_app.child_winodw(title="Motion E web")
            acpt_list = web_window.child_window(
                control_type="List", auto_id="acpt-list")
            test = acpt_list.children()
            print(test)

        except Exception as e:
            window_screen_shot("save_receipt_popup_fail.jpg")
            if MotionStarter.version_search('고객등록'):
                registration_window = motion_app.window(
                    title=MotionStarter.version_search('고객등록'))
                close_btn = registration_window.child_window(
                    title="닫기", control_type="Button")
                close_btn.click()
                print(e)
            elif MotionStarter.version_search('접수'):
                receipt = motion_app.window(
                    title=MotionStarter.version_search('접수'))
                close_btn = receipt.child_window(
                    title="닫기", control_type="Button")
                close_btn.click()
                print(e)

    def save_reserve_popup(serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id):
        try:
            DashBoard.text_edit_popup(
                serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id)
            time.sleep(1)

        except:
            window_screen_shot("save_reserve_popup_fail.jpg")
            if MotionStarter.version_search('고객등록'):
                receipt_window = motion_app.window(
                    title=MotionStarter.version_search('고객등록'))
                close_btn = receipt_window.child_window(
                    title="닫기", control_type="Button")
                close_btn.click()
            else:
                top_menu = motion_app.child_window(auto_id="pnTop")
                dashboard_menu = top_menu.child_window(title="Dashboard")
                dashboard_menu.click_input()

    def user_save(serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id):
        try:
            DashBoard.text_edit_popup(
                serach_name, phone_number, start_sub_process_event, sub_process_done_event, btn_auto_id)
            time.sleep(1)

        except Exception as e:
            print('저장 실패 : ', e)
            window_screen_shot("user_save_fail.jpg")
            if MotionStarter.version_search('고객등록'):
                registration_window = motion_app.window(
                    title=MotionStarter.version_search('고객등록'))
                close_btn = registration_window.child_window(
                    title="닫기", control_type="Button")
                close_btn.click()
            keyboard.send_keys('{F5}')

    def receipt_check(chart_number):
        acpt_list = motion_window.child_window(
            auto_id="acpt-list", control_type="List")
        list_items = acpt_list.children(control_type="ListItem")
        for i in range(len(list_items)):
            item = list_items[i]
            child_elements = item.children()
            for child in child_elements:
                compare_number = child.element_info.name
                if compare_number == chart_number:
                    print(f"접수확인: {compare_number}")
                    break

    def reserve_check(chart_number):
        rsrv_list = motion_window.child_window(
            auto_id="rsrv-list", control_type="List")
        list_items = rsrv_list.children(control_type="ListItem")
        for i in range(len(list_items)):
            item = list_items[i]
            child_elements = item.children()

            for child in child_elements:
                compare_number = child.element_info.name

                if compare_number == chart_number:
                    print(f"예약 확인: {compare_number}")
                    break
                
    def receipt_cancel(chart_number):
        acpt_list = motion_window.child_window(
            auto_id="acpt-list", control_type="List")
        list_items = acpt_list.children(control_type="ListItem")
        for i in range(len(list_items)):
            item = list_items[i]
            child_elements = item.children()
            for child in child_elements:
                compare_number = child.element_info.name
                print(child.element_info.type)
                if compare_number == chart_number:
                    print(f"접수확인: {compare_number}")
                    if type(child).__name__ == "닫기":
                        child.click()
                        break
class ProcessFunc():
    rad_box = None
    retries = 0

    def main_process_func(start_sub_process_event, sub_process_done_event):
        # DashBoard.user_save("자동화체크1", "01074417631",
        #                     start_sub_process_event, sub_process_done_event, "btnSave")
        # # sub process unset
        # sub_process_done_event.clear()
        # start_sub_process_event.clear()
        # time.sleep(1)

        # DashBoard.save_reserve_popup("자동화체크2", "01074417631",
        #                              start_sub_process_event, sub_process_done_event, "btnSaveRsrv")
        # sub_process_done_event.clear()
        # start_sub_process_event.clear()
        # time.sleep(1)

        # DashBoard.save_receipt_popup("자동화체크3", "01074417631",
        #                              start_sub_process_event, sub_process_done_event, "btnSaveAcpt")
        # sub_process_done_event.clear()
        # start_sub_process_event.clear()
        DashBoard.receipt_cancel("0000002351")

    def sub_process_func(start_sub_process_event, sub_process_done_event, window_auto_id, btn_auto_id):

        while ProcessFunc.retries <= MAX_RETRY:
            try:
                start_sub_process_event.wait()
                registration_window = motion_app.window(
                    title=MotionStarter.version_search('고객등록'))
                ProcessFunc.rad_box = registration_window.child_window(
                    auto_id=window_auto_id, first_only=True)
                ProcessFunc.rad_box.wait(wait_for='exists enabled', timeout=30)
                rad_btn = ProcessFunc.rad_box.child_window(auto_id=btn_auto_id)
                rad_btn.click()
                sub_process_done_event.set()
                start_sub_process_event.clear()
            except Exception as e:
                print("서브 모듈 동작 실패 : ", e)
                retries += 1
                continue


if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()


win32_app = application.Application(backend='win32')
motion_app = application.Application(backend='uia')
MotionStarter.app_connect()
motion_window = motion_app.window(title=MotionStarter.version_search('모션.ver'))

if __name__ == "__main__":

    start_sub_process_event = multiprocessing.Event()
    sub_process_done_event = multiprocessing.Event()

    main_process = multiprocessing.Process(
        target=ProcessFunc.main_process_func, args=(start_sub_process_event, sub_process_done_event))
    sub_process = multiprocessing.Process(
        target=ProcessFunc.sub_process_func, args=(start_sub_process_event, sub_process_done_event, "RadMessageBox", "radButton1"))

    main_process.start()
    sub_process.start()

    main_process.join()
    sub_process.terminate()
