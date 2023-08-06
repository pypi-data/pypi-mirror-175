from argparse import ArgumentParser

DESCRIPTION = "Prints curl command with your session id and url"
EXAMPLES = [
    "inopaicli curl_print",
]


def init(_parser: ArgumentParser):
    return


def main(url: str, session_id: str, **_kwargs):
    print(
        f"curl -H 'cookie: sessionid={session_id}' -H 'Content-Type: application/json' '{url}'"
    )
