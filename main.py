import ctypes
import multiprocessing
import sys

from tests.test_chart import *
from tests.test_dashboard_page import *
from tests.test_login import *

if __name__ == "__main__":
    
    # login = TestLogin()
    # test_dash_board = TestDashBoardPage()
    test_chart = TestChart()
    
    

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
