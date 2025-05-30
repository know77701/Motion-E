import time

import pytest

from utils.element_finder import ElementFinder


# @pytest.mark.skip()
class TestDashboardUtil():
    @pytest.fixture(autouse=True)
    def setup(self, dashboard_page, save_user_ctx):
        self.dashboard_page = dashboard_page
        self.ctx = save_user_ctx

    @pytest.mark.skip()
    @pytest.mark.order(11)
    def test_find_user(self):
        user = self.ctx.user
        name = user.name
        chart_no = user.chart_no
        
        self.dashboard_page.find_user_search(name)
        found_user = (self.dashboard_page.get_reservation_list(chart_no) 
                      or self.dashboard_page.get_reception_list(chart_no))
        assert found_user, "환자 검색 실패"
        
        ElementFinder.send_key("{F5}")
        time.sleep(0.5)

    @pytest.mark.order(12)
    def test_open_chart(self):
        chart_no = "0000002351"
        assert self.dashboard_page.open_chart("접수",chart_no, "13:17"), "환자 차트를 열수없습니다."