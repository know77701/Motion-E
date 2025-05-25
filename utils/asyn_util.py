from concurrent.futures import ThreadPoolExecutor

from utils.element_finder import ElementFinder


class AsyncUtil():
    def find_fields_async(self, pane_field, field_ids):
        children = pane_field.children()
        with ThreadPoolExecutor() as executor:
            return list(executor.map(
                lambda fid: ElementFinder.find_edit_by_automation_id(children, fid),
                field_ids
            ))