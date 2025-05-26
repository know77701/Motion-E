import time

from dto.user_dto import UserDTO
from pages.dashboard_page import DashBoardPage
from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from pages.user_save_page import UserSavePage
from tests.test_base import *
from utils.element_finder import ElementFinder


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
        
        self.save_user = UserDTO(chart_no=None, name=None, mobile_no=None, jno=None)
        # self.test_create_notice()
        # self.test_update_notice()
        # self.test_delete_notice()
        
        self.test_save_user()
        # self.test_reserve_user()
        # self.test_receive_user()
        # self.test_receive_cancel()
        # self.test_reserve_cancel()
        
        # self.test_save_with_reserve()
        # self.test_save_with_receive()
        # self.test_find_user()
    
    def test_create_notice(self):
        """
        공지사항 생성 테스트
        - 공지사항을 등록하고, 등록이 확인될 때까지 최대 3회까지 재시도
        """
        tries = 0
        max_tries = 3

        while tries < max_tries:
            self.create_time = self.side_page.save_notice(self.notice_content)
            is_created = self.side_page.compare_notice(notice_content=self.notice_content,compare_time=self.create_time)
            if is_created:
                break  # 등록 확인되면 루프 탈출
            tries += 1
        
        assert is_created,"test_create_notice, 공지사항 등록 실패"
        
    def test_update_notice(self):
        """
            공지사항 업데이트
        """
        self.side_page.update_notice(notice_content=self.notice_content, 
                                      create_time=self.create_time, 
                                      update_content=self.update_content)
        assert self.side_page.compare_notice(notice_content=self.update_content, compare_time=self.create_time), "test_update_notice, 공지사항 업데이트 실패"
    
    def test_delete_notice(self):
        """
            공지사항 삭제        
        """
        self.side_page.delete_notice(notice_content=self.update_content, create_time=self.create_time)
        assert not self.side_page.compare_notice(notice_content=self.notice_content, compare_time=self.create_time), "test_delete_notice, 공지사항 삭제 실패"
    
    def test_find_user(self):
        self.dashboard_page.find_user_search("소말리")
        if not self.dashboard_page.get_reservation_list("0000002351"):
            assert self.dashboard_page.get_reception_list("0000002351"), "test_find_user :  환자 검색되지 않음"
        
        time.sleep(0.5)
        ElementFinder.send_key("{F5}")
    
    def test_save_user(self):
        """
            환자 저장
        """
        self.save_user = UserDTO(chart_no=None, name="QA테스트1", mobile_no="010-7441-7631", jno="941104-1111111")
        self.side_page.search_user(self.save_user.name)
        assert not self.side_page.compare_search_user(self.save_user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
        self.side_page.get_save_user_popup()
        
        time.sleep(1.5)
        self.user_save_page.get_save_user_field()
        self.save_user = self.user_save_page.user_info_write(self.save_user)
        
        self.start_event.set()
        self.user_save_page.user_save_and_proceed()
        
        # 저장 후 유저 검색 확인
        if self.save_user:
            self.side_page.search_user(self.save_user.name)
            assert self.side_page.compare_search_user(self.save_user), "test_save_user : 검색된 유저가 존재하지 않습니다."
        else:
            assert self.save_user, "test_save_user : 저장된 유저가 없습니다."
    
    def test_save_with_reserve(self):
        """
            환자 저장 후 예약
        """
        self.save_user = UserDTO(chart_no=None, name="QA테스트", mobile_no="010-7441-7631", jno="941104-1111111")
        self.side_page.search_user(self.save_user.name)
        assert not self.side_page.compare_search_user(self.save_user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
        self.side_page.get_save_user_popup()
        
        time.sleep(1.5)
        self.user_save_page.get_save_user_field()
        self.save_user = self.user_save_page.user_info_write(self.save_user)
        
        self.start_event.set()
        self.user_save_page.user_save_and_proceed(reserve=True)
        
        if self.save_user:
            self.side_page.reserve_user(self.save_user)
        
        ElementFinder.send_key("{F1}")
        time.sleep(1)
    
    def test_save_with_receive(self):
        """
            환자 저장 후 접수
        """
        self.save_user = UserDTO(chart_no=None, name="QA테스트3", mobile_no="010-7441-7631", jno="941104-1111111")
        self.side_page.search_user(self.save_user.name)
        assert not self.side_page.compare_search_user(self.save_user), "test_save_with_receive : 저장하려는 유저가 존재합니다. 확인해주세요."
        self.side_page.get_save_user_popup()
        
        time.sleep(2)
        self.user_save_page.get_save_user_field()
        self.save_user = self.user_save_page.user_info_write(self.save_user)
        
        self.start_event.set()
        self.user_save_page.user_save_and_proceed(receive=True)
        
        assert self.receive_page.get_compare_popup_text(self.save_user), "test_save_with_receive : 접수 팝업 데이터 확인 필요"
        
        self.receive_page.write_receive_memo("test_save_with_receive user memo", "test_save_with_receive receive memo")
        self.start_event.set()
        self.receive_page.submit_receive()
    
        time.sleep(1.5)
        self.start_event.set()
    
    def test_reserve_user(self):
        self.side_page.search_user(self.save_user.chart_no)
        compare_user = self.side_page.compare_search_user(self.save_user)
        assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
        
        self.side_page.search_user_reserve(self.save_user)
        self.start_event.set()
        self.side_page.reserve_user(self.save_user)
        time.sleep(2)
        
        assert self.dashboard_page.get_reservation_list(self.save_user.chart_no), "test_reserve_user : 환자 예약되지 않았습니다."

    def test_receive_user(self):
        self.side_page.search_user(self.save_user.chart_no)
        assert self.side_page.compare_search_user(self.save_user) , "검색된 유저가 존재하지 않음"
        self.side_page.search_user_receive(self.save_user)
        
        time.sleep(1)
        assert self.receive_page.get_compare_popup_text(self.save_user), "접수 팝업 데이터 확인 필요"
        
        self.receive_page.write_receive_memo("user memo", "receive memo")

        self.start_event.set()
        self.receive_page.submit_receive()
        self.start_event.set()
        
        ElementFinder.send_key("{F5}")
        time.sleep(1)
        assert self.dashboard_page.get_reception_list(self.save_user.chart_no), "test_receive_user : 환자 접수되지 않았습니다."
    
    def test_reserve_cancel(self):
        assert self.dashboard_page.get_cancle_button("예약",self.save_user.chart_no), "test_reserve_cancel : 예약 취소할 환자가 존재하지 않습니다."
        self.dashboard_page.reservation_cancel_popup_control()
        assert self.dashboard_page.cancle_web_popup_action(), "test_reserve_cancel : 예약 취소 화면을 확인해주세요."
        assert not self.dashboard_page.get_reservation_list(self.save_user.chart_no),"test_reserve_cancel : 예약 취소가 되지않았습니다."
   
    def test_receive_cancel(self):
        assert self.dashboard_page.get_cancle_button("접수",self.save_user.chart_no), "test_receive_cancel : 접수 환자가 존재하지 않습니다." 
        assert self.dashboard_page.cancle_web_popup_action(), "test_receive_cancel : 접수 취소 화면을 확인해주세요."
        assert not self.dashboard_page.get_reception_list(self.save_user.chart_no),"test_receive_cancel : 접수 취소가 되지않았습니다."
    
    def test_check_reserve_receive_cancellation():
        return
    
    def test_open_chart(self):
        assert self.dashboard_page.open_chart(self.save_user.chart_no), "test_open_chart : 환자 차트 열기 실패"
    