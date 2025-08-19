import time

import pytest

from utils.element_finder import ElementFinder


# @pytest.mark.skip()
class TestDashboardUtil():
    @pytest.fixture(autouse=True)
    def setup(self, dashboard_page, save_user_ctx):
        self.dashboard_page = dashboard_page
        self.ctx = save_user_ctx

    def _retry_find_user(self, chart_no, retries=3):
        for _ in range(retries):
            found_user = (self.dashboard_page.get_reservation_list(chart_no) 
                          or self.dashboard_page.get_reception_list(chart_no))
            if found_user:
                return found_user
            # Consider adding a small delay here if needed, but explicit waits are generally better
        return None

    @pytest.mark.order(11)
    def test_find_user(self):
        user_name = self.ctx.user.name
        chart_no = self.ctx.user.chart_no
        
        self.dashboard_page.find_user_search(user_name)
        found_user = self._retry_find_user(chart_no)
        
        assert found_user, "환자 검색 실패"
        
        ElementFinder.send_key("{F5}")
        # Consider adding a wait for an element on the dashboard to be visible/enabled after refresh
        # For example: ElementFinder.wait_for_element_visible(self.dashboard_page.parent_field)

    @pytest.mark.order(12)
    def test_open_chart(self):
        chart_no = self.ctx.user.chart_no
        # NOTE: Assuming a fixed time for now, will need to be dynamic if relevant
        assert self.dashboard_page.open_chart("예약", chart_no, "17:30"), "환자 차트를 열수없습니다."