# tests/test_user_save.py
import time

import pytest

from dto.user_dto import UserDTO


@pytest.mark.order(4)
def test_user_save(side_page, user_save_page, start_event,save_user_ctx):
    save_user_ctx.user = UserDTO(chart_no=None, name="QA테스트1", mobile_no="010-7441-7631", jno="941104-1111111")
    
    user = save_user_ctx.user
    side_page.search_user(user.name)
    assert not side_page.compare_search_user(user), "test_save_user : 저장하려는 유저가 존재합니다. 확인해주세요."
    side_page.get_save_user_popup()
    
    time.sleep(1.5)
    
    user_save_page.get_save_user_field()
    user = user_save_page.user_info_write(user)
    
    start_event.set()
    user_save_page.user_save_and_proceed()
    
    if user:
        side_page.search_user(user.name)
        assert side_page.compare_search_user(user), "test_save_user : 검색된 유저가 존재하지 않습니다."
    else:
        assert user, "test_save_user : 저장된 유저가 없습니다."