from pages.chart_page import ChartPage


class TestChart:
    def __init__(self):
        self.chart_page = ChartPage()
        self.test()
    
    def test(self):
        if not self.chart_page.compare_user_info_get_data("0000"):
            print("진입한 차트의 환자 정보를 확인해주세요")
            return
        print("테스트")
        