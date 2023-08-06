from inopaicli.core.api import simple_request


def io_import_json(base_url: str, session_id: str, json_data: any):
    resp = simple_request(
        base_url=base_url,
        url="api/io/import_json/",
        session_id=session_id,
        json=json_data,
        method="post",
    )

    return resp.json()
