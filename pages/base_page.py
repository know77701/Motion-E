from pywinauto.application import Application


class BasePage:
    def __init__(self, app: Application):
        self.app = app

    def find_element(self, auto_id=None, control_type=None, title=None):
        return self.app.window().child_window(auto_id=auto_id, control_type=control_type, title=title)

    def click(self, element):
        """클릭 액션"""
        if element.exists():
            element.click()
        else:
            raise Exception(f"요소를 찾을 수 없음: {element}")

    def input_text(self, element, text):
        """텍스트 입력"""
        if element.exists():
            element.set_focus()
            element.set_text(text)
        else:
            raise Exception(f"입력할 수 없음: {element}")