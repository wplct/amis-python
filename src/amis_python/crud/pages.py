from .helpers import ensure_list


def build_crud_page(
    *,
    title,
    api,
    columns,
    filter_schema=None,
    header_toolbar=None,
    footer_toolbar=None,
    primary_field="object_id",
    crud_id="crud",
    page_id=None,
    **overrides,
):
    crud = {
        "id": crud_id,
        "type": "crud2",
        "mode": "table2",
        "dsType": "api",
        "syncLocation": True,
        "primaryField": primary_field,
        "loadType": "pagination",
        "api": api,
        "columns": ensure_list(columns),
        "headerToolbar": header_toolbar if header_toolbar is not None else [],
        "footerToolbar": footer_toolbar
        if footer_toolbar is not None
        else [
            {
                "type": "pagination",
                "layout": ["total", "perPage", "pager"],
                "perPage": 10,
                "perPageAvailable": [10, 20, 50, 100],
                "align": "right",
            }
        ],
    }
    if filter_schema is not None:
        crud["filter"] = filter_schema

    page = {
        "type": "page",
        "title": title,
        "body": [crud],
    }
    if page_id is not None:
        page["id"] = page_id
    page.update({k: v for k, v in overrides.items() if v is not None})
    return page
