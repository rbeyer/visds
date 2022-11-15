from dagster_postgres.utils import get_conn_string

from dagster._utils import file_relative_path

YAMCS_CONFIG = {
    "client": "localhost:8090/yamcs",
    "parameters": [
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
        ],
}
