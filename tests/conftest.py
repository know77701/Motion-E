import threading

import pytest

from dto.user_dto import UserDTO
from pages.dashboard_page import DashBoardPage
from pages.receive_page import ReceivePage
from pages.reservation_tab_page import ReservationTabPage
from pages.side_chart_page import SideChartPage
from pages.side_page import SidePage
from pages.user_chart_page import UserChartPage
from pages.user_save_page import UserSavePage
from utils.app_manager import AppManger
from utils.close_popup_thread import ClosePopupThread


class NoticeContext:
    def __init__(self):
        self.create_content = "공지사항 테스트"
        self.update_content = "업데이트"
        self.create_time = None

class SideChartContext:
    create_tiem = None

class UserContext:
    def __init__(self):
        self.user = UserDTO(chart_no=None, name=None, mobile_no=None, jno=None)

class ThreadResultContext:
    def __init__(self):
        self.blocked = False

@pytest.fixture(scope="session")
def save_user_ctx():
    return UserContext()

@pytest.fixture(scope="session")
def notice_context():
    return NoticeContext()

@pytest.fixture(scope="session")
def side_chart_context():
    return SideChartContext()

@pytest.fixture(scope="session")
def thread_result():
    return ThreadResultContext()

@pytest.fixture(scope="session")
def app_manager():
    app = AppManger()
    app.check_admin()
    return app

@pytest.fixture(scope="session")
def dashboard_page(app_manager):
    return DashBoardPage(app_manager)

@pytest.fixture(scope="session")
def receive_page(app_manager):
    return ReceivePage(app_manager)

@pytest.fixture(scope="session")
def side_page(app_manager):
    return SidePage(app_manager)

@pytest.fixture(scope="session")
def user_save_page(app_manager):
    return UserSavePage(app_manager)

@pytest.fixture(scope="session")
def side_chart_page(app_manager,user_chart_page):
    return SideChartPage(app_manager,user_chart_page)

@pytest.fixture(scope="session")
def user_chart_page(app_manager):
    return UserChartPage(app_manager)

@pytest.fixture(scope="session")
def reservation_tab_page(app_manager, user_chart_page):
    return ReservationTabPage(app_manager, user_chart_page)

@pytest.fixture(scope="session")
def start_event():
    return threading.Event()

@pytest.fixture(scope="session")
def quit_event():
    return threading.Event()

@pytest.fixture(scope="session", autouse=True)
def popup_thread(start_event, quit_event):
    thread = ClosePopupThread(start_event, quit_event)
    thread.daemon = True
    thread.start()
    yield
    start_event.set()
    quit_event.set()
    thread.join()