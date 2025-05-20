import time

from dto.user_dto import UserDTO
from pages.dashboard_page import DashBoardPage
from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from pages.user_save_page import UserSavePage
from tests.test_base import *


class TestDashBoardPage(TestBase):
    def __init__(self):
        super().__init__()

        self.side_page = SidePage(self.app_manager)
        self.user_save_page = UserSavePage(self.app_manager)
        self.dashboard_page = DashBoardPage(self.app_manager)
        self.receive_page = ReceivePage(self.app_manager)
        
        self.create_time = None
        self.notice_content = "공지사항 테스트"
        self.update_content = "업데이트"
        
        self.save_user = None
        # self.test_create_notice()
        # self.test_update_notice()
        # self.test_delete_notice()
        # self.test_save_user()
        # self.test_reserve_user()
        # self.test_receive_user()
        self.test_receive_cancel()
    
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
        self.save_user = UserDTO(chart_no=None, name="QA테스트123", mobile_no="010-7441-7631", jno="941104-1111111")
        self.side_page.search_user(self.save_user.name)
        assert not self.side_page.compare_search_user(self.save_user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
        self.side_page.save_user_popup()
        
        time.sleep(2)
        self.save_user = self.user_save_page.user_info_write(self.save_user)
        
        self.start_event.set()
        self.user_save_page.user_save_and_proceed()
        
        # 저장 후 유저 검색 확인
        if self.save_user:
            self.side_page.search_user(self.save_user.name)
            assert self.side_page.compare_search_user(self.save_user), "test_save_user : 검색된 유저가 존재하지 않습니다."
        else:
            assert self.save_user, "test_save_user : 저장된 유저가 없습니다. "
    
    def test_save_with_reserve(self):
        self.save_user = UserDTO(chart_no=None, name="QA테스트2", mobile_no="010-7441-7631", jno="941104-1111111")
        self.side_page.search_user(self.save_user.name)
        assert not self.side_page.compare_search_user(self.save_user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
        self.side_page.save_user_popup()
        
        time.sleep(2)
        self.save_user = self.user_save_page.user_info_write(self.save_user)
        
        self.start_event.set()
        self.user_save_page.user_save_and_proceed(reserve=True)
        
        

    
    def test_save_with_receive(self):
        self.save_user = UserDTO(chart_no=None, name="QA테스트3", mobile_no="010-7441-7631", jno="941104-1111111")
        self.side_page.search_user(self.save_user.name)
        assert not self.side_page.compare_search_user(self.save_user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
        self.side_page.save_user_popup()
        
        time.sleep(2)
        self.save_user = self.user_save_page.user_info_write(self.save_user)
        
        self.start_event.set()
        self.user_save_page.user_save_and_proceed(receive=True)
        
        time.sleep(1)
        assert self.receive_page.get_compare_popup_text(self.save_user), "접수 팝업 데이터 확인 필요"
        
        self.receive_page.write_receive_memo("test_save_with_receive user memo", "test_save_with_receive receive memo")
        self.start_event.set()
        self.receive_page.submit_receive()
    
        time.sleep(3)
        self.start_event.set()
    
    def test_reserve_user(self):
        self.side_page.search_user(self.save_user.chart_no)
        compare_user = self.side_page.compare_search_user(self.save_user)
        assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
        
        self.side_page.search_user_reserve(self.save_user)
        self.start_event.set()
        self.side_page.reserve_user(self.save_user)

    def test_receive_user(self):
        # user_dto = UserDTO(chart_no="0000002351", name="소말리", mobile_no="010-7441-7631", jno=None)
        self.side_page.search_user(self.save_user.chart_no)
        assert self.side_page.compare_search_user(self.save_user) , "검색된 유저가 존재하지 않음"
        self.side_page.search_user_receive(self.save_user)
        
        time.sleep(1)
        assert self.receive_page.get_compare_popup_text(self.save_user), "접수 팝업 데이터 확인 필요"
        
        self.receive_page.write_receive_memo("user memo", "receive memo")
        self.start_event.set()
        self.receive_page.submit_receive()
    
        time.sleep(3)
        self.start_event.set()
    
    def test_reserve_cancel(self):
        self.dashboard_page.get_cancle_button("예약",self.save_user.chart_no)
        self.dashboard_page.reservation_cancel_popup_control()
        assert self.dashboard_page.cancle_web_popup_action(), "test_reserve_cancel : 예약 취소 화면을 확인해주세요."
        assert self.dashboard_page.get_reservation_list(self.save_user.chart_no),"test_reserve_cancel : 예약 취소가 되지않았습니다."
   
    def test_receive_cancel(self):
        self.dashboard_page.get_cancle_button("접수",self.save_user.chart_no)
        assert self.dashboard_page.cancle_web_popup_action(), "test_receive_cancel : 접수 취소 화면을 확인해주세요."
        assert self.dashboard_page.get_reception_list(self.save_user.chart_no),"test_receive_cancel : 접수 취소가 되지않았습니다."
        
    def test_reserve_user_reception(self):
        self.dashboard_page.get_reservation_list(self.save_user.chart_no)
    
    def test_open_chart(self):
        assert self.dashboard_page.open_chart(self.save_user.chart_no), "test_open_chart : 환자 차트 열기 실패"
    