import pyautogui

from pages.chart_page import ChartPage
from pages.reservation_tab_page import ReservationTab
from pages.side_chart_page import SideChart
from utils.app_manager import AppManger


class TestChart:
    def __init__(self):
        self.app = AppManger()
        self.chart_page = ChartPage()
        self.side_chart = SideChart()
        self.reservation_tab = ReservationTab()
        self.create_time = None
        self.craete_memo_content = None
        
        self.test_compare_chart_user_info()
        self.test_side_memo_creat()
        self.test_change_side_chart()
        self.test_reservation_tab()
        
    
    def test_compare_chart_user_info(self):
        chart_no = self.app.chart_number_change_format("4650")
        assert self.chart_page.compare_user_info_get_data(chart_no), self.app.assert_alert("환자 정보를 확인해주세요")
    
    def test_side_memo_creat(self):
        """메모 저장"""
        self.craete_memo_content = "메모 테스트"
        link_element = self.side_chart.get_side_field_link("메모")
        link_element.set_focus()
        link_element.click_input()
        
        eidt_element = self.side_chart.get_side_memo_edit()
        eidt_element.set_focus()
        eidt_element.set_text(self.craete_memo_content)
        save_btn = self.side_chart.get_side_memo_button()
        save_btn.click()
        
        self.create_time = self.app.get_now_time()
        compare_result = self.side_chart.compare_side_memo(self.craete_memo_content,self.create_time)
        assert compare_result, self.app.assert_alert("작성된 메모가 존재하지 않습니다.") 
    
    def test_change_side_chart(self):
        self.side_chart.get_side_chart()
        assert self.side_chart.get_comfirm_popup(), self.app.assert_alert("사이드 차트를 진입할 수 없습니다.")
        
    def test_reservation_tab(self):
        test = self.reservation_tab.get_rsrv_timetable()
        test = self.reservation_tab.get_rsrv_list()
        test = self.reservation_tab.get_ticket_list()
        rsrv_edit_list = self.reservation_tab.get_rsrv_edits()
    
    def create_reservation(self):
        return