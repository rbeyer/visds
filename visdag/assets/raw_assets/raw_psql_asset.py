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
def raw_products_table_db_config():
    
    raw_psql_db_url = "postgresql://viper:viper@localhost:5438/visdb"

    return(raw_psql_db_url)


if __name__ == "__main__":
    materialize([raw_products_table_db_config])
