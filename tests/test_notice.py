# tests/test_notice.py
import pytest
import time

@pytest.mark.order(1)
def test_create_notice(side_page):
    content = "공지사항 테스트"
    tries, max_tries = 0, 3
    created = False
    while tries < max_tries:
        create_time = side_page.save_notice(content)
        if side_page.compare_notice(content, create_time):
            created = True
            break
        tries += 1
    assert created, "공지사항 등록 실패"

@pytest.mark.order(2)
def test_update_notice(side_page):
    assert side_page.update_notice("공지사항 테스트", None, "업데이트")
    assert side_page.compare_notice("업데이트", None), "공지사항 업데이트 실패"

@pytest.mark.order(3)
def test_delete_notice(side_page):
    assert side_page.delete_notice("업데이트", None)
    assert not side_page.compare_notice("공지사항 테스트", None), "공지사항 삭제 실패"