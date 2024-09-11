import os
import boto3
import logging

# Initialize SSM client and logger
ssm_client = boto3.client('ssm')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def modify_bucardo_config(config_parameter_store_name: str, new_db_endpoint: str) -> None:
    path = "/media/bucardo/conf/databases-target.conf"

    try:
        # Get the parameter value from the parameter store
        response = ssm_client.get_parameter(
            Name=config_parameter_store_name,
            WithDecryption=True
        )
        param_value = response['Parameter']['Value'].strip()

        lines = param_value.splitlines()
        last_line = lines[-1].split("|")
        last_line[0] = "replica02"
        last_line[1] = new_db_endpoint
        new_param_value = param_value + "\n" + "|".join(last_line)

        # Write to a file in the EFS file system
        with open(path, "w") as file:
            file.write(new_param_value)

    except Exception as e:
        logger.error(f"Failed to write target config file {config_parameter_store_name}: {e}")
        raise

if __name__ == "__main__":
    config_parameter_store_name = os.getenv("CONFIG_PARAMETER_STORE_NAME")
    new_db_endpoint = os.getenv("NEW_DB_ENDPOINT")

    if config_parameter_store_name and new_db_endpoint:
        modify_bucardo_config(config_parameter_store_name, new_db_endpoint)
    else:
        logger.error("Environment variables not set")

