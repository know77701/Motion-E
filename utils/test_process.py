from tests.test_chart import *
from tests.test_dashboard_page import *
from tests.test_login import *


def test_runner(start_event):
    # login = TestLogin(start_event)
    dashboard = TestDashBoardPage(start_event)
    # chart = TestChart(start_event)