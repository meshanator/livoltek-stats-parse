import datetime
import json
import logging
import os
import time
import urllib
from dataclasses import asdict

import dateutil
from influxdb_client import InfluxDBClient, Point
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
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

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
            ts = line.date.strftime("%Y-%m-%dT%H:%M:%SZ")

            fields = asdict(line)
            fields["time"] = ts

            # TODO
            del fields["date"]

            point_dict = {
                "measurement": self.influxdbMeasurement,
                "time": ts,
                "tags": {
                    "Datetime": line.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "Running Status": running_status,
                },
                "fields": fields,
                "date": line.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            point = Point.from_dict(point_dict)
            result = self.write_api.write(bucket=self.influxdbBucket, record=point)
            logger.info(result)

    def push_to_influxdb_v1(
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
            logger.info(result)
        except InfluxDBClientError:
            logger.exception("error pushing to influxdb")
            raise
