# tests/test_reception.py
import time

import pytest

from dto.user_dto import UserDTO
from utils.element_finder import ElementFinder


@pytest.mark.order(7)
def test_reserve_user(start_event, side_page, save_user_ctx, dashboard_page):
    save_user_ctx.user = UserDTO("0000004798","QA테스트1","941111-1111111", "010-7441-7631")
    user = save_user_ctx.user
    side_page.search_user(user.chart_no)
    compare_user = side_page.compare_search_user(user)
    assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
    
    side_page.search_user_reserve(user)
    start_event.set()
    side_page.reserve_user(user)
    time.sleep(2)
    
    assert dashboard_page.get_reservation_list(user.chart_no), "test_reserve_user : 환자 접수되지 않았습니다."

@pytest.mark.order(10)
def test_save_with_receive(dashboard_page, start_event, side_page, user_save_page, receive_page):
    user = UserDTO(None, "QA테스트3","941104-1111111","010-7441-7631")
    side_page.search_user(user.name)
    assert not side_page.compare_search_user(user)

    side_page.get_save_user_popup()
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
    
    assert dashboard_page.get_reservation_list(user.chart_no), "test_reserve_user : 환자 접수되지 않았습니다."

@pytest.mark.order(8)
def test_receive_cancel(dashboard_page, save_user_ctx):
    user = save_user_ctx.user
    
    assert dashboard_page.get_cancle_button("접수", user.chart_no), "test_receive_cancel : 해당하는 접수 환자가 없습니다."
    assert dashboard_page.cancle_web_popup_action(), "test_receive_cancel : 환자 접수 취소 팝업 컨트롤 실패"
    assert not dashboard_page.get_reception_list(user.chart_no), "test_receive_cancel : 환자 접수 취소를 실패했습니다."
