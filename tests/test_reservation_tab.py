import pytest
import logging
from pages.reservation_tab_page import ReservationTabPage

# 로그 설정은 conftest.py에서 이미 되어 있으므로 여기서는 추가하지 않습니다.

def test_connect_to_tbeauty_chart_form(reservation_tab_page: ReservationTabPage):
    """
    tBeautyChartForm 윈도우에 연결되는지 테스트합니다.
    """
    logging.info("tBeautyChartForm 윈도우 연결 테스트 시작")
    tbeauty_chart_form_window = reservation_tab_page.connect_to_beauty_chart_form()
    assert tbeauty_chart_form_window is not None
    logging.info(f"tBeautyChartForm 윈도우 연결 성공: {tbeauty_chart_form_window.window_text()} (AutomationId: {tbeauty_chart_form_window.automation_id()})")


def test_find_rad_panel1_pane(reservation_tab_page: ReservationTabPage):
    """
    radPanel1 Pane을 찾는지 테스트합니다.
    """
    logging.info("radPanel1 Pane 찾기 테스트 시작")
    rad_panel1_pane = reservation_tab_page.find_rad_panel1_pane()
    assert rad_panel1_pane is not None
    logging.info(f"radPanel1 Pane 찾기 성공: {rad_panel1_pane.element_info.name} (AutomationId: {rad_panel1_pane.element_info.automation_id})")

# def test_find_panel30_pane(reservation_tab_page: ReservationTabPage):
#     """
#     panel30 Pane을 찾는지 테스트합니다.
#     """
#     logging.info("panel30 Pane 찾기 테스트 시작")
#     panel30_pane = reservation_tab_page.find_panel30_pane()
#     assert panel30_pane is not None
#     logging.info(f"panel30 Pane 찾기 성공: {panel30_pane.element_info.name} (AutomationId: {panel30_pane.element_info.automation_id})")

def test_find_rad_scrollable_panel3_pane(reservation_tab_page: ReservationTabPage):
    """
    radScrollablePanel3 Pane을 찾는지 테스트합니다.
    """
    logging.info("radScrollablePanel3 Pane 찾기 테스트 시작")
    rad_scrollable_panel3_pane = reservation_tab_page.find_rad_scrollable_panel3_pane()
    assert rad_scrollable_panel3_pane is not None
    logging.info(f"radScrollablePanel3 Pane 찾기 성공: {rad_scrollable_panel3_pane.element_info.name} (AutomationId: {rad_scrollable_panel3_pane.element_info.automation_id})")

def test_find_panel1_pane(reservation_tab_page: ReservationTabPage):
    """
    panel1 Pane을 찾는지 테스트합니다.
    """
    logging.info("panel1 Pane 찾기 테스트 시작")
    panel1_pane = reservation_tab_page.find_panel1_pane()
    assert panel1_pane is not None
    logging.info(f"panel1 Pane 찾기 성공: {panel1_pane.element_info.name} (AutomationId: {panel1_pane.element_info.automation_id})")

def test_find_checkboxes(reservation_tab_page: ReservationTabPage):
    """
    ControlType이 'CheckBox'인 요소들을 찾는지 테스트합니다.
    """
    logging.info("ControlType이 'CheckBox'인 요소들 찾기 테스트 시작")
    checkbox_elements = reservation_tab_page.find_checkboxes_by_control_type()
    assert len(checkbox_elements) > 0, "ControlType이 'CheckBox'인 요소가 하나도 발견되지 않았습니다."
    logging.info(f"ControlType이 'CheckBox'인 요소들 찾기 성공: {len(checkbox_elements)}개 발견")
    for i, element in enumerate(checkbox_elements):
        print(f"  [{i}] AutomationId: {element.element_info.automation_id}, Name: {element.element_info.name}, ControlType: {element.element_info.control_type}")

