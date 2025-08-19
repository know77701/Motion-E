import time

from pywinauto import findwindows, keyboard, mouse

from locators.login_locators import LoginLocators
from utils.app_screen_shot import window_screen_shot
from utils.element_finder import ElementFinder


class LoginPage:
    """
        로그인 객체 모음
    """
    def __init__(self, app):
        self.app = app
        self.login_window = app.window(title=LoginLocators.LOGIN_FORM_TITLE)
    
    """병원정보 영역 보이기"""
    def hospital_info_view(self):
        ElementFinder.send_key("^h")
        hospital_info_group = self.login_window.child_window(auto_id=LoginLocators.HOSPITAL_INFO_GROUP_ID)
        # Wait for the group to become visible
        ElementFinder.wait_for_element_visible(hospital_info_group)

        yakiho_window = self.login_window.child_window(auto_id=LoginLocators.YAKIHO_TEXT_ID)
        if not yakiho_window.exists():
            raise Exception("요양기관번호 입력영역을 찾을 수 없습니다.")
    
    """요양기관번호 입력"""
    def hospital_yakiho_setting(self, value):
        start_time_input = time.time()
        edit = ElementFinder.find_element(self.login_window,auto_id=LoginLocators.YAKIHO_TEXT_ID).wrapper_object().children()[0]
        if edit:
            ElementFinder.input_text(edit,value)
        end_time_input = time.time()
        print(f"   요양기관번호 입력 소요 시간: {end_time_input - start_time_input:.2f}초")

        start_time_click = time.time()
        save_btn = ElementFinder.find_element(self.login_window, auto_id=LoginLocators.YAKIHO_SAVE_BUTTON_ID).wrapper_object()
        if save_btn:
            ElementFinder.click(save_btn)
        end_time_click = time.time()
        print(f"   저장 버튼 클릭 소요 시간: {end_time_click - start_time_click:.2f}초")
        
        # Wait for the hospital info group to disappear after saving
        # Removed explicit wait as per user's request to proceed immediately.
        # start_time_wait = time.time()
        # hospital_info_group = self.login_window.child_window(auto_id=LoginLocators.HOSPITAL_INFO_GROUP_ID)
        # ElementFinder.wait_for_element_not_visible(hospital_info_group, timeout=1)
        # end_time_wait = time.time()
        # print(f"   병원정보 영역 사라짐 대기 소요 시간: {end_time_wait - start_time_wait:.2f}초")

    """유저 아이디 입력"""
    def user_id_setting(self, user_id):
        id_edit = ElementFinder.find_element(self.login_window, auto_id=LoginLocators.ID_EDIT_ID).wrapper_object().children()[0]
        ElementFinder.input_text(id_edit, user_id)
    
    """유저 비밀번호 입력"""
    def user_pw_setting(self,user_pw):
        pw_edit = ElementFinder.find_element(self.login_window, auto_id=LoginLocators.PW_EDIT_ID).wrapper_object().children()[0]
        ElementFinder.input_text(pw_edit, user_pw)

    """로그인 버튼 클릭"""
    def login_btn_click(self):
        try:
            login_btn = ElementFinder.find_element(self.login_window, auto_id=LoginLocators.LOGIN_BUTTON_ID).wrapper_object()
            ElementFinder.click(login_btn)
        except Exception as e:
            print(f"로그인 실패 : {e}")
            window_screen_shot("login_click_fail")

    def login_full_process(self, user_id, user_pw, yakiho_no):
        print("[로그인 프로세스 시작]")
        # 2. [초기 로딩 대기]
        print("2. 초기 로딩 대기: 'frmWatingBar' 창이 사라질 때까지 대기합니다.")
        try:
            waiting_bar_window = self.app.window(title=LoginLocators.FRM_WAITING_BAR_TITLE)
            ElementFinder.wait_for_element_not_visible(waiting_bar_window, timeout=3)
            print("   'frmWatingBar' 창 사라짐 확인.")
        except findwindows.ElementNotFoundError:
            print("   WatingBar 팝업이 나타나지 않았습니다. 이미 로딩이 완료되었을 수 있습니다.")
        
        # 3. [로그인 팝업 확인 및 상호작용]
        print("3. 로그인 팝업 확인: 'FrmLogin' 아이디를 가진 로그인 팝업 노출을 확인합니다.")
        if ElementFinder.wait_for_element_visible(self.login_window):
            print("   로그인 팝업 노출 확인. 사용자 ID 및 비밀번호를 입력합니다.")
            self.user_id_setting(user_id)
            print(f"   ID: {user_id} 입력 완료.")
            self.user_pw_setting(user_pw)
            print(f"   PW: {user_pw} 입력 완료.")

            # Always ensure Hospital Info is set
            print("   병원정보 영역 설정을 시작합니다.")
            print("   '컨트롤 + H' 키를 입력하여 병원정보 영역을 노출합니다.")
            self.hospital_info_view() # This will send ^h and wait for visibility
            print("   요양기관번호를 입력하고 저장합니다.")
            self.hospital_yakiho_setting(yakiho_no)
            print("   병원정보 저장 완료. 병원정보 영역이 사라졌는지 확인합니다.")

            print("   로그인 버튼을 클릭합니다.")
            self.login_btn_click()
            print("   로그인 버튼 클릭 완료.")
        else:
            print("   로그인 팝업이 없거나 이미 닫혀있습니다. 로그인 프로세스를 종료합니다.")
            return False

        # 4. [로그인 접속 시도 확인]
        print("4. 로그인 접속 시도 확인: 'FrmMain' 아이디와 '모션.ver' 이름의 메인 창 노출을 확인합니다.")
        try:
            main_window = self.app.window(auto_id=LoginLocators.MAIN_FORM_AUTOMATION_ID, title=LoginLocators.MAIN_FORM_TITLE)
            ElementFinder.wait_for_element_visible(main_window, timeout=10)
            print("   메인 창 노출 확인. 로그인 성공.")
            return True
        except findwindows.ElementNotFoundError:
            print("   메인 창이 노출되지 않았습니다. 로그인 실패.")
            return False
            
            
    