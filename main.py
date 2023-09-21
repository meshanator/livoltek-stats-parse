import configparser
import datetime
import os
import re
from dataclasses import asdict

from influxdb_helper import push_to_influxdb
from livoltek_file import LivoltekFile
from livoltek_parser import process_file
from pvoutput_helper import push_to_pvoutput

config = configparser.ConfigParser()
config.sections()
config.read("config.ini")

overrideDirectory = config["general"]["OverrideDirectory"]
fileRegexPattern = config["general"]["FileRegexPattern"]
archiveFolderName = config["general"]["ArchiveFolderName"]

influxdbEnabled = config["influxdb"]["Enabled"]
influxdbHost = config["influxdb"]["Host"]
influxdbPort = config["influxdb"]["Port"]
influxdbDatabase = config["influxdb"]["Database"]
influxdbMeasurement = config["influxdb"]["Measurement"]

pvoutputEnabled = config["pvoutput"]["Enabled"]
pvoutputApiKey = config["pvoutput"]["ApiKey"]
pvoutputSystemId = config["pvoutput"]["SystemId"]
pvoutputUrl = config["pvoutput"]["Url"]

if overrideDirectory:
    os.chdir(overrideDirectory)

for file_name in os.listdir():
    pattern = fileRegexPattern
    if re.match(pattern=pattern, string=file_name):
        timestamp = str(datetime.datetime.now().timestamp())
        ll_file: LivoltekFile = process_file(file_name)
        if archiveFolderName:
            newname = f"{archiveFolderName}/{timestamp}.{file_name}"
            print("renaming to", newname)
            os.rename(file_name, newname)

        if influxdbEnabled:
            push_to_influxdb(
                ll_file,
                influxdbHost,
                influxdbPort,
                influxdbDatabase,
                influxdbMeasurement,
            )

        if pvoutputEnabled:
            push_to_pvoutput(ll_file, pvoutputApiKey, pvoutputSystemId, pvoutputUrl)
