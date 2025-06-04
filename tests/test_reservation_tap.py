import pytest


# @pytest.mark.skip()
class TestReservationTab():
    @pytest.fixture(autouse=True)
    def setup(self, reservation_tab_page):
        self.reservation_tab_page = reservation_tab_page
    
    @pytest.mark.skip()
    def test_new_reserve(self, start_event):
        """
            신규 예약 화면여부 확인 후 > 아닐경우 신규예약 버튼 클릭 > 신규화면진입 >
            예약 시간 설정 > 예약/전달 메모 작성 > 팝업 감지 이벤트 시작 >
            신규 예약 버튼 클릭 > 예약 리스트 확인하여 예약되었는지 확인
        """
        self.reservation_tab_page.prepare_new_reservation("신규 예약 메모", "신규 전달 메모")
        start_event.set()
        self.reservation_tab_page.get_new_rsrv_button().click()
        assert self.reservation_tab_page.verify_rsrv_list(), "신규예약되지 않았습니다."
        
    @pytest.mark.skip()
    def test_cancel_reserve(self):
        """
            취소팝업 확인필요
        """
        if not self.reservation_tab_page.get_cancle_rsrv_button():
            table = self.reservation_tab_page.get_rsrv_list_elements(
                rsrv_day="20250602",
                rsrv_time="1930"
            )
            table.click_input()
            
            assert self.reservation_tab_page.get_rsrv_day_edit, "예약 날짜 확인"
            assert self.reservation_tab_page.get_rsrv_time_edit, "예약 시간 확인"
            self.reservation_tab_page.get_rsrv_buttons()
            
            
        cancle_btn = self.reservation_tab_page.get_cancle_rsrv_button()

        cancle_btn.click()
        self.reservation_tab_page.get_rsrv_cancle_popup()
        
        
    def test_change_reserve(self, start_event):
        self.reservation_tab_page.select_reservation_by_datetime("20250602", "1700")
        self.reservation_tab_page.change_reservation_time()
        self.reservation_tab_page.submit_reservation_change(start_event)
        self.reservation_tab_page.verify_reservation_changed()