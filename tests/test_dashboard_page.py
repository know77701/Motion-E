import multiprocessing
import time

from dto.user_dto import UserDTO
from pages.dashboard_page import DashBoardPage
from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from pages.user_save_page import UserSavePage
from utils.app_manager import AppManger
from utils.multi_processing import MultiProcess


class TestDashBoardPage:
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        
        self.window = self.app_manager.app_connect(retries=0)
        self.side_page = SidePage()
        self.user_save_page = UserSavePage()
        self.create_time = None
        self.notice_content = "공지사항 테스트"
        self.update_content = "업데이트"
        self.user_dto = UserDTO(chart_no=None,name="소말리QA", mobile_no="010-7441-7631",jno=None)
        self.dashboard_page = DashBoardPage()
        self.test_dashboard()
        # self.test_create_notice()
        # self.test_update_notice()
        # self.test_delete_notice()
        # self.test_save_user()
        # self.test_reseve_user()
        # self.receive_page = ReceivePage()
        
        # self.start_sub_process_event = multiprocessing.Event()
        # self.sub_process_done_event = multiprocessing.Event()
        # self.test()
    
    
    def test_dashboard(self):
        self.dashboard_page.get_reservation_list()
        # self.dashboard_page.get_reception_list()
        # self.dashboard_page.get_treatment_list()
        # self.dashboard_page.get_payment_list()
        
    
    def test_create_notice(self):
        print("공지사항 생성 시작")
        start_time = time.perf_counter()
        self.create_time = self.side_page.save_notice(self.notice_content)
        if not self.side_page.compare_notice(notice_content=self.notice_content, compare_time=self.create_time):
            print("공지사항이 등록되지 않았습니다.")
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function executed in: {execution_time:.4f} seconds")
        print("공지사항 생성 종료")
        
    def test_update_notice(self):
        print("공지사항 업데이트 시작")
        self.side_page.update_notice(notice_content=self.notice_content, 
                                      create_time=self.create_time, 
                                      update_content=self.update_content)
        if not self.side_page.compare_notice(notice_content=self.update_content, compare_time=self.create_time):
            print("공지사항이 업데이트되지 않았습니다.")
        print("공지사항 업데이트 종료")
    
    def test_delete_notice(self):
        print("공지사항 삭제 시작")
        self.side_page.delete_notice(notice_content=self.notice_content, create_time=self.create_time)
        if self.side_page.compare_notice(notice_content=self.notice_content, compare_time=self.create_time):
            print("공지사항이 삭제되지 않았습니다.")
        print("공지사항 삭제 종료")
    
    def test_save_user(self):
        print("유저 저장 시작")
        self.side_page.search_user(self.user_dto.name)
        self.side_page.save_user_popup()
        self.user_save_page.user_info_write(self.user_dto)
        self.user_save_page.user_save_and_proceed("저장")
        print("유저 저장 종료")
    
    def test_reseve_user(self):
        print("유저 예약 시작")
        user_dto = UserDTO(chart_no="0000002351",name="소말리", mobile_no="010-7441-7631",jno=None)
        self.side_page.search_user(user_dto.chart_no)
        if self.side_page.compare_search_user(user_dto):
            print("검색된 유저가 존재하지 않습니다.")
        self.side_page.search_user_reserve(user_dto)
        self.side_page.reserve_user(user_dto)
        print("유저 예약 종료")

    def test_receive_user(self):
        print("유저 접수 시작")
        user_dto = UserDTO(chart_no="0000002351", name="소말리", mobile_no="010-7441-7631", jno=None)
        self.side_page.search_user(user_dto.chart_no)
        if self.side_page.compare_search_user(user_dto):
            print("검색된 유저가 존재하지 않습니다.")
        self.side_page.search_user_receive(user_dto)
        if self.receive_page.get_compare_popup_text(user_dto):
            print("접수 팝업 데이터를 확인해주세요.")
        self.receive_page.write_receive_memo("user memo", "receive memo")
        self.receive_page.submit_receive()

    

if __name__ == "__main__": 
    test = TestDashBoardPage()