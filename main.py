from multiprocessing import Event, Process

from utils.sub_process import *
from utils.test_process import test_runner

if __name__ == "__main__":
    
    start_event = Event()
    
    test_process = Process(target=test_runner, args=(start_event,))
    sub_process = Process(target=close_popup_handler, args=(start_event,))
    
    test_process.start()
    sub_process.start()
    
    test_process.join()
    sub_process.join()
    
