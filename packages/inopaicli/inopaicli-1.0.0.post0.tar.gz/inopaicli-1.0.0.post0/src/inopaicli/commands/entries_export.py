import json
from argparse import ArgumentParser
from inopaicli.concepts.io_search.functions import io_search
from inopaicli.core.export import get_export_filename
from inopaicli.core.file import write_json

DESCRIPTION = "Export group ios entries in json format"
EXAMPLES = [
    "inopaicli entries_export -g 1 -a 1 -f '/filedir/filename.json'",
]


def init(parser: ArgumentParser):
    parser.add_argument('-a', '--app', type=int, help='Application ID')
    parser.add_argument('-g', '--group', type=int, help='Group ID')
    parser.add_argument(
        '-f',
        '--filename',
        help='Filename for destination json file (print if no filename given)'
    )
    parser.add_argument('--force', action='store_true', default=False)
    parser.add_argument('--query', default=False)
    parser.add_argument('--sourceoverride', default=False)


def main(
    url: str,
    session_id: str,
    group: int,
    app: int,
    filename: str,
    query=None,
    force=False,
    sourceoverride=None,
    **_kwargs,
):
    filename = get_export_filename(group, app, 'json', filename, force)
    source_override = json.loads(sourceoverride) if sourceoverride else None

    search_response = io_search(
        url=url,
        session_id=session_id,
        group=group,
        app=app,
        query=query,
        field_query_extra={},
        source_override=source_override,
    )

    write_json(data=search_response['hits'], filename=filename)
