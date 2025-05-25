# tests/test_user_save.py
from dto.user_dto import UserDTO
import pytest
import time

@pytest.mark.order(4)
def test_save_user(side_page, user_save_page, start_event):
    save_user = UserDTO(chart_no="0000004793", name="김지헌", mobile_no="010-7441-7631", jno="941104-1111111")
    side_page.search_user(save_user.name)
    assert not side_page.compare_search_user(save_user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
    side_page.get_save_user_popup()
    
    time.sleep(1.5)
    user_save_page.get_save_user_field()
    save_user = user_save_page.user_info_write(save_user)
    
    user_save_page.user_save_and_proceed()
    time.sleep(1)
    start_event.set()
    
    # 저장 후 유저 검색 확인
    if save_user:
        side_page.search_user(save_user.name)
        assert side_page.compare_search_user(save_user), "test_save_user : 검색된 유저가 존재하지 않습니다."
    else:
        assert save_user, "test_save_user : 저장된 유저가 없습니다."