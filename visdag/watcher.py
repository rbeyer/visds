#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
from pathlib import Path
from time import sleep
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yamcs.client import YamcsClient

import os
sys.path.insert(1, os.path.join(sys.path[0],'/users/moses/Documents/Development/VIPER/vipersci/src'))

from vipersci.vis.pds.create_raw import Creator
import vipersci.util as util


parameters = [
    "/ViperGround/Images/ImageData/Navcam_left_icer",
    "/ViperGround/Images/ImageData/Navcam_left_jpeg",
    "/ViperGround/Images/ImageData/Navcam_right_icer",
    "/ViperGround/Images/ImageData/Navcam_right_jpeg",
    "/ViperGround/Images/ImageData/Aftcam_left_icer",
    "/ViperGround/Images/ImageData/Aftcam_left_jpeg",
    "/ViperGround/Images/ImageData/Aftcam_right_icer",
    "/ViperGround/Images/ImageData/Aftcam_right_jpeg",
    "/ViperGround/Images/ImageData/Hazcam_front_left_icer",
    "/ViperGround/Images/ImageData/Hazcam_front_left_jpeg",
    "/ViperGround/Images/ImageData/Hazcam_front_right_icer",
    "/ViperGround/Images/ImageData/Hazcam_front_right_jpeg",
    "/ViperGround/Images/ImageData/Hazcam_back_left_icer",
    "/ViperGround/Images/ImageData/Hazcam_back_left_jpeg",
    "/ViperGround/Images/ImageData/Hazcam_back_right_icer",
    "/ViperGround/Images/ImageData/Hazcam_back_right_jpeg",
]
# The structure for adding SLoG images to the database is not complete,
# because I don't know if we have to worry about it, so it hasn't been
# built out.  Which is why these are separate.  If, indeed, SLoG images
# could come down from the rover, then a variety of code changes are needed
# in raw_products.py and create_raw.py
slog_parms = [
    "/ViperGround/Images/ImageData/Navcam_left_slog",
    "/ViperGround/Images/ImageData/Navcam_right_slog",
    "/ViperGround/Images/ImageData/Aftcam_left_slog",
    "/ViperGround/Images/ImageData/Aftcam_right_slog",
    "/ViperGround/Images/ImageData/Hazcam_front_left_slog",
    "/ViperGround/Images/ImageData/Hazcam_front_right_slog",
    "/ViperGround/Images/ImageData/Hazcam_back_left_slog",
    "/ViperGround/Images/ImageData/Hazcam_back_right_slog",
]


class Watcher(list):

    def on_data(self, data):
        for parameter in data.parameters:
            print(f"{parameter.generation_time} - {parameter.name}")
            self.append(
                (
                    parameter.name,
                    parameter.generation_time.isoformat(),
                    parameter.eng_value['imageHeader']
                )
            )


def arg_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        parents=[util.parent_parser()]
    )
    parser.add_argument(
        "-y", "--yamcsclient",
        default="localhost:8090/yamcs",
    )
    parser.add_argument(
        "-d", "--dburl",
        help="Something like postgresql://postgres:NotTheDefault@localhost/visdb"
    )
    parser.add_argument(
        "-j", "--json",
        help="If neither -d or -o are given, a JSON file of the Yamcs "
             "parameters will be written."
    )
    parser.add_argument(
        "-o", "--outdir",
        type=Path,
        help="Output directory."
    )

    return parser

def do_db(args, processor=None):
    if isinstance(args, dict):
        yamcsclient = args["yamcsclient"]
        print(yamcsclient)
        dburl = args["dburl"]
        print(dburl)
        outdir = args["outdir"]
        outdir = Path(outdir)
        print(outdir)
    else:
        yamcsclient = args.yamcsclient
        dburl = args.dburl
        outdir = args.outdir

    if processor is None:
        client, processor = get_client_processor(yamcsclient)

    engine = create_engine(dburl)
    session_maker = sessionmaker(engine, future=True) 
    creator = Creator(
            outdir=outdir,
            session=session_maker
        )

    processor.create_parameter_subscription(
            parameters,
            on_data=creator.from_yamcs_parameters
        ) 

    wait_loop()


def do_outdir(args, processor=None):
    if isinstance(args, dict):
        yamcsclient = args["yamcsclient"]
        dburl = args["dburl"]
        outdir = args["outdir"]
    else:
        yamcsclient = args.yamcsclient
        dburl = args.dburl
        outdir = args.outdir

    if processor is None:
        client, processor = get_client_processor(yamcsclient)

    creator = Creator(
            outdir=args,
        ) 
    processor.create_parameter_subscription(
            parameters,
            on_data=creator.from_yamcs_parameters
        )
    wait_loop()

def do_json(args, processor): 
    if isinstance(args, dict):
        yamcsclient = args["yamcsclient"]
        dburl = args["dburl"]
        outdir = args["outdir"]
        jsonarg = args["json"]
    else:
        yamcsclient = args.yamcsclient
        dburl = args.dburl
        outdir = args.outdir
        jsonarg = args.json

    if processor is None:
        client, processor = get_client_processor(yamcsclient)

    watched = Watcher() 
    processor.create_parameter_subscription(
            parameters + slog_parms,
            on_data=watched.on_data
        ) 
    with open(jsonarg, "w") as f: 
        json.dump(watched, f, indent=2, sort_keys=True) 

    wait_loop()

def get_client_processor(yamcsclient):
    client = YamcsClient(yamcsclient)
    processor = client.get_processor("viper", "realtime")
    return(client, processor)

def main():
    parser = arg_parser()
    args = parser.parse_args()
    util.set_logger(args.verbose)
    yamcsclient = args.yamcsclient

    client, processor = get_client_processor(yamcsclient)

    if args.dburl is not None:
        do_db(args, processor)

    elif args.outdir is not None:
        do_outdir(args, processor)

    elif args.json is not None:
        do_json(args, processor)

    else:
        parser.print_usage()


def wait_loop():
    print("Press Ctrl-C to stop watching.")
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        print("Stopped watching.")


if __name__ == "__main__":
    sys.exit(main())
