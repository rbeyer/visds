import os
from dagster import repository

from .assets import raw_assets
from .sensors import raw_product_json_sensor

all_assets = [*raw_assets]
all_sensors = [raw_product_json_sensor]

@repository
def visdag():
    return [
            all_assets,
            all_sensors,
            ]
