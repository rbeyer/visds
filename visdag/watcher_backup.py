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
sys.path.insert(1, os.path.join(sys.path[0],'/Work/VIPER/vipersci/src'))

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


def main():
    parser = arg_parser()
    args = parser.parse_args()
    util.set_logger(args.verbose)

    client = YamcsClient(args.yamcsclient)
    processor = client.get_processor("viper", "realtime")

    if args.dburl is not None:
        engine = create_engine(args.dburl)
        session_maker = sessionmaker(engine, future=True)

        creator = Creator(
            outdir=args.outdir,
            session=session_maker
        )

        processor.create_parameter_subscription(
            parameters,
            on_data=creator.from_yamcs_parameters
        )

        wait_loop()

    elif args.outdir is not None:

        creator = Creator(
            outdir=args.outdir,
        )

        processor.create_parameter_subscription(
            parameters,
            on_data=creator.from_yamcs_parameters
        )

        wait_loop()

    elif args.json is not None:
        watched = Watcher()

        processor.create_parameter_subscription(
            parameters + slog_parms,
            on_data=watched.on_data
        )

        wait_loop()

        with open(args.json, "w") as f:
            json.dump(watched, f, indent=2, sort_keys=True)

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
