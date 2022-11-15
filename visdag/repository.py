from dagster import (
        define_asset_job,
        load_assets_from_current_module, 
        load_assets_from_package_module, 
        repository,
        resource,
        ScheduleDefinition,
        with_resources,
        )
from . import assets
from .jobs import core_assets_schedule
from .resources import RESOURCES_DEV, RESOURCES_PROD, RESOURCES_LOCAL
from .ops import *
import os

resource_defs_by_deployment_name = {
        "prod": RESOURCES_PROD,
        "dev": RESOURCES_DEV,
        "local": RESOURCES_LOCAL,
        }

all_jobs = [core_assets_schedule]


@repository
def visdag():
    deployment_name = os.environ.get("DAG_DEPLOY", "dev")
    resource_defs=resource_defs_by_deployment_name[deployment_name]
    #definitions = [
    #        #with_resources(
    #        #    load_assets_from_package_module(assets),
    #        #    *all_jobs,
    #        #    ),
    #        # Update all assets once a day
    #        ScheduleDefinition(
    #            job=define_asset_job("all_assets", selection="*"), 
    #            cron_schedule="@daily"
    #            ),
    #        ]
    #return definitions
    return [load_assets_from_package_module(assets)]
