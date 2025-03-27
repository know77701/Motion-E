import multiprocessing
import time

from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from pages.user_save_page import UserSavePage
from utils.app_manager import AppManger
from utils.multi_processing import MultiProcess


class TestSidePage:
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        
        self.window = self.app_manager.app_connect(retries=0)
        self.side_page = SidePage()
        self.user_save_page = UserSavePage()
        self.test_set_notice()
        # self.receive_page = ReceivePage()
        
        # self.start_sub_process_event = multiprocessing.Event()
        # self.sub_process_done_event = multiprocessing.Event()
        # self.test()
        
    
    def test_set_notice(self):
        # notice = "테스트"
        start_time = time.perf_counter()
        # self.side_page.search_user("0000002351")
        # self.side_page.save_user_popup()
        self.user_save_page.get_popup_field()
        
            
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function executed in: {execution_time:.4f} seconds")
    
    # def test(self):
    #     sub_process = multiprocessing.Process(
    #         target=MultiProcess.detect_and_close_popup,
    #         args=(self.start_sub_process_event, self.sub_process_done_event)
    #     )
    #     sub_process.start()
    #     self.receive_page.verify_receive_info(username="소말리", chart_number="0000002351")
    #     self.receive_page.write_receive_memo("메모","테스트메모")
        
    #     self.start_sub_process_event.set()
    #     self.receive_page.submit_receive() 
    #     self.sub_process_done_event.wait()
    #     sub_process.terminate()
    #     sub_process.join()

if __name__ == "__main__": 
    test = TestSidePage()