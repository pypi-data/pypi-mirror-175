# Development guide

#### This file is intended to contain all information and instructions a developer may need to work on this package

**If someone notices a mistake, or something misleading, please create a merge request with a better version of this guide, so it is improved for the next time**

## 1. Getting started

You will need to have `python>=3.8` and `virtualenv` command, you want to have a separate virtual environment for running your python command ```virtualenv -p /usr/bin/python3 venv```, and in case you are using a virtual environment you have to activate it ```source venv/bin/activate```, otherwise you can skip the last two commands, but anyway from here you need be able to see the output of ```pip -V``` in your project folder

This is the fastest way to make changes and test something

```pip install -e .```

```inopaicli -h```

To be able to use an api to get data you can pass the credentials as command arguments,

```inopaicli -e some@email.com -u http://some.url -p theactualpassword```

but even better you can use a `.env` file to store your credentials and reuse them easily, you can find `.env.example` file in the repo you can copy, rename and add your credentials to it

To test whether your credentials work you can run the following command

```inopaicli curl_print```

You are now able to manually change and test the actual code and connect to an api successfully

## 2. Understand the core package structure

```
src
--inopaicli
----core (Here are all the helper files that are reused in the project, like auth.py, file.py etc)
----concepts (Here is the concept related code that is not related to the package functionality itself)
------some_concept (This folder is named like the concept it will contain common code for)
--------functions.py (Here are all the functions related to this concept that are not api calls)
--------constants.py (Here are all the constants related to this concept)
--------api.py (This are all the api calls related to this concept)
----commands (Here you add a new command, or test a new plugin in, the filename represends the command)
------example_command.py (This is an example command that you can call with `inopaicli example_command`)
----tests (Here you can add subfolders as test data, to then be used in `inopaicli` subfolder)
------inopaicli (Here are the actual tests that can be run with `pytest`)
----manage.py (This is the main controller of the `inopaicli` script)
----pyproject.toml (This is the plugin configuration, we update the version here when we build it)
----.env.example (To easily rename to `.env` and add your info)
----README.md (Containing all commands and a changelog so we have to update it for each version)
--inopaicli.py (Shortcut for `src/inopaicli/py`)
```

## 3. Add new command that will be shared for all projects using `inopaicli`

To add a new command like `curl_print`, you need to create a new file in `src/inopaicli/commands`

If you want to name your command `new_test_command`, your new file will be called `new_test_command.py`

Each command file must have an `init` function, that will add the command settings both arguments
and each command file must have a `main` function, that will be executed if the command is called

Here is a template with the required functions and their parameters

```
from argparse import ArgumentParser


DESCRIPTION = "Add description for your command here"
EXAMPLES = [
    "inopaicli this_is_example_command --show-example",
]


def init(parser: ArgumentParser):
    return


def main(url: str, session_id: str, debug: bool, **kwargs):
    print(
        f"curl -H 'cookie: sessionid={session_id}' -H 'Content-Type: application/json' '{url}'"
    )
```

If the `init` functions specifies additional arguments, you can use the parameters with the same name as the arguments in the `main` function


```
from argparse import ArgumentParser


DESCRIPTION = "Add description for your command here"
EXAMPLES = [
    "inopaicli this_is_example_command --show-example",
    "inopaicli this_is_example_command --show-another-example"
]


def init(parser: ArgumentParser):
    parser.add_argument(
        "-t",
        "--test_argument",
        type=int,
        help="Add description for your argument here",
        required=True,
    )


def main(
    subparsers: _SubParsersAction,
    test_argument: int,
    **kwargs,
):
    print("This is the argument setup from the init function: ", test_argument)
    print("This is just to show you have the subparsers here too: ", subparsers)

```

If the command contains duplicate code or functionality in the package in its `main` function

## 4. Install the package and test the actual command locally

You can install the project local dependencies with [flit](https://flit.pypa.io/)

First you need to install `flit`

```pip install flit~=3.7.1```

Then you can install or reinstall the project with

```flit install --deps=develop```

And you can reinstall with pip as you already installed the dependencies

```pip install -e .```

After that you should be able to run the actual package command

```inopaicli -h```

## 5. Test and import external plugin commands

To develop a new plugin create a new command, after you developed and tested it, you add it to `inopaicli-plugins` folder, as a sibling folder of the virtual environment folder (venv), so if your `venv` folder is in your project folder, you must have the `inopaicli-plugins` and the `.env` file in the project folder too

## 6. Contribution process when making changes as a new merge request

1. Development (fix, update or create a new command)

- Update `README.md` commands if needed

2. Check if the package builds after you installed it with `flit`<br>
```flit install --deps=develop && inopaicli -h```

3. Use formatter to resolve fixable styling issues<br>
```yapf --in-place --recursive ./src ./tests```

4. Use linter to check for problems and resolve if any<br>
```pylint ./src ./tests```

5. If automated tests are required for the issue

Add test file(s) to `tests/inopaicli`, and if some mock/data file(s) are needed, subfolders could be added to the `tests` folder

Run tests with

```pytest```

6. If there is an update in a command description and/or help, or there is a new command, call this to update the COMMANDS.md file, so it is automatically documented<br>
```inopaicli commands_info --update```


7. Create a merge request, link an issue to it, add explanation if any and assign a reviewer

Branch name convention: lowercase with dash, ex: **`some-new-branch`**

Commit message convention: first uppercase only, ex: **`New commit message describing the commit`**

## 7. Publish new version of the package

1. Increase the version in `pyproject.toml` using [SemVer convention](https://semver.org/)
2. Update `README.md` changelog
3. Increase the version in `pyproject.toml` using [SemVer convention](https://semver.org/)

4. ```flit build```

- you should see a message similar to `Built wheel: dist/inopaicli-1.0.0-py3-none-any.whl` in the console

5. Install the build locally using pip to ensure the package is pip compatible or test command<br>
```pip install dist/inopaicli-1.0.0-py3-none-any.whl```

- If the build is installed properly you should be able to see the help command<br>
```inopaicli -h```

6. Publish the new built version to PyPI repository<br>
```flit publish```

You can refer to the [Flit Documentation](https://flit.pypa.io/en/latest/cmdline.html#flit-publish) if needed

