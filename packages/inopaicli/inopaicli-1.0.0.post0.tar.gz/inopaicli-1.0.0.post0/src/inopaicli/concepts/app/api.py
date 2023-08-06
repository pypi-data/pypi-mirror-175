from inopaicli.core.api import simple_get


def get_app(baseurl: str, app_id: int, session_id: str) -> dict[str, dict]:

    return simple_get(baseurl=baseurl, url=f"/api/app/{app_id}/", session_id=session_id)
