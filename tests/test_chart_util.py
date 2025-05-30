
import pytest


@pytest.mark.skip(reason="유틸 함수 추가 후 테스트 진행예정")
@pytest.mark.order(11)
def test_compare_chart_user_info(app_manager, user_chart_page,save_user_ctx):
    user = save_user_ctx.user
    chart_no = app_manager.chart_number_change_format(user.chart_no)
    
    assert user_chart_page.compare_user_info_get_data(chart_no), app_manager.assert_alert("환자 정보를 확인해주세요")
    