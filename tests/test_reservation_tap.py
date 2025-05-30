import pytest


# @pytest.mark.skip()
class TestReservationTab():
    @pytest.fixture(autouse=True)
    def setup(self, reservation_tab_page):
        self.reservation_tab_page = reservation_tab_page
    
    def test_reservation_tab(self):
        test = self.reservation_tab_page.get_rsrv_timetable()
        for i in test.children():
            print(i.element_info.name)
            print(i.element_info.control_type)
            print(i.element_info.automation_id)
            print(i.children())
        test = self.reservation_tab_page.get_rsrv_list()
        for i in test.children():
            print(i.element_info.name)
            print(i.element_info.control_type)
            print(i.element_info.automation_id)
            print(i.children())
        test = self.reservation_tab_page.get_ticket_list()
        for i in test.children():
            print(i.element_info.name)
            print(i.element_info.control_type)
            print(i.element_info.automation_id)
            print(i.children())
        rsrv_edit_list = self.reservation_tab_page.get_rsrv_edits()
        print(rsrv_edit_list)