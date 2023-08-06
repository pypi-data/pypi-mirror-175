import os
from argparse import ArgumentParser
from inopaicli.concepts.app_export.api import export_update
from inopaicli.core.api import get_id_or_identifier
from inopaicli.core.config import add_allowed_urls_argument, add_use_action_ids_argument, parse_allowed_urls
from inopaicli.core.file import get_all_files, read_file, read_json_file

DESCRIPTION = "Update export in app based on a folder containing data (.json) and template files (.docx)"
EXAMPLES = [
    "inopaicli exports_update -a 1 -f './directory' --allowedurls http://localhost:9000",
    "inopaicli exports_update -a 1 -f './directory' --allowedurls http://localhost:9000 --useactionids",
]


def init(parser: ArgumentParser):
    parser.add_argument("-a", "--app", type=int, help="Application ID", required=False)
    parser.add_argument(
        "-f",
        "--folder",
        help="Specify the folder where are exported files",
        required=True,
    )
    add_use_action_ids_argument(parser)
    add_allowed_urls_argument(parser)


def main(
    url: str,
    session_id: str,
    app: int,
    folder: str,
    allowedurls: str,
    useactionids=False,
    **_kwargs,
):
    dir_path = os.path.realpath(folder)

    assert url in parse_allowed_urls(allowedurls)

    if not os.path.isdir(dir_path):
        raise ValueError("Not a directory", dir_path)

    for file_name in get_all_files(dir_path):
        if ".docx" in file_name:
            print("Ignoring template")
            continue

        path = os.path.realpath(os.path.join(dir_path, file_name))
        data = read_json_file(path, quiet=True)

        export_app = data.get("app")
        if app and app != export_app:
            continue

        template_docx_path = os.path.realpath(
            os.path.join(
                dir_path,
                f"app__{export_app}__export__{get_id_or_identifier(data, useactionids)}__TEMPLATE.docx"
            )
        )
        template_file = read_file(template_docx_path, quiet=True)

        export_update(
            url=url,
            session_id=session_id,
            data=data,
            template_file=template_file,
        )
