import pytest


# @pytest.mark.skip()
class TestReservationTab():
    @pytest.fixture(autouse=True)
    def setup(self, reservation_tab_page):
        self.reservation_tab_page = reservation_tab_page
    
    @pytest.mark.skip()
    def test_reservation_tab(self):
        test = self.reservation_tab_page.get_rsrv_timetable()
        for i in test.children():
            for el in i.children():
                print(el)
                
        test = self.reservation_tab_page.get_rsrv_list()
        for i in test.children():
            for el in i.children():
                print(el)
        
        
        test = self.reservation_tab_page.get_ticket_list()
        for i in test.children():
            for el in i.children():
                print(el)
        
    def test_new_reserve(self):
        self.reservation_tab_page.write_rsrv_memo("신규 예약, 예약메모 작성")
        self.reservation_tab_page.write_forward_memo("신규 예약, 예약메모 작성")
        
        test =  self.reservation_tab_page.get_rsrv_buttons()
        for el in test:
            print(el.element_info.automation_id)
            print(el.element_info.name)
        return
    
    def test_cancel_reserve(self):
        return
    
    def test_change_reserve(self):
        return