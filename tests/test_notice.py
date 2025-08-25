# tests/test_notice.py
import time

import pytest


# @pytest.mark.skip()
class TestNotice():
    @pytest.fixture(autouse=True)
    def setup(self, dashboard_page, side_page, notice_context):
        self.dashboard = dashboard_page
        self.side_page = side_page
        self.ctx = notice_context

    def _retry_save_notice(self, content, retries=3):
        for _ in range(retries):
            create_time = self.side_page.save_notice(content)
            if create_time and self.side_page.compare_notice(content, create_time):
                return create_time
        return None

    @pytest.mark.order(1)
    def test_create_notice(self):
        created_time = self._retry_save_notice(self.ctx.create_content)
        self.ctx.create_time = created_time
        assert created_time, "test_create_notice : 공지사항 등록 실패"

    @pytest.mark.order(2)
    def test_update_notice(self):
        self.side_page.update_notice(self.ctx.create_content, self.ctx.create_time, self.ctx.update_content)
        assert self.side_page.compare_notice(self.ctx.update_content, self.ctx.create_time), "test_update_notice : 공지사항 업데이트 실패"

    @pytest.mark.order(3)
    def test_delete_notice(self):
        self.side_page.delete_notice(self.ctx.update_content, self.ctx.create_time)
        assert not self.side_page.compare_notice(self.ctx.update_content, self.ctx.create_time), "test_delete_notice : 공지사항 삭제 실패"
