import time

import pytest

from dto.user_dto import UserDTO
from utils.element_finder import ElementFinder


@pytest.mark.usefixtures("side_page","save_user_ctx","dashboard_page")
class TestReservation():
    @pytest.fixture(autouse=True)
    def setup(self,side_page, dashboard_page, save_user_ctx):
        self.side_page = side_page
        self.dashboard_page = dashboard_page
        self.notice_crate_time = None
        self.user = save_user_ctx.user

    @pytest.mark.order(5)
    def test_reserve_user(self, start_event):
        while True:
            self.side_page.search_user(self.user.chart_no)
            compare_user = self.side_page.compare_search_user(self.user)
            assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
            
            self.side_page.search_user_reserve(self.user)
            result = start_event.set()
            if result:
                self.side_page.reserve_user(self.user)
                time.sleep(1)
                
                assert self.dashboard_page.get_reservation_list(self.user.chart_no), "test_reserve_user : 환자 예약실패"
            else:
                continue
        

    @pytest.mark.order(9)
    def test_save_with_reserve(self, start_event, user_save_page):
        user = UserDTO(None, "QA테스트2", "941104-1111111", "010-7441-7631")
        self.side_page.search_user(user.name)
        assert not self.side_page.compare_search_user(user)

        self.side_page.get_save_user_popup()
        time.sleep(1.5)
        user_save_page.get_save_user_field()
        user = user_save_page.user_info_write(user)
        start_event.set()
        user_save_page.user_save_and_proceed(reserve=True)

        self.side_page.reserve_user(user)
        start_event.set()
        time.sleep(1)
        ElementFinder.send_key("{F1}")
        time.sleep(1)
        assert self.dashboard_page.get_reservation_list(user.chart_no), "test_save_with_reserve : 환자 저장 후 예약 실패" 

    @pytest.mark.order(6)
    def test_reserve_cancel(self):
        assert self.dashboard_page.get_cancle_button("예약",  self.user.chart_no), "test_reserve_cancel : 해당하는 예약 환자가 없습니다."
        self.dashboard_page.reservation_cancel_popup_control()
        assert self.dashboard_page.cancle_web_popup_action(), "test_reserve_cancel : 환자 예약취소 웹 팝업 컨트롤 실패"
        assert not self.dashboard_page.get_reservation_list( self.user.chart_no), " test_reserve_cancel : 환자 예약 취소 실패"
