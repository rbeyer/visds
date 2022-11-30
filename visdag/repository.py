import os
from contextlib import contextmanager
from dagster import (
        asset,
        job,
        load_assets_from_package_module,
        op,
        repository, 
        with_resources,
        sensor,
        )
from dagster._utils import file_relative_path

from .assets import raw_assets
from .jobs import raw_jobs
from .sensors import raw_sensors

all_assets = [*raw_assets]

all_jobs = [*raw_jobs,
            ]

all_sensors = [*raw_sensors,
               ]

@repository
def visdag():
    """
    "PARAMETER_NAME": {"env": "ENVIRONMENT_VARIABLE_NAME"}
    resource_defs = {
            "local": {
                "db_type": {"env": "db_type"},
                "db_user": {"env": "db_user"},
                "db_pass": {"env": "db_pass"},
                "db_name": {"env": "db_name"},
                "db_host": {"env": "db_host"},
                "db_port": {"env": "db_port"},
                "RAW_DIRECTORY": {"env": "RAW_DIRECTORY"},
                }
            }

    return [
        *with_resources(all_assets, resource_defs["local"]),
            *all_jobs,
            ]
    """
    return [
            all_jobs,
            all_assets,
            all_sensors,
            ]
