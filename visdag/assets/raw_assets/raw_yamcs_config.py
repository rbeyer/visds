import argparse
import dagster
from dagster import asset, materialize
import json
import os
from pathlib import Path
import sys
from time import sleep
from yamcs.client import YamcsClient
from visdag.db_con import get_postgres_db


@asset
def raw_yamcs_parameters():
    """This should pull from a config file stored in the file system."""
    raw_yamcs_parameters = [
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

    return(raw_yamcs_parameters)

@asset
def yamcs_client_url():
    """Similarly, this should pull from a config file on the file system."""
    yamcs_client_url = "localhost:8090/yamcs"

    return(yamcs_client_url)


if __name__ == "__main__":
    materialize([raw_yamcs_parameters, yamcs_client_url])
