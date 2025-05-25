from dto.user_dto import UserDTO
import pytest
import time
from utils.element_finder import ElementFinder

def test_reserve_user(start_event, side_page, dashboard, save_user):
        side_page.search_user(save_user.chart_no)
        compare_user = side_page.compare_search_user(save_user)
        assert compare_user, "test_reserve_user : 검색된 유저가 존재하지 않습니다."
        
        side_page.search_user_reserve(save_user)
        start_event.set()
        side_page.reserve_user(save_user)
        time.sleep(2)
        
        assert dashboard.get_reservation_list(save_user.chart_no), "test_reserve_user : 환자 예약되지 않았습니다."
    

# @pytest.mark.order(5)
def test_save_with_reserve(start_event, side_page, user_save_page, dashboard):
    user = UserDTO(None, "QA테스트2", "010-7441-7631", "941104-1111111")
    side_page.search_user(user.name)
    assert not side_page.compare_search_user(user)

    side_page.get_save_user_popup()
    time.sleep(1.5)
    user_save_page.get_save_user_field()
    user = user_save_page.user_info_write(user)
    start_event.set()
    user_save_page.user_save_and_proceed(reserve=True)

    side_page.reserve_user(user)
    ElementFinder.send_key("{F1}")
    time.sleep(1)
    assert dashboard.get_reservation_list(user.chart_no)

# @pytest.mark.order(6)
def test_reserve_cancel(dashboard, save_user):
    chart_no = save_user.chart_no  # 예시
    assert dashboard.get_cancle_button("예약", chart_no), "해당하는 차트 환자가 없습니다."
    dashboard.reservation_cancel_popup_control()
    assert dashboard.cancle_web_popup_action()
    assert not dashboard.get_reservation_list(chart_no)
