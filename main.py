import ctypes
import multiprocessing
import sys

from func.dashboard.dashboard import *
from func.process_func.process_func import *
from func.publicFunc.public_func import *
from func.start.motion_starter import *
from pages.login_page import *
from pages.login_page import LoginPage
from tests.test_login import *
from utils.app_manager import AppManger

if __name__ == "__main__":
    
    # AppManger 인스턴스 생성 후 실행
    app_manager = AppManger()
    app_manager.check_admin()
    window = app_manager.app_connect(retries=0)
    login = LoginPage(window)
    login.login_info()
    # login.setting_yakiho()
    # login.login_click()
    
    

    # start_sub_process_event = multiprocessing.Event()
    # sub_process_done_event = multiprocessing.Event()
    
    # process_func = ProcessFunc()
    

    # main_process = multiprocessing.Process(
    #     target=process_func.main_process_func, args=(start_sub_process_event, sub_process_done_event))
    # sub_process = multiprocessing.Process(
    #     target=process_func.sub_process_func, args=(start_sub_process_event, sub_process_done_event))
    # # chart_sub_process = multiprocessing.Process(
    # #     target=process_func.chart_sub_process, args=(start_sub_process_event,sub_process_done_event))
    
    
    # main_process.start()
    # sub_process.start()
    
    # # chart_sub_process.start()

    # main_process.join()
    # sub_process.terminate()
    # # chart_sub_process.terminate()
