# tests/test_reception.py
from dto.user_dto import UserDTO
import pytest
import time
from utils.element_finder import ElementFinder

# @pytest.mark.order(7)
def test_save_with_receive(side_page, user_save_page, receive_page):
    user = UserDTO(None, "QA테스트3", "010-7441-7631", "941104-1111111")
    side_page.search_user(user.name)
    assert not side_page.compare_search_user(user)

    side_page.get_save_user_popup()
    time.sleep(2)
    user_save_page.get_save_user_field()
    user = user_save_page.user_info_write(user)
    user_save_page.user_save_and_proceed(receive=True)

    assert receive_page.get_compare_popup_text(user)
    receive_page.write_receive_memo("user memo", "receive memo")
    receive_page.submit_receive()
    time.sleep(1.5)

# @pytest.mark.order(8)
def test_receive_cancel(dashboard):
    chart_no = "0000000001"  # 예시
    assert dashboard.get_cancle_button("접수", chart_no)
    assert dashboard.cancle_web_popup_action()
    assert not dashboard.get_reception_list(chart_no)
