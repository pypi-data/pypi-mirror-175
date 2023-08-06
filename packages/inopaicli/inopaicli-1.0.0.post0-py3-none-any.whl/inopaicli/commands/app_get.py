import json
from argparse import ArgumentParser
from inopaicli.concepts.app.api import get_app

DESCRIPTION = "Download application from id and print it"
EXAMPLES = [
    "inopaicli app_get -a 1",
]


def init(parser: ArgumentParser):
    parser.add_argument(
        "-a",
        "--app",
        type=int,
        help="Application ID",
        required=True,
    )


def main(
    url: str,
    session_id: str,
    app: int,
    **_kwargs,
):
    data = get_app(url, app, session_id)
    print(json.dumps(data, indent=2))
    return data
