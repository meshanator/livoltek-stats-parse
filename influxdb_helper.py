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
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

from livoltek_file import LivoltekFile
from livoltek_line import LivoltekLine


class InfluxDBHelper:
    def __init__(
        self, influxdbHost, influxdbPort, influxdbDatabase, influxdbMeasurement
    ):
        self.influxdbHost = influxdbHost
        self.influxdbPort = influxdbPort
        self.influxdbDatabase = influxdbDatabase
        self.influxdbMeasurement = influxdbMeasurement
        # print(self.influxdbHost, self.influxdbPort, self.influxdbDatabase, self.influxdbMeasurement, type(self.influxdbMeasurement), type(self.influxdbPort))
        self.client = InfluxDBClient(host=self.influxdbHost, port=self.influxdbPort)
        self.client.switch_database(self.influxdbDatabase)

    def push_to_influxdb(
        self,
        file: LivoltekFile,
    ):
        points = []
        line: LivoltekLine
        for line in file.livoltekLines:
            running_status = line.runningStatus
            ts = line.date.strftime("%Y-%m-%dT%H:%M:%SZ")

            fields = asdict(line)
            fields["time"] = ts

            # TODO
            del fields["date"]

            point = {
                "measurement": self.influxdbMeasurement,
                "time": ts,
                "tags": {
                    "Datetime": line.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "Running Status": running_status,
                },
                "fields": fields,
                "date": line.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            points.append(point)

        try:
            result = self.client.write_points(points)
        except InfluxDBClientError as e:
            # print(points)
            print(str(e))
            raise
