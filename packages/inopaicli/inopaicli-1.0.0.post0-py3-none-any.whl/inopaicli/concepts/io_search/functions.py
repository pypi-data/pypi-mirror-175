import os
import json
import time
from inopaicli.concepts.io_search.api import do_search_req
from inopaicli.core.api import build_url

CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 5000))
ALL_SEARCH_HITS_LIMIT = 50000


def io_search_until_max_hits_limit(
    resp_data: dict,
    hits: list[any],
    total: int,
    query_params: dict,
    limit: int,
    start_time: float
):
    while total > len(hits):
        current_hits = resp_data['hits']['hits']

        if len(hits) + limit <= ALL_SEARCH_HITS_LIMIT:
            query_params['json_data']['offset'] = len(hits)
        elif not current_hits and total - len(hits) < 10:
            break
        else:
            last_item_array = current_hits[len(current_hits) - 1:len(current_hits)]

            if last_item_array:
                last_item = last_item_array.pop()
                last_item_id = last_item.get('_id')
                query_params['json_data']['search_after'] = [last_item_id]
                query_params['json_data']['offset'] = 0
        print(
            'There are more results in this query --> Do another request',
            total,
            len(hits),
            query_params['json_data']['offset'],
            f'Took {time.time() - start_time}s',
        )
        start_time = time.time()
        resp = do_search_req(**query_params)
        resp_data = resp.json()
        hits.extend(current_hits)


def get_app_view_io_search_params(
    url: str,
    session_id: str,
    group: list[str],
    app: int,
    field_query_extra: dict,
    query: str,
    source_override: list,
    embedded: list,
    search_once: bool,
    app_view: dict,
    modified: bool = False,
    sort: list = None,
    detailled_query: dict = None,
):
    app_view = app_view if app_view else {}
    final_app = app_view.get('app') if app_view.get('app') else app
    final_query = app_view.get('q') if app_view.get('q') else query
    final_sort = app_view.get('sort') if app_view.get('sort') else sort
    final_field_query = app_view.get('field_query') if app_view.get(
        'field_query'
    ) else field_query_extra
    final_detailled_query = app_view.get('detailled_query') if app_view.get(
        'detailled_query'
    ) else detailled_query

    return {
        'url': url,
        'session_id': session_id,
        'embedded': embedded,
        'search_once': search_once,
        'modified': modified,
        'group': group,
        'app': final_app,
        'field_query_extra': final_field_query,
        'detailled_query': final_detailled_query,
        'query': final_query,
        'sort': final_sort,
        'source_override': source_override,
    }


def io_search(
    url: str,
    session_id: str,
    group: int | list[int],
    app: int,
    query: str,
    modified: bool,
    field_query_extra={},
    sort=[{
        "_id": {
            "order": "desc"
        }
    }],
    source_override=None,
    embedded=[],
    search_once=False,
    detailled_query=None
):
    limit = CHUNK_SIZE
    final_field_query = field_query_extra

    if group:
        final_field_query['group'] = group
    if app:
        final_field_query['io_type'] = [app]
    if modified:
        final_field_query["modified"] = [int(modified)]

    json_data = {
        'q': query,
        'field_query': final_field_query,
        'detailled_query': detailled_query,
        'limit': limit,
        'sort': sort,
        'exclude_permissions': True,
        '_embedded': embedded,
    }

    if source_override:
        json_data['_source_override'] = source_override

    query_params = dict(
        url=build_url(url, '/api/search/'),
        headers={
            'Content-Type': 'application/json',
        },
        json_data=json_data,
        cookies={'sessionid': session_id},
    )

    print(json.dumps(query_params))
    print('Search query start')

    start_time = time.time()
    resp = do_search_req(**query_params)
    resp_data = resp.json()

    hits = resp_data['hits']['hits']
    total = resp_data['hits']['total']

    print(
        f"> Total count {total}. took {resp.elapsed.total_seconds()}s. jsondata: {json.dumps(json_data)}"
    )

    if not search_once:
        io_search_until_max_hits_limit(
            resp_data,
            hits,
            total,
            query_params,
            limit,
            start_time,
        )

    embedded = resp_data['_embedded'] if '_embedded' in resp_data else None
    apps = embedded['apps'] if embedded and 'apps' in embedded else []
    r_ios = embedded['related_ios'] if embedded and 'related_ios' in embedded else []

    return {
        'hits': hits,
        'total': total,
        'apps': apps,
        'related_ios': r_ios,
    }
