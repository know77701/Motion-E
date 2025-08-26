from pages.base_page import BasePage
from pages.user_chart_page import UserChartPage
from utils.element_finder import ElementFinder
from locators.util_locators import UtilLocators
from pywinauto import Desktop
import logging
from pywinauto.controls import uia_controls


class ReservationTabPage(BasePage):
    def __init__(self, user_chart_page: UserChartPage):
        super().__init__(user_chart_page.app, user_chart_page.app_manager)
        self.user_chart_page = user_chart_page

    def some_reservation_method(self):
        # Placeholder for future implementation
        pass

    def connect_to_beauty_chart_form(self):
        return self.app_manager.connect_to_tbeauty_chart_form()

    def select_reservation_tab(self):
        # 최상위 애플리케이션 윈도우를 가져옵니다.
        main_window_title = self.app_manager.version_search(UtilLocators.MOTION_VERSION_TITLE)
        main_window = Desktop(backend="uia").window(title=main_window_title)
        logging.info(f"메인 윈도우: {main_window.window_text()} (AutomationId: {main_window.automation_id()})")

        # tBeautyChartForm에 먼저 연결합니다.
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
        logging.info(f"tBeautyChartForm 윈도우: {tbeauty_chart_form_window.window_text()} (AutomationId: {tbeauty_chart_form_window.automation_id()})")

        # 디버깅을 위해 tBeautyChartForm 윈도우의 모든 하위 컨트롤의 속성을 출력합니다.
        # logging.info("tBeautyChartForm 윈도우의 하위 컨트롤:")
        # for i, child in enumerate(ElementFinder.recursive_children(tbeauty_chart_form_window, depth=0, max_depth=5)):
        #     logging.info(f"  [{i}] Name: {child.element_info.name}, ControlType: {child.element_info.control_type}, AutomationId: {child.element_info.automation_id}")

        # "예약" 탭 아이템을 automation_id, name, control_type으로 정확하게 찾아 클릭
        reservation_tab_item = ElementFinder.find_child_by_attributes(
            tbeauty_chart_form_window,
            automation_id="tabModules", # 원래의 automation_id로 복구
            name=" 예약", # 이름 앞에 공백 포함하여 검색
            control_type="Tab" # ControlType을 Tab으로 복구
        )

        if reservation_tab_item:
            logging.info(f"'예약' 탭 아이템 찾음: (Name: {reservation_tab_item.element_info.name}, ControlType: {reservation_tab_item.element_info.control_type}, AutomationId: {reservation_tab_item.element_info.automation_id})")
            # ElementFinder.click(reservation_tab_item) # 일반 클릭 대신 TabControlWrapper에 적합한 click_input 사용
            reservation_tab_item.click_input() # TabControlWrapper는 click_input()으로 탭 선택
            logging.info("예약 탭 아이템을 선택했습니다.")
        else:
            logging.error("'예약' 탭 아이템을 찾을 수 없습니다.")
            raise Exception("'예약' 탭 아이템을 찾을 수 없습니다.")

    def find_rad_panel_main_panel_children(self):
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")

        rad_panel_main_panel = ElementFinder.find_child_by_attributes(
            tbeauty_chart_form_window,
            automation_id="radPanelMainPanel",
            control_type="Pane"
        )

        if rad_panel_main_panel:
            logging.info(f"'radPanelMainPanel' Pane 찾음: (Name: {rad_panel_main_panel.element_info.name}, ControlType: {rad_panel_main_panel.element_info.control_type}, AutomationId: {rad_panel_main_panel.element_info.automation_id})")
            logging.info("'radPanelMainPanel'의 하위 컨트롤:")
            children = []
            for i, child in enumerate(ElementFinder.recursive_children(rad_panel_main_panel, depth=0, max_depth=5)):
                children.append(child)
                logging.info(f"  [{i}] Name: {child.element_info.name}, ControlType: {child.element_info.control_type}, AutomationId: {child.element_info.automation_id}")
            return children
        else:
            logging.error("'radPanelMainPanel' Pane을 찾을 수 없습니다.")
            raise Exception("'radPanelMainPanel' Pane을 찾을 수 없습니다.")

    def find_rad_panel1_pane(self):
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")

        rad_panel1 = ElementFinder.find_child_by_attributes(
            tbeauty_chart_form_window,
            automation_id="radPanel1",
            control_type="Pane"
        )

        if rad_panel1:
            logging.info(f"'radPanel1' Pane 찾음: (Name: {rad_panel1.element_info.name}, ControlType: {rad_panel1.element_info.control_type}, AutomationId: {rad_panel1.element_info.automation_id})")
            return rad_panel1
        else:
            logging.error("'radPanel1' Pane을 찾을 수 없습니다.")
            raise Exception("'radPanel1' Pane을 찾을 수 없습니다.")

    def find_panel30_pane(self):
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")

        panel30 = ElementFinder.find_child_by_attributes(
            tbeauty_chart_form_window,
            automation_id="panel30",
            control_type="Pane"
        )

        if panel30:
            logging.info(f"'panel30' Pane 찾음: (Name: {panel30.element_info.name}, ControlType: {panel30.element_info.control_type}, AutomationId: {panel30.element_info.automation_id})")
            return panel30
        else:
            logging.error("'panel30' Pane을 찾을 수 없습니다.")
            raise Exception("'panel30' Pane을 찾을 수 없습니다.")

    def find_rad_scrollable_panel3_pane(self):
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")

        rad_scrollable_panel3 = ElementFinder.find_child_by_attributes(
            tbeauty_chart_form_window,
            automation_id="radScrollablePanel3",
            control_type="Pane" # ControlType은 'Pane'으로 가정합니다.
        )

        if rad_scrollable_panel3:
            logging.info(f"'radScrollablePanel3' Pane 찾음: (Name: {rad_scrollable_panel3.element_info.name}, ControlType: {rad_scrollable_panel3.element_info.control_type}, AutomationId: {rad_scrollable_panel3.element_info.automation_id})")
            return rad_scrollable_panel3
        else:
            logging.error("'radScrollablePanel3' Pane을 찾을 수 없습니다.")
            raise Exception("'radScrollablePanel3' Pane을 찾을 수 없습니다.")

    def find_panel1_pane(self):
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")

        panel1 = ElementFinder.find_child_by_attributes(
            tbeauty_chart_form_window,
            automation_id="panel1",
            control_type="Pane"
        )

        if panel1:
            logging.info(f"'panel1' Pane 찾음: (Name: {panel1.element_info.name}, ControlType: {panel1.element_info.control_type}, AutomationId: {panel1.element_info.automation_id})")
            return panel1
        else:
            logging.error("'panel1' Pane을 찾을 수 없습니다.")
            raise Exception("'panel1' Pane을 찾을 수 없습니다.")

    def find_panel1_children_automation_ids(self):
        panel1_pane = self.find_panel1_pane()
        if panel1_pane is None:
            logging.error("'panel1' Pane을 찾을 수 없습니다.")
            raise Exception("'panel1' Pane을 찾을 수 없습니다.")

        logging.info("'panel1' Pane의 하위 AutomationId 탐색 시작")
        children_automation_ids = []
        for i, child in enumerate(ElementFinder.recursive_children(panel1_pane, depth=0, max_depth=5)):
            if child.element_info.automation_id:
                children_automation_ids.append(child.element_info.automation_id)
                logging.info(f"  [{i}] 하위 요소 AutomationId: {child.element_info.automation_id}")
        return children_automation_ids

    def get_panel1_children_details(self):
        panel1_pane = self.find_panel1_pane()
        if panel1_pane is None:
            logging.error("'panel1' Pane을 찾을 수 없습니다.")
            raise Exception("'panel1' Pane을 찾을 수 없습니다.")

        logging.info("'panel1' Pane의 하위 요소 상세 정보 탐색 시작")
        children_details = []
        for i, child in enumerate(ElementFinder.recursive_children(panel1_pane, depth=0, max_depth=5)):
            detail = {
                "automation_id": child.element_info.automation_id,
                "name": child.element_info.name,
                "control_type": child.element_info.control_type
            }
            children_details.append(detail)
            logging.info(f"  [{i}] AutomationId: {child.element_info.automation_id}, Name: {child.element_info.name}, ControlType: {child.element_info.control_type}")
        return children_details

    def find_checkboxes_by_control_type(self):
        tbeauty_chart_form_window = self.connect_to_beauty_chart_form()
        if tbeauty_chart_form_window is None:
            logging.error("tBeautyChartForm 윈도우를 찾을 수 없습니다.")
            raise Exception("tBeautyChartForm 윈도우를 찾을 수 없습니다.")

        logging.info("ControlType이 'CheckBox'인 요소 탐색 시작")
        all_children = ElementFinder.recursive_children(tbeauty_chart_form_window, depth=0, max_depth=5)
        
        checkbox_elements = [
            child for child in all_children
            if child.element_info.control_type == "CheckBox"
        ]

        if checkbox_elements:
            logging.info(f"ControlType이 'CheckBox'인 요소 {len(checkbox_elements)}개 발견:")
            for i, element in enumerate(checkbox_elements):
                logging.info(f"  [{i}] AutomationId: {element.element_info.automation_id}, Name: {element.element_info.name}, ControlType: {element.element_info.control_type}")
            return checkbox_elements
        else:
            logging.error("ControlType이 'CheckBox'인 요소를 찾을 수 없습니다.")
            return []

