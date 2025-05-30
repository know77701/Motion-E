# tests/test_notice.py
import time

import pytest


@pytest.mark.skip()
class TestNotice():
    @pytest.fixture(autouse=True)
    def setup(self, dashboard_page, side_page, notice_context):
        self.dashboard = dashboard_page
        self.side_page = side_page
        self.ctx = notice_context

    @pytest.mark.order(1)
    def test_create_notice(self):
        tries, max_tries = 0, 3
        created = False
        
        while tries < max_tries:
            self.ctx.create_time = self.side_page.save_notice(self.ctx.create_content)
            if self.side_page.compare_notice(self.ctx.create_content, self.ctx.create_time):
                created = True
                break
            tries += 1
            
        assert created, "test_create_notice : 공지사항 등록 실패"

    @pytest.mark.order(2)
    def test_update_notice(self):
        self.side_page.update_notice(self.ctx.create_content, self.ctx.create_time, self.ctx.update_content)
        assert self.side_page.compare_notice(self.ctx.update_content, self.ctx.create_time), "test_update_notice : 공지사항 업데이트 실패"

    @pytest.mark.order(3)
    def test_delete_notice(self):
        self.side_page.delete_notice(self.ctx.update_content, self.ctx.create_time)
        assert not self.side_page.compare_notice(self.ctx.update_content, self.ctx.create_time), "test_delete_notice : 공지사항 삭제 실패"
