import os
from dagster import repository

from .assets import raw_assets
from .sensors import raw_product_json_sensor

"""TODO:
I'm not very happy with the way I'm doing this inclusion of
assets and sensors (and other objects. Basically it seems like I 
have too many places to manage when I add an asset or sensor or 
anything else:
* First, I have to write the asset.
* Then I have to add the asset to the proper group directory
* Then I have to import the asset in __init__.py of either the 
group directory or the main asset directory.
* Then I have to import the asset here.
* Then I have to add the imported asset to the all_assets list

This just seems excessive. I cannot believe there are really that
many places I have to edit every time I add an asset.
"""
all_assets = [*raw_assets]
all_sensors = [raw_product_json_sensor]

@repository
def visdag():
    return [
            all_assets,
            all_sensors,
            ]
