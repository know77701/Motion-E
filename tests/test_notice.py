# tests/test_notice.py
import time

import pytest


@pytest.mark.usefixtures("app_manager", "side_page")
class TestNotice():
    @pytest.fixture(autouse=True)
    def setup(self,app_manager, side_page):
        self.dashboard = app_manager
        self.side_page = side_page
        self.notice_crate_time = None

    @pytest.mark.order(1)
    def test_create_notice(self):
        content = "공지사항 테스트"
        tries, max_tries = 0, 3
        created = False
        
        while tries < max_tries:
            self.notice_crate_time = self.side_page.save_notice(content)
        
            if self.side_page.compare_notice(content, self.notice_crate_time):
                created = True
                break
            tries += 1

        assert created, "test_create_notice : 공지사항 등록 실패"

    @pytest.mark.order(2)
    def test_update_notice(self):
        self.side_page.update_notice("공지사항 테스트", self.notice_crate_time, "업데이트")
        assert self.side_page.compare_notice("업데이트", self.notice_crate_time), "test_update_notice : 공지사항 업데이트 실패"

    @pytest.mark.order(3)
    def test_delete_notice(self):
        self.side_page.delete_notice("업데이트", self.notice_crate_time)
        assert not self.side_page.compare_notice("공지사항 테스트", self.notice_crate_time), "test_delete_notice : 공지사항 삭제 실패"