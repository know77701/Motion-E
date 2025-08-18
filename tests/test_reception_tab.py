import pytest


class TestReceptionTab:
    
    @pytest.fixture(autouse=True)
    def setup(self, reception_tab_page, side_chart_page):
        self.reception_tab_page = reception_tab_page
        self.side_chart_page = side_chart_page
    
    def test_save_reception(self,start_event):
        self.reception_tab_page.get_element_list()
        return