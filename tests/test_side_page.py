import multiprocessing
import time

from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from utils.app_manager import AppManger
from utils.multi_processing import MultiProcess


class TestSidePage:
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        
        self.window = self.app_manager.app_connect(retries=0)
        self.side_page = SidePage()
        # self.test_set_notice()
        self.receive_page = ReceivePage()
        self.test()
        
    
    def test_set_notice(self):
        # notice = "테스트"
        start_time = time.perf_counter()
        self.side_page.search_user_receive("김지헌", "0000003392")
        time.sleep(1)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function executed in: {execution_time:.4f} seconds")
    
    def test(self):
        self.receive_page.verify_receive_info(username="소말리", chart_number="0000002351")
        self.receive_page.write_receive_memo("메모","테스트메모")
        
        stop_event = multiprocessing.Event()
        process = multiprocessing.Process(
            target=MultiProcess.detect_and_close_popup,
            args=(stop_event,)
        )

        process.start()
        self.receive_page.submit_receive()  # 팝업을 발생시키는 함수
        # stop_event.set()  # 팝업 감지를 멈추도록 이벤트 설정
        # process.join()  # 프로세스 종료까지 대기


if __name__ == "__main__": 
    test = TestSidePage()