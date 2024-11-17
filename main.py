#!python

import configparser
import datetime
import logging
import os
import re

from influxdb_helper import InfluxDBHelper
from livoltek_file import LivoltekFile
from livoltek_parser import LivoltekParser
from pvoutput_helper import PVOutputHelper


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")

    overrideDirectory = config["general"]["OverrideDirectory"]
    fileRegexPattern = config["general"]["FileRegexPattern"]
    archive = config.getboolean("general", "Archive")
    archiveFolderName = config["general"]["ArchiveFolderName"]

    influxdbEnabled = config.getboolean("influxdb", "Enabled")
    pvoutputEnabled = config.getboolean("pvoutput", "Enabled")

    logger.info(
        "Starting run, influxdbEnabled: %s, pvoutputEnabled: %s",
        influxdbEnabled,
        pvoutputEnabled,
    )

    if overrideDirectory:
        os.chdir(overrideDirectory)

    for file_name in os.listdir():
        pattern = fileRegexPattern
        if re.match(pattern=pattern, string=file_name):
            timestamp = str(datetime.datetime.now().timestamp())
            ll_file: LivoltekFile = LivoltekParser.process_file(file_name)

            if influxdbEnabled:
                influxdbHost = config["influxdb"]["Host"]
                influxdbToken = config["influxdb"]["Token"]
                influxdbOrg = config["influxdb"]["Org"]
                influxdbBucket = config["influxdb"]["Bucket"]
                influxdbMeasurement = config["influxdb"]["Measurement"]

                influxDBHelper = InfluxDBHelper(
                    influxdbHost,
                    influxdbToken,
                    influxdbOrg,
                    influxdbBucket,
                    influxdbMeasurement,
                )
                influxDBHelper.ping()
                influxDBHelper.push_to_influxdb_v2(
                    ll_file,
                )
                influxDBHelper.close()  # Ensure proper shutdown

            if pvoutputEnabled:
                pvoutputApiKey = config["pvoutput"]["ApiKey"]
                pvoutputSystemId = config["pvoutput"]["SystemId"]
                pvoutputUrl = config["pvoutput"]["Url"]
                pVOutputHelper = PVOutputHelper(
                    pvoutputApiKey, pvoutputSystemId, pvoutputUrl
                )
                pVOutputHelper.push_to_pvoutput(ll_file)

            if archive and archiveFolderName:
                newname = f"{archiveFolderName}/{timestamp}.{file_name}"
                logger.info("Renaming to %s", newname)
                os.rename(file_name, newname)


if __name__ == "__main__":
    main()
