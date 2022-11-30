from dagster import op, job

@op(config_schema={"filename": str})
def process_json(context):
    filename = context.op_config["filename"]
    context.log.info(filename)

@job
def log_raw_json():
    process_json()
