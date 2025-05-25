import pytest
from utils.app_manager import AppManger
from utils.close_popup_thread import ClosePopupThread
import threading 

from pages.dashboard_page import DashBoardPage
from pages.receive_page import ReceivePage
from pages.side_page import SidePage
from pages.user_save_page import UserSavePage
from dto.user_dto import UserDTO


@pytest.fixture(scope="session")
def app_manager():
    app = AppManger()
    app.check_admin()
    return app

@pytest.fixture(scope="session")
def dashboard(app_manager):
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
def start_event():
    return threading.Event()

@pytest.fixture(scope="session")
def quit_event():
    return threading.Event()

@pytest.fixture(scope="session")
def save_user():
    return UserDTO(chart_no=None, name="QA테스트", mobile_no= "010-7441-7631",jno="941111-1111111")

@pytest.fixture(scope="session", autouse=True)
def popup_thread(start_event, quit_event):
    thread = ClosePopupThread(start_event, quit_event)
    thread.daemon = True
    thread.start()
    yield
    quit_event.set()
    thread.join()