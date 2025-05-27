
def test_side_memo_creat(side_chart_page, app_manager):
    craete_memo_content = "메모 테스트"
    link_element = side_chart_page.get_side_field_link("메모")
    link_element.set_focus()
    link_element.click_input()
    
    eidt_element = side_chart_page.get_side_memo_edit()
    eidt_element.set_focus()
    eidt_element.set_text(craete_memo_content)
    save_btn = side_chart_page.get_side_memo_button()
    save_btn.click()
    
    screate_time = app_manager.get_now_time()
    compare_result = side_chart_page.compare_side_memo(craete_memo_content, create_time)
    assert compare_result, app_manager.assert_alert("작성된 메모가 존재하지 않습니다.") 
    
def test_change_side_chart(side_chart_page, app_manager):
    side_chart_page.get_side_chart()
    assert side_chart_page.get_comfirm_popup(), app_manager.assert_alert("사이드 차트를 진입할 수 없습니다.")
