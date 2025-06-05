

import pytest


class TestSideChart():
    @pytest.fixture(autouse=True)
    def setup(self,app_manager, side_chart_page):
        self.app_manager = app_manager
        self.side_chart_page = side_chart_page

def test_side_memo_creat(self):
    craete_memo_content = "메모 테스트"
    link_element = self.side_chart_page.get_side_field_link("메모")
    link_element.set_focus()
    link_element.click_input()
    
    eidt_element = self.side_chart_page.get_side_memo_edit()
    eidt_element.set_focus()
    eidt_element.set_text(craete_memo_content)
    save_btn = self.side_chart_page.get_side_memo_button()
    save_btn.click()
    
    create_time = self.app_manager.get_now_time()
    compare_result = self.side_chart_page.compare_side_memo(craete_memo_content, create_time)
    assert compare_result, self.app_manager.assert_alert("작성된 메모가 존재하지 않습니다.") 
    
def test_change_side_chart(self):
    self.side_chart_page.side_chart_change()
    assert (self.side_chart_page.get_comfirm_popup(), 
        self.app_manager.assert_alert("사이드 차트를 진입할 수 없습니다."))

