import dagster
from dagster import asset, materialize, op
from visdag import watch_cam


@asset
def raw_from_yamcs(
        yamcs_client_url, 
        raw_yamcs_parameters, 
        raw_products_table_db_config,
        ):
    args = {
            "yamcsclient": yamcs_client_url,
            "parameters": raw_yamcs_parameters,
            "dburl": raw_products_table_db_config,
            "outdir": "./",
            }
    raw_product = watch_cam.to_db(args)


if __name__ == "__main__":
    materialize([raw_from_yamcs])
