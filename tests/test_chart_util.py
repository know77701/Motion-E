

def test_compare_chart_user_info(app_manager, user_chart_page):
    chart_no = app_manager.chart_number_change_format("2351")
    assert user_chart_page.compare_user_info_get_data(chart_no), app_manager.assert_alert("환자 정보를 확인해주세요")
    