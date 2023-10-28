import datetime
import json
import logging
import os
import time
import urllib
from dataclasses import asdict

import dateutil
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

from livoltek_file import LivoltekFile
from livoltek_line import LivoltekLine

logger = logging.getLogger()


class InfluxDBHelper:
    def __init__(
        self,
        influxdbHost,
        influxdbToken,
        influxdbOrg,
        influxdbBucket,
        influxdbMeasurement,
    ):
        self.influxdbHost = influxdbHost
        self.influxdbToken = influxdbToken
        self.influxdbOrg = influxdbOrg
        self.influxdbBucket = influxdbBucket
        self.influxdbMeasurement = influxdbMeasurement
        self.client = InfluxDBClient(
            url=self.influxdbHost, token=self.influxdbToken, org=self.influxdbOrg
        )
        self.write_options = WriteOptions()

    def ping(self):
        self.client.ping()

    def push_to_influxdb_v2(
        self,
        file: LivoltekFile,
    ):
        points = []
        line: LivoltekLine
        for line in file.livoltekLines:
            running_status = line.runningStatus
            ts = line.date.strftime("%Y-%m-%dT%H:%M:%S%z")

            fields = asdict(line)
            fields["time"] = ts

            # TODO
            del fields["date"]

            point_dict = {
                "measurement": self.influxdbMeasurement,
                "time": ts,
                "tags": {
                    "Datetime": line.date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "Running Status": running_status,
                },
                "fields": fields,
                "date": line.date.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }
            point = Point.from_dict(point_dict)
            points.append(point)

        # for inflluxdb v1
        # self.client.write_points(points)

        with self.client.write_api(write_options=self.write_options) as client:
            logger.info("sending batch of %s to influxdb", len(points))
            client.write(bucket=self.influxdbBucket, record=points)
