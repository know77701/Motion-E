import time

from pages.side_page import SidePage
from utils.app_manager import AppManger


class TestSidePage:
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        
        self.window = self.app_manager.app_connect(retries=0)
        self.side_page = SidePage(self.window)
        self.test_set_notice()
    
    def test_set_notice(self):
        notice = "테스트"
        start_time = time.perf_counter()
        # current_time = self.side_page.save_notice(notice)
        # self.side_page.compare_notice(notice, current_time)
        # self.side_page.delete_notice(notice)
        # self.side_page.update_notice(notice)
        # self.side_page.search_user("소말리")
        # self.side_page.compare_search_user("소말리")
        self.side_page.get_search_user_list()
        end_time = time.perf_counter()
        execution_time = end_time - start_time  # 실행 시간 차이
        print(f"Function executed in: {execution_time:.4f} seconds")
        return
    