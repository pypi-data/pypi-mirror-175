import os
import time
from argparse import ArgumentParser
from inopaicli.concepts.io.functions import import_ios
from inopaicli.core.api import calculate_end
from inopaicli.core.file import read_json_file

DESCRIPTION = "Synchronize ios from id in json file"
EXAMPLES = [
    "inopaicli entries_sync -a 1 -g 1 -p fdjshk -f FILENAME",
]


def init(parser: ArgumentParser):
    parser.add_argument("-a", "--app", type=int, help="Application ID", required=True)
    parser.add_argument("-g", "--group", type=int, help="Group ID", required=True)
    parser.add_argument(
        "-p_name", "--property_name", type=str, help="Property name", required=True
    )
    parser.add_argument(
        "-f",
        "--filename",
        help="Filename for spare part input data json file",
    )
    parser.add_argument("-c", "--chunk_size", type=int, default=0, required=False)
    parser.add_argument("--prevent_io_create", action="store_true")
    parser.add_argument("--prevent_io_update", action="store_true")
    parser.add_argument(
        "--user_forces_skip_actions",
        help="User forces skip actions",
        nargs="+",
        required=False
    )


def main(
    url: str,
    session_id: str,
    app: int,
    group: int,
    property_name: str,
    filename: str,
    debug=False,
    chunk_size=0,
    prevent_io_create=False,
    prevent_io_update=False,
    user_forces_skip_actions=None,
):
    if not os.path.exists(filename):
        raise Exception(f'File does not exist {filename}')

    spare_parts = read_json_file(filename)

    if chunk_size != 0:
        chunk_count = (len(spare_parts) // chunk_size)
        rest = (len(spare_parts) % (chunk_count * chunk_size))
        start_time = time.time()
        print('Splitting input file in', chunk_count, 'chunks')

        for i in range(0, chunk_count):
            start = i * chunk_size
            end = calculate_end(
                chunk_count=chunk_count, chunk_size=chunk_size, rest=rest, i=i
            )
            print('start', start, 'end', end)
            respdata = import_ios(
                url=url,
                session_id=session_id,
                app=app,
                group=group,
                property_name=property_name,
                ios=spare_parts[start:(end + 1)],
                prevent_io_create=prevent_io_create,
                prevent_io_update=prevent_io_update,
                debug=debug,
                user_forces_skip_actions=user_forces_skip_actions,
            )
            updated = f"{respdata['updated']}"
            created = f"{respdata['created']}"
            unchanged = f"{respdata['unchanged']}"

            print(
                'Chunk',
                i,
                'took',
                time.time() - start_time,
                's',
                f"Stats: updated:{updated} created:{created} unchanged:{unchanged}",
            )
            start_time = time.time()
    else:
        respdata = import_ios(
            url=url,
            session_id=session_id,
            app=app,
            group=group,
            property_name=property_name,
            ios=spare_parts,
            prevent_io_create=prevent_io_create,
            prevent_io_update=prevent_io_update,
            debug=debug,
        )
