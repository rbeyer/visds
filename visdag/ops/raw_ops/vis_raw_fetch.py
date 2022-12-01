import argparse
import dagster
from dagster import asset, AssetMaterialization, MetadataValue, op, load_assets_from_modules
import json
import os
from pathlib import Path
import sys
from time import sleep
from yamcs.client import YamcsClient
from visdag.db_con import get_postgres_db


## Not in alphabetical order because need to have path and os imported first.
# Once the vipersci module is installed, I can avoid this mess.
sys.path.insert(1, os.path.join(sys.path[0],'../../../../vipersci/src'))
from vipersci.vis.pds.create_raw import Creator
import vipersci.util as util
from . import assets



@op
def vis_raw_product_to_db(psql_db_url, raw_from_yamcs):
    vis_raw_product_to_db(raw_from_yamcs, psql_db_url)

@op
def vis_raw_product_to_xml(raw_xml_config, raw_from_yamcs):
    vis_raw_product_to_xml(raw_from_yamcs, raw_xml_config)

@op
def vis_raw_product_to_json(raw_json_config, raw_from_yamcs):
    vis_raw_product_to_json(raw_from_yamcs, raw_json_config)



#@op(config_schema={
#    "yamcs_client_url": str,
#    "raw_yamcs_parameters": list,
#    "psql_db_url": str,
#    )
#def vis_raw_todb(context):
#
#    #watched = Watcher()
#    #client = YamcsClient(yamcs_client)
#    #yamcs_client = "localhost:8090/yamcs"
#    #dburl = "postgresql://viper:viper@localhost:5438/visdb"
#    #outdir = Path(".")
#    args = {
#            "yamcsclient": context.op_config["yamcs_client_url"],
#            "dburl": context.op_config["psql_db_url"],
#            "outdir": "./",
#            }
#
#    do_db(args)



#@asset
#def vis_raw_fetch():
#    """Watcher pulls objects from the yamcs server.
#    I could not figure out how to define configurations
#    outside of the asset in a way that makes sense to me
#    so for now we're defining everything here. 
#    TODO: make this externally-configurable."""
#    parameters = [
#            "/ViperGround/Images/ImageData/Navcam_left_icer", 
#            "/ViperGround/Images/ImageData/Navcam_left_jpeg", 
#            "/ViperGround/Images/ImageData/Navcam_right_icer", 
#            "/ViperGround/Images/ImageData/Navcam_right_jpeg", 
#            "/ViperGround/Images/ImageData/Aftcam_left_icer", 
#            "/ViperGround/Images/ImageData/Aftcam_left_jpeg", 
#            "/ViperGround/Images/ImageData/Aftcam_right_icer", 
#            "/ViperGround/Images/ImageData/Aftcam_right_jpeg", 
#            "/ViperGround/Images/ImageData/Hazcam_front_left_icer", 
#            "/ViperGround/Images/ImageData/Hazcam_front_left_jpeg", 
#            "/ViperGround/Images/ImageData/Hazcam_front_right_icer", 
#            "/ViperGround/Images/ImageData/Hazcam_front_right_jpeg", 
#            "/ViperGround/Images/ImageData/Hazcam_back_left_icer", 
#            "/ViperGround/Images/ImageData/Hazcam_back_left_jpeg", 
#            "/ViperGround/Images/ImageData/Hazcam_back_right_icer", 
#            "/ViperGround/Images/ImageData/Hazcam_back_right_jpeg", 
#        ]
#    yamcs_client = "localhost:8090/yamcs"
#
#    watched = Watcher()
#    client = YamcsClient(yamcs_client)
#    processor = client.get_processor("viper", "realtime")
#    processor.create_parameter_subscription(parameters, 
#                                            on_data=watched.on_data)
#    # sleeping here is a hack. How to enable this to watch indefinitely? 
#    return(json.dumps(watched, sort_keys=True, indent=2))
