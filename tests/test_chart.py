from pages.chart_page import ChartPage
from utils.app_manager import AppManger
from utils.element_finder import ElementFinder


class TestChart:
    def __init__(self):
        self.app = AppManger()
        self.chart_page = ChartPage()
        self.create_time = None
        self.craete_memo_content = None
        self.side_chart_info_compare()
        # self.side_memo_creat()
        
    
    def compare_chart_user_info(self):
        chart_no = self.app.chart_number_change_format("4591")
        if not self.chart_page.compare_user_info_get_data(chart_no):
            print("진입한 차트의 환자 정보를 확인해주세요")
    
    def side_memo_creat(self):
        """메모 저장"""
        self.craete_memo_content = "메모 테스트"
        link_element = self.chart_page.get_side_field_link("메모")
        link_element.set_focus()
        link_element.click_input()
        
        eidt_element = self.chart_page.get_side_memo_edit()
        eidt_element.set_focus()
        eidt_element.set_text(self.craete_memo_content)
        save_btn = self.chart_page.get_side_memo_button()
        save_btn.click()
        
        self.create_time = self.app.get_now_time()
        compare_result = self.chart_page.compare_side_memo(self.craete_memo_content,self.create_time)
        if not compare_result:
            print("작성된 메모가 존재하지 않습니다.")
    
    def side_chart_info_compare(self):
        compare_result = self.chart_page.get_side_chart()
        return