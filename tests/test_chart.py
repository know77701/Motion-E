from pages.chart_page import ChartPage
from utils.app_manager import AppManger


class TestChart:
    def __init__(self):
        self.app = AppManger()
        self.chart_page = ChartPage()
        self.compare_side_memo()
    
    def compare_chart_user_info(self):
        chart_no = self.app.chart_number_change_format("2351")
        if not self.chart_page.compare_user_info_get_data(chart_no):
            print("진입한 차트의 환자 정보를 확인해주세요")
    
    def side_memo_creat(self):
        self.chart_page.create_side_memo("테스트")
        return
    
    def compare_side_memo(self):
        memo_list = self.chart_page.get_side_memo_list()
        for items in memo_list:
            for item in items:
                print(item)