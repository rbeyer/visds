import argparse
import dagster
from dagster import asset
import json
import logging
import os
import sys
from time import sleep
from yamcs.client import YamcsClient
from visdag.db_con import get_postgres_db
from visdag import watcher


## Not in alphabetical order because need to have path and os imported first.
# Once the vipersci module is installed, this mess can go away.
# TODO: make sure vipersci is installed and fix the imports.
sys.path.insert(1, os.path.join(sys.path[0],'/Work/VIPER/vipersci/src'))
from vipersci.vis.pds.create_raw import Creator
import vipersci.util as util


@asset
def vis_raw_fetch2():
    """Watcher pulls objects from the yamcs server.
    I could not figure out how to define configurations
    outside of the asset in a way that makes sense to me
    so for now we're defining everything here. 
    TODO: make this externally-configurable."""
    parameters = watcher.parameters
    args = [ 
            "-json", 'watcher.json', 
            "-outdir", None, 
            "-dburl", None, 
            "-verbose", 0, 
            "-yamcs_client", "localhost:8090/yamcs", 
            ]
    processor = watcher.make_processor()
    watcher.do_json(args, processor)
