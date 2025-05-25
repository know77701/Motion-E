import pytest
import time
from pages.dashboard_page import DashBoardPage
from utils.element_finder import ElementFinder
from utils.app_manager import AppManger

@pytest.mark.usefixtures("app_manager")
class TestDashboardUtil():
    @pytest.fixture(autouse=True)
    def setup(self,app_manager):
        self.dashboard = DashBoardPage(app_manager)
        

    @pytest.mark.order(9)
    def test_find_user(self):
        self.dashboard.find_user_search("소말리")
        chart_no = "0000002351"
        found_user = self.dashboard.get_reservation_list(chart_no) or self.dashboard.get_reception_list(chart_no)
        assert found_user, "환자 검색 실패"
        ElementFinder.send_key("{F5}")
        time.sleep(0.5)

    @pytest.mark.order(10)
    def test_open_chart(self):
        chart_no = "0000002351"
        assert self.dashboard.open_chart(chart_no), "환자 차트를 열수없습니다."
