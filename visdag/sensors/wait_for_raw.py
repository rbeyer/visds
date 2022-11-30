from dagster import op, job, sensor, RunRequest, SkipReason
import os
import hashlib

md5 = hashlib.md5()

def get_hash_for_file(fpath):
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    md5_checksum = md5.hexdigest()
    return(md5_checksum)

"""
TODO: Can/should the @op and @job be extracted into their own
file?
TODO: Replace this generic logging with an actual from_json_to_db 
function so this starts doing what we really want it to do.
TODO: Consider replacing the directory sensor with a sensor
attached to the yamcs server. 
"""
@op(config_schema={"filename": str})
def process_json(context):
    filename = context.op_config["filename"]
    context.log.info(filename)

@job
def log_raw_json():
    process_json()
        

# Watch for new json files to be created in the raw_products directory
# Run this sensor no more often than every 60 seconds.
#@sensor()
@sensor(job=log_raw_json)
def raw_product_json_sensor(context):
    new_files = False
    last_mtime = float(context.cursor) if context.cursor else 0
    max_mtime = last_mtime

    RAW_DIRECTORY = os.getenv("RAW_DIRECTORY")
    print("\n\n\n---------------------")
    print(RAW_DIRECTORY)
    print("---------------------")
    for filename in os.listdir(RAW_DIRECTORY):
        filepath = os.path.join(RAW_DIRECTORY, filename)
        if os.path.isfile(filepath):
            print("---------------------")
            print(filepath)
            print("---------------------")
            fstats = os.stat(filepath)
            file_mtime = fstats.st_mtime
            print(file_mtime)

            print("---------------------")
            print(file_mtime, last_mtime)
            print("---------------------")
            if file_mtime <= last_mtime:
                """ Nothing to do with this file because its modification time
                    is from before the most recent modification time stored in
                    the sensor context.
                """
                continue

            new_files = True
            max_mtime = max(max_mtime, file_mtime)
            """ Get the md5 checksum of the file."""
            md5_checksum = get_hash_for_file(filepath)
            print(md5_checksum)

            """The run_key is built from the filename and its checksum.
            TODO: This is fine for the run_key, but doesn't tell us what to do
            with the mtime Even if the checksum is different from what it 
            was previously, we may end up with running the @op anyway. We probably 
            need to use the max mtime because that can be persisted within dagster 
            and is dependent on all of the file mtimes in the directory. On the 
            other hand, each file's md5 is independent of what might have happened 
            to other files, which means it's not helpful for knowing if we should 
            run the rest of the steps here. 
            """
            run_key = f"{filename}:{md5_checksum}"
            print(run_key)

            run_config = {
                    "ops": {
                        "process_json": {
                            "config": {
                                "filename": filename} 
                            } 
                        }
                    }

        yield RunRequest(run_key=run_key, run_config=run_config)

    if not new_files:
        yield SkipReason(f"No new files found in {RAW_DIRECTORY}.")


    context.update_cursor(str(max_mtime))
