from unittest import TestCase

from amis_python.crud import build_crud_page, build_filter_form


class CrudPagesTestCase(TestCase):
    def test_build_crud_page_returns_plain_schema(self):
        page = build_crud_page(
            title="类目管理",
            api={"url": "/api/mission-category/", "method": "get"},
            columns=[{"type": "tpl", "name": "name", "title": "名称"}],
            filter_schema=build_filter_form([
                {"type": "input-text", "name": "search", "label": "搜索"}
            ]),
            crud_id="mission-category-crud",
        )

        self.assertEqual(page["type"], "page")
        self.assertEqual(page["title"], "类目管理")
        self.assertEqual(page["body"][0]["type"], "crud2")
        self.assertEqual(page["body"][0]["id"], "mission-category-crud")
        self.assertEqual(page["body"][0]["columns"][0]["name"], "name")
        self.assertEqual(page["body"][0]["filter"]["type"], "form")
