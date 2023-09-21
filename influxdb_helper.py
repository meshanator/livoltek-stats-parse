import datetime
import json
import os
import re
import time
import urllib
from dataclasses import asdict

import dateutil
import pandas as pd
import requests

from livoltek_file import LivoltekFile
from livoltek_line import LivoltekLine


def push_to_influxdb(
    file: LivoltekFile,
    influxdbHost,
    influxdbPort,
    influxdbDatabase,
    influxdbMeasurement,
):
    points = []
    line: LivoltekLine
    for line in file.livoltekLines:
        running_status = line.runningStatus
        ts = line.date.strftime("%Y-%m-%dT%H:%M:%SZ")

        fields = asdict(line)
        fields["time"] = ts

        point = {
            "measurement": influxdbMeasurement,
            "time": ts,
            "tags": {"Datetime": line.date, "Running Status": running_status},
            "fields": fields,
            "date": line.date,
        }
        points.append(point)

    # print(points)
    # try:
    #     result = client.write_points(points)
    # except InfluxDBClientError as e:
    #     # print(points)
    #     print(str(e))
    #     raise

    pass
