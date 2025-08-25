import pytest


@pytest.mark.skip()
class TestConsultTab():
    @pytest.fixture(autouse=True)
    def setup(self, consult_tab_page, side_chart_page):
        self.consult_tab_page = consult_tab_page
        self.side_chart_page = side_chart_page
    
    def test_consult_save(self, start_event):
        save_mopr_list = self.consult_tab_page.mopr_search()
        start_event.set()
        self.consult_tab_page.mopr_save()

        self.side_chart_page.verify_side_chart(save_mopr_list)
        