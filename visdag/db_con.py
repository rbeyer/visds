import dagster
from dagster import (
        asset,
        fs_io_manager,
        In,
        repository,
        root_input_manager,
        with_resources
        )
import os
import yaml


@dagster.input_manager(config_schema={"base_dir": str})
def read_db_conf(context):
    with open(context.resource_config["base_dir"] + "../../../visdb/src/visdb/database/docker-compose.yml") as yml_f:
        db_conn = yaml.safe_load(yml_f, Loader=yaml.FullLoader)
    return(db_conn)


def get_postgres_db():
    db_conn = read_db_conf()
    db_host = 'localhost'
    db_port = db_conn['services']['postgres']['ports'][0].split(":")[0] 
    db_user=db['services']['postgres']['environment'][0].split("=")[1] 
    db_pass=db['services']['postgres']['environment'][1].split("=")[1] 
    db_name=db['services']['postgres']['environment'][2].split("=")[1]
    db_type='postgresql'
    url = f'{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    return(url)

