from pages.base_entry_page import BaseEntryPage
from pages.dashboard_page import DashboardPage

class SingleEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "single", "Cancel")
        
    # override the toggle icon's image
    def create_widgets(self):
        super().create_widgets()
        self.toggle_entry_type_icon.configure(image=self.single_entry_icon)

    # ensure user is redirect to the dashboard after completing an singular entry
    def after_entry_submission(self):
        self.controller.show_page(DashboardPage)