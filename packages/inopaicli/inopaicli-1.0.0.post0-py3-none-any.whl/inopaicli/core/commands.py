from argparse import _SubParsersAction, ArgumentParser, RawTextHelpFormatter
import glob
from importlib import import_module
from importlib.machinery import SourceFileLoader
from os.path import basename, dirname, isfile, join
from types import ModuleType
from typing import Callable

from inopaicli.core.file import get_current_working_directory
from inopaicli.core.constants import EXTERNAL_PLUGINS_FOLDER


def sort_commands(command_names: list[str]) -> list[str]:
    return sorted(command_names)


def get_commands_documentation(subparsers: _SubParsersAction) -> str:
    command_parsers_map: dict[str, ArgumentParser] = {}

    for name, subp in subparsers.choices.items():
        command_parsers_map[name] = subp

    sorted_command_names = sort_commands(command_parsers_map.keys())
    commands_documentation_text = "# Inopai CLI commands documentation\n\n"
    commands_documentation_text += "You can use the [commands_print](#commands_print_link) command to get the documentation in terminal\n\n"
    commands_documentation_text += "## Here is a list of all the commands\n\n"

    for name in sorted_command_names:
        commands_documentation_text += f"- [{name}](#{name}_link)\n"

    commands_documentation_text += "\n"

    for name in sorted_command_names:
        commands_documentation_text += f'## <a id="{name}_link"></a> {name}\n'
        commands_documentation_text += f'{command_parsers_map[name].format_help()}'

    return commands_documentation_text


def print_commands_documentation(subparsers: _SubParsersAction) -> None:
    print(get_commands_documentation(subparsers))


def update_commands_documentation(subparsers: _SubParsersAction) -> None:
    with open(get_commands_documentation_path(), "w") as file:
        file.write(get_commands_documentation(subparsers))


def add_subcommand_description(description: str, *examples: list[str]) -> str:
    examples_description = ""

    for example in examples:
        examples_description += f"`{example}`\n"

    return f"description:\n{description}\n\n\nexamples:\n{examples_description}"


def add_subcommand_parser(
    subparsers: _SubParsersAction,
    command_name: str,
    description: str,
    *examples: list[str]
) -> ArgumentParser:
    return subparsers.add_parser(
        name=command_name,
        description=add_subcommand_description(description, examples),
        formatter_class=RawTextHelpFormatter
    )


def validate_selected_command(
    subcommand: str,
    subcommand_functions: dict[str, Callable],
) -> None:
    if subcommand not in subcommand_functions:
        print(
            f'Unknown subcommand "{subcommand}". Please use one of {", ".join(subcommand_functions.keys())}.'
        )
        raise SystemExit(1)

    return subcommand_functions


def get_subcommand_functions_map(subparsers: _SubParsersAction) -> str | None:
    subcommand_functions = {}
    subcommand_modules_map = {}
    all_commands = get_all_command_names()

    for command in all_commands:
        command_module = import_module(f".{command}", "inopaicli.commands")

        subcommand_modules_map[command] = {
            "module": command_module,
            "is_plugin": False,
        }

    all_plugins = get_all_plugin_names()

    for plugin in all_plugins:
        plugin_path = f"{get_external_plugins_folder_path()}{plugin}.py"

        SourceFileLoader(f"inopaicli.plugins.{plugin}", plugin_path).load_module()

        plugin_module = import_module(f".{plugin}", "inopaicli.plugins")

        subcommand_modules_map[command] = {
            "module": plugin_module,
            "is_plugin": True,
        }

    sorted_command_names = sort_commands(subcommand_modules_map.keys())

    for module_name in sorted_command_names:
        module = subcommand_modules_map[module_name]["module"]
        is_plugin = subcommand_modules_map[module_name]["is_plugin"]
        module_subcommand = get_subcommand_from_module(module_name, module, is_plugin)
        subcommand_parser = add_subcommand_parser(
            subparsers,
            module_name,
            module_subcommand["description"],
            *module_subcommand["examples"]
        )
        module_subcommand["init_function"](subcommand_parser)
        subcommand_functions[module_name] = module_subcommand["main_function"]

    return subcommand_functions


def get_module_error(subcommand_name: str, problem: str, is_plugin: bool):
    plugin_prefix = f'Plugin "plugins/{subcommand_name}.py"'
    command_prefix = f'Command "commands/{subcommand_name}.py"'
    error_prefix = plugin_prefix if is_plugin else command_prefix

    print(f'{error_prefix} does not have a {problem}')
    raise SystemExit(1)


def get_subcommand_from_module(
    subcommand_name: str, module: ModuleType, is_plugin: bool
):
    try:
        description = getattr(module, "DESCRIPTION")

        if not description:
            raise
    except AttributeError:
        get_module_error(subcommand_name, "DESCRIPTION string constant", is_plugin)

    try:
        examples = getattr(module, "EXAMPLES")

        if not examples[0]:
            raise
    except AttributeError:
        get_module_error(subcommand_name, "EXAMPLES string array constant", is_plugin)

    try:
        init_function = getattr(module, "init")
    except AttributeError:
        get_module_error(subcommand_name, "init function", is_plugin)

    try:
        main_function = getattr(module, "main")
    except AttributeError:
        get_module_error(subcommand_name, "main function", is_plugin)

    return {
        "description": description,
        "examples": examples,
        "init_function": init_function,
        "main_function": main_function,
    }


def get_external_plugins_folder_path() -> str | None:
    path = f"{get_current_working_directory()}/{EXTERNAL_PLUGINS_FOLDER}/"

    return path


def get_commands_folder_path() -> str | None:
    path = f"{dirname(dirname(__file__))}/commands/"

    return path


def get_commands_documentation_path() -> str | None:
    path = f"{dirname(dirname(dirname(dirname(__file__))))}/COMMANDS.md"

    return path


def get_all_command_names() -> list[str]:
    command_files = glob.glob(join(get_commands_folder_path(), "*.py"))
    all_command_names = [
        basename(f)[:-3] for f in command_files
        if isfile(f) and not f.endswith("__init__.py")
    ]

    return all_command_names


def get_all_plugin_names() -> list[str]:
    plugin_files = glob.glob(f"{get_external_plugins_folder_path()}*.py")
    all_plugin_names = [
        basename(f)[:-3] for f in plugin_files
        if isfile(f) and not f.endswith("__init__.py")
    ]

    return all_plugin_names


def get_all_subcommand_names() -> list[str]:
    command_files = glob.glob(join(get_commands_folder_path(), "*.py"))
    all_subcommands = [
        basename(f)[:-3] for f in command_files
        if isfile(f) and not f.endswith("__init__.py")
    ]

    return all_subcommands
