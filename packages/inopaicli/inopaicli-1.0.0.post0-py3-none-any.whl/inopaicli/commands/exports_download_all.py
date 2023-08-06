import os
from argparse import ArgumentParser
from inopaicli.concepts.app_export.api import export_template_download, get_exports
from inopaicli.core.api import get_id_or_identifier
from inopaicli.core.config import add_use_action_ids_argument
from inopaicli.core.file import write_json

DESCRIPTION = "Downloads export in app based on a folder containing data"
EXAMPLES = [
    "inopaicli exports_download_all -a 1 -o './directory'",
    "inopaicli exports_download_all -a 1 -o './directory' --useactionids",
]


def init(parser: ArgumentParser):
    parser.add_argument(
        "-a",
        "--app",
        type=int,
        help="Application ID",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--outputdirectory",
        help="Specify the directory where to generate the json file with exported files",
        default="exports",
    )
    add_use_action_ids_argument(parser)


def main(
    url: str,
    session_id: str,
    app: int,
    outputdirectory: str,
    debug=False,
    useactionids=False,
    **_kwargs,
):
    dir_path = os.path.realpath(outputdirectory)

    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise ValueError("Not a directory", dir_path)
        os.mkdir(dir_path)

    for export in get_exports(
        url=url,
        session_id=session_id,
        app=app,
        debug=debug,
    ):
        export.pop("_gnas")
        local_filename = file_name = os.path.join(
            dir_path,
            f"app__{export['app']}__export__{get_id_or_identifier(export, useactionids)}__TEMPLATE.docx"
        )

        export_template_download(
            url=url,
            session_id=session_id,
            export_id=export["id"],
            local_filename=local_filename,
        )

        if "exportgna_count" not in export or export.get("exportgna_count", None) == 0:
            print("Ignoring unused export")
            continue

        print("exportgna_count ", export["exportgna_count"])

        file_name = os.path.join(
            dir_path,
            f"app__{export['app']}__export__{export['id']}__data__{export['semantic_identifier']}__{export['text']}.json",
        )

        print("export", export.get("id", None), "-->", file_name)
        write_json(data=export, filename=file_name)
