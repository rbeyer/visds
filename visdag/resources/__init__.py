from dagster._utils import file_relative_path
from dagster import resource, build_resources



@resource
def raw_directory():
    RAW_DIRECTORY = file_relative_path(__file__, "./JSON")
    RESOURCES_LOCAL = {
        "RAW_DIRECTORY": RAW_DIRECTORY,
        }
    return(RESOURCES_LOCAL)

#build_resources(resources={"resources_local": raw_directory})


"""
RESOURCES_DB = {
        "yamcs_client": "localhost:8090/yamcs",
        "output_mode": "DB",
        }
RESOURCES_JSON = {
        "yamcs_client": "localhost:8090/yamcs",
        "output_mode": "JSON",
        }
"""
