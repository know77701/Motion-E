import multiprocessing
import time
from multiprocessing import Process

from dto.user_dto import UserDTO
from pages.dashboard_page import DashBoardPage
from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from pages.user_save_page import UserSavePage
from utils.app_manager import AppManger
from utils.popup_handler import popupHandler


class TestDashBoardPage:
    def __init__(self):
        self.app_manager = AppManger()
        self.app_manager.check_admin()
        
        self.side_page = SidePage(self.app_manager)
        self.user_save_page = UserSavePage(self.app_manager)
        self.dashboard_page = DashBoardPage(self.app_manager)
        self.receive_page = ReceivePage(self.app_manager)
        self.popup_handler = popupHandler(self.app_manager)
        
        self.window = self.app_manager.motion_app_connect(retries=0)
        
        self.create_time = None
        self.notice_content = "공지사항 테스트"
        self.update_content = "업데이트"
        
        self.user_dto = UserDTO(chart_no=None,name="소말리QA", mobile_no="010-7441-7631",jno="941111-1111111")
        
        # self.test_create_notice()
        # self.test_update_notice()
        # self.test_delete_notice()
        # self.test_save_user()
        # self.test_reseve_user()
        self.test_receive_user()
    
    def test_create_notice(self):
        self.create_time = self.side_page.save_notice(self.notice_content)
        assert self.side_page.compare_notice(notice_content=self.notice_content, compare_time=self.create_time), "test_create_notice, 공지사항이 등록되지 않았습니다."
        
    def test_update_notice(self):
        self.side_page.update_notice(notice_content=self.notice_content, 
                                      create_time=self.create_time, 
                                      update_content=self.update_content)
        assert self.side_page.compare_notice(notice_content=self.update_content, compare_time=self.create_time), "test_update_notice, 공지사항 업데이트 실패"
    
    def test_delete_notice(self):
        self.side_page.delete_notice(notice_content=self.notice_content, create_time=self.create_time)
        assert self.side_page.compare_notice(notice_content=self.notice_content, compare_time=self.create_time), "test_delete_notice, 공지사항 삭제 실패"
    
    
    def test_save_user(self):
        self.side_page.search_user(self.user_dto.name)
        self.side_page.save_user_popup()
        
        save_user = self.user_save_page.user_info_write(self.user_dto)
        self.user_save_page.user_save_and_proceed("저장")
        
        # 저장 후 유저 검색 확인
        self.side_page.search_user(self.user_dto.name)
        assert self.side_page.compare_search_user(save_user), "저장된 데이터가 존재하지않음."
    
    def test_reseve_user(self):
        user_dto = UserDTO(chart_no="0000002351",name="소말리", mobile_no="010-7441-7631",jno="941111-1111111")
        
        self.side_page.search_user(user_dto.chart_no)
        assert self.side_page.compare_search_user(user_dto), "검색된 유저 존재하지 않음"
        
        self.side_page.search_user_reserve(user_dto)
        self.side_page.reserve_user(user_dto)

    def test_receive_user(self):
        user_dto = UserDTO(chart_no="0000002351", name="소말리", mobile_no="010-7441-7631", jno=None)
        self.side_page.search_user(user_dto.chart_no)
        
        assert self.side_page.compare_search_user(user_dto) , "검색된 유저가 존재하지 않음"
        self.side_page.search_user_receive(user_dto)
        time.sleep(1)
        
        assert self.receive_page.get_compare_popup_text(user_dto), "접수 팝업 데이터 확인 필요"
        self.receive_page.write_receive_memo("user memo", "receive memo")
        p = Process(target=self.popup_handler.close_receive_popup_handler, args=())
        p.start()
        self.receive_page.submit_receive()
        p.join()
    
    def test_reservation_cancel(self):
        self.dashboard_page.reservation_cancel(self.user_dto.chart_no)
        assert self.dashboard_page.get_reservation_list(self.user_dto.chart_no),"예약 취소가 되지않았습니다."
   
    def test_reception_cancel(self):
        self.dashboard_page.reception_cancel(self.user_dto.chart_no)
        assert self.dashboard_page.get_reception_list(self.user_dto.chart_no),"접수 취소가 되지않았습니다."

    def test_reserve_user_reception(self):
        self.dashboard_page.get_reception_list(self.user_dto.chart_no)
    
    def test_open_chart(self):
        self.user_dto.chart_no = "0000002351"
        assert self.dashboard_page.open_chart(self.user_dto.chart_no), "test_open_chart, 환자 차트 열기 실패"
    
if __name__ == "__main__": 
    test = TestDashBoardPage()