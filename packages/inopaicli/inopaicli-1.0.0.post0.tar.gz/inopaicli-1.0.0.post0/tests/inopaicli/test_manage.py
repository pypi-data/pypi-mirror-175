import os
from dotenv import load_dotenv
from inopaicli.manage import main


def test_main_call():
    load_dotenv(verbose=True)

    def simple_test_command(**_kwargs):
        return True

    main_result = main(
        'test_command', {'test_command': simple_test_command},
        os.environ.get("INOPAI_URL"),
        os.environ.get("INOPAI_EMAIL"),
        os.environ.get("INOPAI_PASSWORD"),
        True
    )

    assert main_result
