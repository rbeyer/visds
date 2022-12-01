import dagster
from dagster import asset
import json
import os
import sys
from time import sleep
from yamcs.client import YamcsClient
from visdag.db_con import get_postgres_db
from visdag.assets.vis_raw_fetch import vis_raw_fetch
sys.path.insert(1, os.path.join(sys.path[0],'/Work/VIPER/vipersci/src'))
from vipersci.vis.pds.create_raw import Creator
import vipersci.util as util

#@asset
#def vis_raw_to_db(vis_raw_fetch):
#    """Output the watched content to the database writer based on
#    OUTPUT_PARAM."""
#    dburl = "postgresql://viper:viper@localhost:5438/visdb"
#    engine = create_engine(dburl)
#    session_maker = sessionmaker(engine, future=True)
#    creator = Creator(
#            outdir=
