from argparse import ArgumentParser
import os
from dotenv import load_dotenv

from inopaicli.core.file import get_env_file_path


def load_config():
    load_dotenv(get_env_file_path(), verbose=True)


def environ_or_required(key):
    if os.environ.get(key):
        return {"default": os.environ.get(key)}
    return {"required": True}


def parse_allowed_urls(argument_value: str) -> list[str]:
    if not argument_value:
        return []

    return [x.strip() for x in argument_value.split(',')]


def add_allowed_urls_argument(parser: ArgumentParser):
    parser.add_argument(
        "--allowedurls", default=os.environ.get("INOPAICLI_ALLOWED_URLS")
    )


def add_use_action_ids_argument(parser: ArgumentParser):
    parser.add_argument(
        "--useactionids",
        help="Use action ids instead of action identifiers",
        action="store_true",
    )


def add_initial_arguments(parser: ArgumentParser):
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-u", "--url", **environ_or_required("INOPAI_URL"))
    parser.add_argument("-e", "--email", **environ_or_required("INOPAI_EMAIL"))
    parser.add_argument("-p", "--password", default=os.environ.get("INOPAI_PASSWORD"))
