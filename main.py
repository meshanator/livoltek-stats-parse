import configparser
import datetime
import logging
import os
import re
from dataclasses import asdict

from influxdb_helper import InfluxDBHelper
from livoltek_file import LivoltekFile
from livoltek_parser import LivoltekParser
from pvoutput_helper import PVOutputHelper

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.sections()
config.read("config.ini")

overrideDirectory = config["general"]["OverrideDirectory"]
fileRegexPattern = config["general"]["FileRegexPattern"]
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
        if archiveFolderName:
            newname = f"{archiveFolderName}/{timestamp}.{file_name}"
            logger.info("Renaming to %s", newname)
            os.rename(file_name, newname)

        if influxdbEnabled:
            influxdbHost = config["influxdb"]["Host"]
            influxdbPort = int(config["influxdb"]["Port"])
            influxdbDatabase = config["influxdb"]["Database"]
            influxdbMeasurement = config["influxdb"]["Measurement"]

            influxDBHelper = InfluxDBHelper(
                influxdbHost,
                influxdbPort,
                influxdbDatabase,
                influxdbMeasurement,
            )
            influxDBHelper.push_to_influxdb(
                ll_file,
            )

        if pvoutputEnabled:
            pvoutputApiKey = config["pvoutput"]["ApiKey"]
            pvoutputSystemId = config["pvoutput"]["SystemId"]
            pvoutputUrl = config["pvoutput"]["Url"]
            pVOutputHelper = PVOutputHelper(
                pvoutputApiKey, pvoutputSystemId, pvoutputUrl
            )
            pVOutputHelper.push_to_pvoutput(ll_file)
