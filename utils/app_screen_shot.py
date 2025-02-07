import os
from functools import partial

from PIL import ImageGrab

import config


def window_screen_shot(save_file_name):
    """스크린샷 캡처 후 저장"""
    retry = 0
    while retry <= config.MAX_RETRY:
        if os.path.exists(config.SCREENSHOT_SAVE_DIR):
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
            screenshot_path = os.path.join(config.SCREENSHOT_SAVE_DIR, save_file_name + ".jpg")
            save_image = ImageGrab.grab()
            save_image.save(screenshot_path)
            print(f": {screenshot_path}")
            break
        else:
            print("경로 생성")
            create_screenshot_folder()
            retry += 1

def create_screenshot_folder():
    """스크린샷 저장 폴더 생성"""
    os.makedirs(config.SCREENSHOT_SAVE_DIR, exist_ok=True)