from pywinauto import findwindows, keyboard, mouse

from locators.login_locators import LoginLocators
from utils.app_screen_shot import window_screen_shot
from utils.element_finder import ElementFinder

class LoginPage:
    """
        로그인 객체 모음
    """
    def __init__(self, app):
        self.login_window = app.window(title=LoginLocators.LOGIN_FORM_TITLE)
    
    """병원정보 영역 보이기"""
    def hospital_info_view(self):
        keyboard.send_keys("^h")
        yakiho_window = self.login_window.child_window(auto_id=LoginLocators.YAKIHO_TEXT_ID)
        if not yakiho_window.exists():
            raise Exception("요양기관번호 입력영역을 찾을 수 없습니다.")
    
    """요양기관번호 입력"""
    def hospital_yakiho_setting(self, value):
        edit = ElementFinder.find_element(self.login_window,auto_id=LoginLocators.YAKIHO_TEXT_ID).wrapper_object().children()[0]
        if edit:
            ElementFinder.input_text(edit,value)
        save_btn = ElementFinder.find_element(self.login_window,title="저장").wrapper_object()
        if save_btn:
            ElementFinder.click(save_btn)
        

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
            
            
    