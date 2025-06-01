import pytest


# @pytest.mark.skip()
class TestReservationTab():
    @pytest.fixture(autouse=True)
    def setup(self, reservation_tab_page):
        self.reservation_tab_page = reservation_tab_page
    
    def test_new_reserve(self, start_event):
        if self.reservation_tab_page.get_change_rsrv_button():
            self.reservation_tab_page.get_new_rsrv_button().click()
        
        self.reservation_tab_page.rsrv_time_setting()
        self.reservation_tab_page.write_rsrv_memo("신규 예약, 예약메모 작성")
        self.reservation_tab_page.write_forward_memo("신규 예약, 전달메모 작성")
        start_event.set()
        self.reservation_tab_page.get_new_rsrv_button().click()
        
        assert self.reservation_tab_page.verify_rsrv_list(), "신규예약되지 않았습니다."
        
    
    def test_cancel_reserve(self):
        
        return
    
    def test_change_reserve(self):
        return