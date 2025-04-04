import os
from functools import partial

from PIL import ImageGrab

from locators.util_locators import UtilLocators


def window_screen_shot(save_file_name):
    """스크린샷 캡처 후 저장"""
    retry = 0
    while retry <= 3:
        if os.path.exists(UtilLocators.SCREENSHOT_SAVE_DIR):
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
            screenshot_path = os.path.join(UtilLocators.SCREENSHOT_SAVE_DIR, save_file_name + ".jpg")
            save_image = ImageGrab.grab()
            save_image.save(screenshot_path)
            break
        else:
            create_screenshot_folder()
            retry += 1

def create_screenshot_folder():
    """스크린샷 저장 폴더 생성"""
    os.makedirs(UtilLocators.SCREENSHOT_SAVE_DIR, exist_ok=True)