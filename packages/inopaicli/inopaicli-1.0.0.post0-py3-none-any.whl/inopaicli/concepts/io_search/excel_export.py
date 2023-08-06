from inopaicli.concepts.app.functions import get_app_from_list
from inopaicli.concepts.io.constants import IO_MAIN_ATTRIBUTES
from inopaicli.core.file import write_excel
from inopaicli.core.util import flatten_dict


def get_columns_from_search_response(
    app_id: int,
    search_response: dict,
    columns: str,
    with_relations: bool,
    app_view_properties: list[str]
) -> dict:
    column_map = get_column_value_map(app_id, search_response, with_relations)
    ordered_columns = get_final_ordered_columns(
        column_map, columns, app_view_properties
    )

    return ordered_columns


def get_io_attribute_headers(relation_header_text='') -> list[str]:
    attribute_headers = [
        get_io_attribute_header('id', relation_header_text),
        get_io_attribute_header('title', relation_header_text),
    ]

    return attribute_headers


def get_io_attribute_header(attribute_name: str, relation_header_text='') -> list[str]:
    attribute_header = IO_MAIN_ATTRIBUTES.get(attribute_name)

    if relation_header_text:
        attribute_header = f"{relation_header_text} {attribute_header}"
    return attribute_header


def get_io_property_columns(app_id: int, apps: list) -> dict[str, str]:
    main_app = get_app_from_list(app_id, apps)
    main_app_schema = main_app.get('schema')
    main_app_schema_properties = main_app_schema.get('properties')
    columns = {}

    for propname, value in main_app_schema_properties.items():
        columns[propname] = {
            "is_relation": value.get('format') == 'relation',
            "relation_app_id": value.get('ranges', [None])[0],
            "header_text": value.get('verbose_name'),
        }

    return columns


def get_io_headers(
    column_map: dict[str, str],
    ordered_columns: list[str],
) -> list[str]:
    headers = []

    for column_key in ordered_columns:
        column = column_map.get(column_key)
        headers.append(column)

    return headers


def get_io_rows(
    search_response: dict,
    ordered_columns: list[str],
) -> list:
    hits = search_response['hits'] if 'hits' in search_response.keys() else []
    rows_data = []

    for io in hits:
        io_source = io.get('_source')
        line = []

        flat_source = flatten_dict(io_source)

        for column_key in ordered_columns:
            line.append(flat_source.get(column_key))

        rows_data.append(tuple(line))

    return rows_data


def get_column_value_map(
    app_id: int, search_response: dict, with_relations: bool, **_kwargs
) -> dict[str, str]:
    apps = search_response['apps'] if 'apps' in search_response.keys() else []
    main_property_columns = get_io_property_columns(app_id, apps)
    headers = get_io_attribute_headers()
    column_map = {
        'id': headers[0],
        'title': headers[1],
    }

    for column_key in main_property_columns:
        column = main_property_columns.get(column_key)

        if column.get('is_relation'):
            if with_relations:
                relation_header_text = column.get('header_text')
                relation_headers = get_io_attribute_headers(relation_header_text)
                column_map[f'properties.{column_key}.id'] = relation_headers[0]
                column_map[f'properties.{column_key}.title'] = relation_headers[1]
                relation_columns = get_io_property_columns(
                    column.get('relation_app_id'), apps
                )

                for relation_column_key in relation_columns:
                    relation_column = relation_columns.get(relation_column_key)

                    if not relation_column.get('is_relation'):
                        column_map[
                            f'properties.{column_key}.properties.{relation_column_key}'
                        ] = f"{relation_header_text} {relation_column.get('header_text')}"
        else:
            column_map[f'properties.{column_key}'] = column.get('header_text')

    return column_map


def append_column_considering_app_view_properties(
    ordered_columns: list[str], app_view_properties: list[str], column
):
    column_with_stripped_inner_props = ".".join(column.split(".", 2)[:2])

    if not app_view_properties or column_with_stripped_inner_props in app_view_properties:
        ordered_columns.append(column)


def get_final_ordered_columns(
    column_map: dict[str, str], columns: str, app_view_properties: list[str]
) -> list[str]:
    ordered_columns = []
    columns_map_keys = column_map.keys()

    if columns:
        for column in columns.split(','):
            if column in columns_map_keys:
                append_column_considering_app_view_properties(
                    ordered_columns, app_view_properties, column
                )
            else:
                print(f'Input column {column} does not exist in the search result')

        print('Ordered columns from argument: ', ordered_columns)
    else:
        for column in columns_map_keys:
            append_column_considering_app_view_properties(
                ordered_columns, app_view_properties, column
            )

    return ordered_columns


def build_excel_for_search_response(
    main_app_id: int,
    search_response: dict,
    filename: str,
    columns: str,
    with_relations: bool,
    app_view_properties: list[str]
):
    column_map = get_column_value_map(main_app_id, search_response, with_relations)
    ordered_columns = get_final_ordered_columns(
        column_map, columns, app_view_properties
    )
    headers = get_io_headers(column_map, ordered_columns)
    rows = get_io_rows(search_response, ordered_columns)

    excel_data = [headers, *rows]

    write_excel(excel_data, filename, True)
