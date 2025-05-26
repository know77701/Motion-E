# tests/test_notice.py
import time

import pytest


@pytest.mark.order(1)
def test_create_notice(side_page,notice_context):
    content = "공지사항 테스트"
    tries, max_tries = 0, 3
    created = False
    while tries < max_tries:
        notice_context.create_time = side_page.save_notice(content)
        if side_page.compare_notice(content, notice_context.create_time):
            created = True
            break
        tries += 1
    
    assert created, "test_create_notice : 공지사항 등록 실패"

@pytest.mark.order(2)
def test_update_notice(side_page,notice_context):
    side_page.update_notice("공지사항 테스트", notice_context.create_time, "업데이트")
    assert side_page.compare_notice("업데이트", notice_context.create_time), "test_update_notice : 공지사항 업데이트 실패"

@pytest.mark.order(3)
def test_delete_notice(side_page,notice_context):
    side_page.delete_notice("업데이트", notice_context.create_time)
    assert not side_page.compare_notice("공지사항 테스트", notice_context.create_time), "test_delete_notice : 공지사항 삭제 실패"