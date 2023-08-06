# Inopai CLI commands documentation

You can use the [commands_print](#commands_print_link) command to get the documentation in terminal

## Here is a list of all the commands

- [actions_download_all](#actions_download_all_link)
- [actions_update](#actions_update_link)
- [app_get](#app_get_link)
- [app_get_element_definitions](#app_get_element_definitions_link)
- [app_get_schema](#app_get_schema_link)
- [app_get_workflow_states](#app_get_workflow_states_link)
- [commands_print](#commands_print_link)
- [curl_print](#curl_print_link)
- [entries_export](#entries_export_link)
- [entries_export_excel](#entries_export_excel_link)
- [entries_sync](#entries_sync_link)
- [entries_update](#entries_update_link)
- [exports_download_all](#exports_download_all_link)
- [exports_update](#exports_update_link)

## <a id="actions_download_all_link"></a> actions_download_all
usage: inopaicli actions_download_all [-h] -a APP [-o OUTPUTDIRECTORY] [-t] [--useactionids]

description:
Download actions from application ID and generate json file to an output location

examples:
`("inopaicli actions_download_all -a P -o './actions'", "inopaicli actions_download_all -a P -o './actions' -c")`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -o OUTPUTDIRECTORY, --outputdirectory OUTPUTDIRECTORY
                        Folder with action files
  -t, --includeunused   Include unused actions
  --useactionids        Use action ids instead of action identifiers
## <a id="actions_update_link"></a> actions_update
usage: inopaicli actions_update [-h] [-a APP] -f FOLDER [--useactionids] [--allowedurls ALLOWEDURLS]

description:
Update all actions for specified application from data in folder

examples:
`("inopaicli actions_update -a P -f './actions' --allowedurls http://localhost:9000", "inopaicli actions_update -a P -f './actions' --allowedurls http://localhost:9000 --useactionids")`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -f FOLDER, --folder FOLDER
                        Folder with action files
  --useactionids        Use action ids instead of action identifiers
  --allowedurls ALLOWEDURLS
## <a id="app_get_link"></a> app_get
usage: inopaicli app_get [-h] -a APP

description:
Download application from id and print it

examples:
`('inopaicli app_get -a P',)`

options:
  -h, --help         show this help message and exit
  -a APP, --app APP  Application ID
## <a id="app_get_element_definitions_link"></a> app_get_element_definitions
usage: inopaicli app_get_element_definitions [-h] -a APP [-o OUTPUTDIRECTORY]

description:
Download element definitions and generate json file to an output location

examples:
`("inopaicli app_get_element_definitions -a P -o './directory'",)`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -o OUTPUTDIRECTORY, --outputdirectory OUTPUTDIRECTORY
                        Specify the directory where to generate the json file with element definiton
## <a id="app_get_schema_link"></a> app_get_schema
usage: inopaicli app_get_schema [-h] -a APP -o OUTPUTDIRECTORY

description:
Returns app schema for specified application from data in folder

examples:
`("inopaicli app_get_schema -a P -o './directory'",)`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -o OUTPUTDIRECTORY, --outputdirectory OUTPUTDIRECTORY
                        Specify the directory where to generate the json file with app schema
## <a id="app_get_workflow_states_link"></a> app_get_workflow_states
usage: inopaicli app_get_workflow_states [-h] -a APP -o OUTPUTDIRECTORY

description:
Download workflow information from application id and generate json file to an output location

examples:
`("inopaicli app_get_workflow_states -a P -o './directory'",)`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -o OUTPUTDIRECTORY, --outputdirectory OUTPUTDIRECTORY
                        Specify the directory where to generate the json file with workflow information
## <a id="commands_print_link"></a> commands_print
usage: inopaicli commands_print [-h] [-d]

description:
Prints all command documentations

examples:
`('inopaicli commands_print', 'inopaicli commands_print --devupdate')`

options:
  -h, --help       show this help message and exit
  -d, --devupdate  Used from a developer to update the COMMANDS.md file
## <a id="curl_print_link"></a> curl_print
usage: inopaicli curl_print [-h]

description:
Prints curl command with your session id and url

examples:
`('inopaicli curl_print',)`

options:
  -h, --help  show this help message and exit
## <a id="entries_export_link"></a> entries_export
usage: inopaicli entries_export [-h] [-a APP] [-g GROUP] [-f FILENAME] [--force] [--query QUERY]
                                [--sourceoverride SOURCEOVERRIDE]

description:
Export group ios entries in json format

examples:
`("inopaicli entries_export -g P -a P -f '/filedir/filename.json'",)`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -g GROUP, --group GROUP
                        Group ID
  -f FILENAME, --filename FILENAME
                        Filename for destination json file (print if no filename given)
  --force
  --query QUERY
  --sourceoverride SOURCEOVERRIDE
## <a id="entries_export_excel_link"></a> entries_export_excel
usage: inopaicli entries_export_excel [-h] [-a APP] [-g GROUP [GROUP ...]] [-f FILENAME] [--force] [--query QUERY]
                                      [--columns COLUMNS] [--printcolumns] [--withrelations]
                                      [--appviewid APPVIEWID]

description:
Export group ios entries in excel format

examples:
`('inopaicli entries_export_excel -g 1 -a 1 --printcolumns', 'inopaicli entries_export_excel -g 1 -a 1 --columns "id, properties.firstname" --force', "inopaicli entries_export_excel -g 1 2 3 -a 1 -f '/filedir/filename.xlsx'")`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -g GROUP [GROUP ...], --group GROUP [GROUP ...]
                        Group ID or a list of IDs
  -f FILENAME, --filename FILENAME
                        Filename for destination json file (print if no filename given)
  --force
  --query QUERY
  --columns COLUMNS
  --printcolumns        Print the columns that would be exported
  --withrelations       Export relation properties in the excel too
  --appviewid APPVIEWID
                        Application View ID
## <a id="entries_sync_link"></a> entries_sync
usage: inopaicli entries_sync [-h] -a APP -g GROUP -p_name PROPERTY_NAME [-f FILENAME] [-c CHUNK_SIZE]
                              [--prevent_io_create] [--prevent_io_update]
                              [--user_forces_skip_actions USER_FORCES_SKIP_ACTIONS [USER_FORCES_SKIP_ACTIONS ...]]

description:
Synchronize ios from id in json file

examples:
`('inopaicli entries_sync -a P -g P -p fdjshk -f FILENAME',)`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -g GROUP, --group GROUP
                        Group ID
  -p_name PROPERTY_NAME, --property_name PROPERTY_NAME
                        Property name
  -f FILENAME, --filename FILENAME
                        Filename for spare part input data json file
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
  --prevent_io_create
  --prevent_io_update
  --user_forces_skip_actions USER_FORCES_SKIP_ACTIONS [USER_FORCES_SKIP_ACTIONS ...]
                        User forces skip actions
## <a id="entries_update_link"></a> entries_update
usage: inopaicli entries_update [-h] [--request_data_file REQUEST_DATA_FILE]

description:
Update entries from requested file

examples:
`('inopaicli ios_patch --requestdatafile ./requested-file.json',)`

options:
  -h, --help            show this help message and exit
  --request_data_file REQUEST_DATA_FILE
                        Requested file
## <a id="exports_download_all_link"></a> exports_download_all
usage: inopaicli exports_download_all [-h] -a APP [-o OUTPUTDIRECTORY] [--useactionids]

description:
Downloads export in app based on a folder containing data

examples:
`("inopaicli exports_download_all -a P -o './directory'", "inopaicli exports_download_all -a P -o './directory' --useactionids")`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -o OUTPUTDIRECTORY, --outputdirectory OUTPUTDIRECTORY
                        Specify the directory where to generate the json file with exported files
  --useactionids        Use action ids instead of action identifiers
## <a id="exports_update_link"></a> exports_update
usage: inopaicli exports_update [-h] [-a APP] -f FOLDER [--useactionids] [--allowedurls ALLOWEDURLS]

description:
Update export in app based on a folder containing data (.json) and template files (.docx)

examples:
`("inopaicli exports_update -a P -f './directory' --allowedurls http://localhost:9000", "inopaicli exports_update -a P -f './directory' --allowedurls http://localhost:9000 --useactionids")`

options:
  -h, --help            show this help message and exit
  -a APP, --app APP     Application ID
  -f FOLDER, --folder FOLDER
                        Specify the folder where are exported files
  --useactionids        Use action ids instead of action identifiers
  --allowedurls ALLOWEDURLS
