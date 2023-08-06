import os
from argparse import ArgumentParser
from inopaicli.concepts.app_action.api import get_actions
from inopaicli.core.api import get_id_or_identifier
from inopaicli.core.config import add_use_action_ids_argument
from inopaicli.core.file import write_json

DESCRIPTION = "Download actions from application ID and generate json file to an output location"
EXAMPLES = [
    "inopaicli actions_download_all -a 1 -o './actions'",
    "inopaicli actions_download_all -a 1 -o './actions' -c",
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
        help="Folder with action files",
        default="actions",
    )
    parser.add_argument(
        "-t",
        "--includeunused",
        help="Include unused actions",
        action="store_true",
    )
    add_use_action_ids_argument(parser)


def main(
    url: str,
    session_id: str,
    app: int,
    outputdirectory: str,
    includeunused=False,
    useactionids=False,
    debug=False,
    **_kwargs
):
    dir_path = os.path.realpath(outputdirectory)

    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise ValueError("Not a directory", dir_path)
        os.mkdir(dir_path)

    all_actions = get_actions(
        url=url,
        session_id=session_id,
        app=app,
        debug=debug,
    )

    for action in all_actions:
        semantic_identifier = action.get("semantic_identifier", None)
        final_action_id = f"{action['id']}__{semantic_identifier}" if semantic_identifier else get_id_or_identifier(
            action, useactionids
        )
        action_file = os.path.join(
            dir_path, f"app__{action['application']}__action__{final_action_id}.json"
        )

        print("action", action.get("id", None), "-->", action_file)

        activation_info = action.pop("activation_info", None)
        activation_info_count = len(activation_info)

        if activation_info_count == 0 and not includeunused:
            continue

        if activation_info_count:
            action["ACTIVATIONCOUNT"] = activation_info_count

        action.pop("actionlog_errors", None)
        action.pop("actionlog_stats", None)
        action.pop("actionlog_count", None)
        action.pop("actiongna_count", None)

        write_json(data=action, filename=action_file)
