import pytest


# @pytest.mark.skip()
class TestConsentTab():
    @pytest.fixture(autouse=True)
    def setup(self, consent_tab_page):
        self.consent_tab_page = consent_tab_page
    
    def test_consent_save(self, start_event):
        self.consent_tab_page.write_mopr_edit()
    