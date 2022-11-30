import json
import os

from dagster import load_assets_from_package_module
from dagster._utils import file_relative_path

from . import core, raw_assets

CORE = "core"
RAW = "raw"

core_assets = load_assets_from_package_module(
        package_module=core, 
        group_name=CORE
        )

raw_assets = load_assets_from_package_module(
        package_module=raw_assets, 
        group_name=RAW
        )
