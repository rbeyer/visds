import os
from dagster import repository

from .assets import raw_assets
from .jobs import raw_jobs
from .sensors import raw_sensors

all_assets = [*raw_assets]
all_jobs = [*raw_jobs]
all_sensors = [*raw_sensors]

@repository
def visdag():
    return [
            all_jobs,
            all_assets,
            all_sensors,
            ]
