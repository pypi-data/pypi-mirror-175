import os


def get_export_filename(
    group: int | list[int],
    app: int,
    suffix: str,
    filename: str | None = None,
    force: bool = False
) -> str:
    group = [group] if isinstance(group, int) else group

    if not filename:
        today = '20181213'
        filename = f'out-g-{"-".join([str(g) for g in group])}-a-{app}-{today}.{suffix}'

    if filename and os.path.exists(filename) and not force:
        raise Exception(f'File exists {filename}')

    print(f'Output filename is {filename}')

    return filename
