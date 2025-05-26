import time

import pytest

from dto.user_dto import UserDTO
from utils.element_finder import ElementFinder


@pytest.mark.order(5)
def test_reserve_user(start_event, side_page, dashboard_page, save_user_ctx):
    while True:
        save_user_ctx.user = UserDTO("0000004798","QA테스트1","941111-1111111", "010-7441-7631")
        user = save_user_ctx.user
        
        side_page.search_user(user.chart_no)
        compare_user = side_page.compare_search_user(user)
        assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
        
        side_page.search_user_reserve(user)
        result = start_event.set()
        if result:
            side_page.reserve_user(user)
            time.sleep(1)
            
            assert dashboard_page.get_reservation_list(user.chart_no), "test_reserve_user : 환자 예약실패"
        else:
            continue
    

@pytest.mark.order(9)
def test_save_with_reserve(start_event, side_page, user_save_page, dashboard_page):
    user = UserDTO(None, "QA테스트2", "941104-1111111", "010-7441-7631")
    side_page.search_user(user.name)
    assert not side_page.compare_search_user(user)

    side_page.get_save_user_popup()
    time.sleep(1.5)
    user_save_page.get_save_user_field()
    user = user_save_page.user_info_write(user)
    start_event.set()
    user_save_page.user_save_and_proceed(reserve=True)

    side_page.reserve_user(user)
    start_event.set()
    time.sleep(1)
    ElementFinder.send_key("{F1}")
    time.sleep(1)
    assert dashboard_page.get_reservation_list(user.chart_no), "test_save_with_reserve : 환자 저장 후 예약 실패" 

@pytest.mark.order(6)
def test_reserve_cancel(dashboard_page, save_user):
    chart_no = save_user.chart_no 
    
    assert dashboard_page.get_cancle_button("예약", chart_no), "test_reserve_cancel : 해당하는 예약 환자가 없습니다."
    dashboard_page.reservation_cancel_popup_control()
    assert dashboard_page.cancle_web_popup_action(), "test_reserve_cancel : 환자 예약취소 웹 팝업 컨트롤 실패"
    assert not dashboard_page.get_reservation_list(chart_no), " test_reserve_cancel : 환자 예약 취소 실패"
