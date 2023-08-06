def get_app_from_list(app_id: int, apps: list) -> list[str]:
    matches = list(filter(lambda app: app.get('id') == app_id, apps))

    return matches[0]
