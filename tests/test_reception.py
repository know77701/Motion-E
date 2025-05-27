# tests/test_reception.py
import time

import pytest

from dto.user_dto import UserDTO
from utils.element_finder import ElementFinder


@pytest.mark.usefixtures("app_manager", "side_page","dashboard_page","save_user_ctx")
class TestReception():
    @pytest.fixture(autouse=True)
    def setup(self,side_page, dashboard_page, save_user_ctx):
        self.side_page = side_page
        self.dashboard_page = dashboard_page
        self.notice_crate_time = None
        self.user = save_user_ctx.user

    @pytest.mark.order(7)
    def test_reserve_user(self, start_event):
        self.side_page.search_user(self.user.chart_no)
        compare_user = self.side_page.compare_search_user(self.user)
        assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
        
        self.side_page.search_user_reserve(self.user)
        start_event.set()
        self.side_page.reserve_user(self.user)
        time.sleep(2)
        
        assert self.dashboard_page.get_reservation_list(self.user.chart_no), "test_reserve_user : 환자 접수되지 않았습니다."

    @pytest.mark.order(10)
    def test_save_with_receive(self, receive_page, user_save_page, start_event):
        user = UserDTO(None, "QA테스트3","941104-1111111","010-7441-7631")
        self.side_page.search_user(user.name)
        assert not self.side_page.compare_search_user(user)

        self.side_page.get_save_user_popup()
        time.sleep(2)
        user_save_page.get_save_user_field()
        user = user_save_page.user_info_write(user)
        
        start_event.set()    
        user_save_page.user_save_and_proceed(receive=True)

        
        assert receive_page.get_compare_popup_text(user), "test_save_with_receive : 접수 팝업 환자 정보 확인"
        receive_page.write_receive_memo("user memo", "receive memo")
        start_event.set()
        receive_page.submit_receive()
        time.sleep(1.5)
        
        assert self.dashboard_page.get_reservation_list(user.chart_no), "test_reserve_user : 환자 접수되지 않았습니다."

    @pytest.mark.order(8)
    def test_receive_cancel(self):
        assert self.dashboard_page.get_cancle_button("접수", self.user.chart_no), "test_receive_cancel : 해당하는 접수 환자가 없습니다."
        assert self.dashboard_page.cancle_web_popup_action(), "test_receive_cancel : 환자 접수 취소 팝업 컨트롤 실패"
        assert not self.dashboard_page.get_reception_list(self.user.chart_no), "test_receive_cancel : 환자 접수 취소를 실패했습니다."
