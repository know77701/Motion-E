from pages.base_page import BasePage
from pages.user_chart_page import UserChartPage


class ConsultTabPage(BasePage):
    def __init__(self, user_chart_page: UserChartPage):
        super().__init__(user_chart_page.app, user_chart_page.app_manager)
        self.user_chart_page = user_chart_page

    def some_consult_method(self):
        # Placeholder for future implementation
        pass

