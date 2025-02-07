from pywinauto import findwindows, keyboard, mouse

import config
from locators.login_locators import LoginLocators
from utils.app_screen_shot import window_screen_shot


class LoginPage:
    """
        로그인 객체 모음
    """
    def __init__(self, app):
        self.login_window = app.window(title=LoginLocators.LOGIN_FORM_TITLE)
        
    def login_info(self):
        keyboard.send_keys("^h")
        yakiho_text = self.login_window.child_window(auto_id=LoginLocators.YKIHO_TEXT_ID)

        if not yakiho_text.exists():
            raise Exception("야키호 텍스트 박스를 찾을 수 없습니다.")

        yakiho_text = yakiho_text.wrapper_object()  # 컨트롤 객체 변환

        try:
            # 텍스트 가져오기
            current_text = yakiho_text.window_text()
            print(f"현재 입력된 값: {current_text}")
        except AttributeError:
            # get_value()가 없으면 texts() 사용
            current_text = yakiho_text.texts()[0] if yakiho_text.texts() else ""
            print(f"현재 입력된 값: {current_text}")

        return current_text



    
    def setting_yakiho(self):
        yakiho_text = self.login_window.child_window(auto_id=LoginLocators.YKIHO_TEXT_ID)

        if yakiho_text == "22222222":
            print("개발차트 확인")
            return
        else:
            yakiho_text.set_focus()            
            yakiho_text.set_text("22222222")          
    
    def login_click(self):
        try:
            self.login_window.child_window(auto_id=LoginLocators.LOGIN_BUTTON_ID).click()
        except Exception as e:
            print("로그인 실패")
            window_screen_shot("login_click_fail")
            
            
    