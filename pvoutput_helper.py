import datetime
import json
import logging
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

logger = logging.getLogger()


class PVOutputHelper:
    def __init__(self, pvoutputApiKey, pvoutputSystemId, pvoutputUrl):
        self.pvoutputApiKey = pvoutputApiKey
        self.pvoutputSystemId = pvoutputSystemId
        self.pvoutputUrl = pvoutputUrl

    @staticmethod
    def batch(x, bs) -> []:
        return [x[i : i + bs] for i in range(0, len(x), bs)]

    def push_to_pvoutput(self, file: LivoltekFile):
        lines = file.livoltekLines
        line_batches = PVOutputHelper.batch(lines, 30)
        logger.info("%s batches to push", len(line_batches))
        for line_batch in line_batches:
            if line_batch:
                self.push_to_pvoutput_batched(line_batch)

    def push_to_pvoutput_batched(self, line_batch: [LivoltekLine]):
        start = line_batch[0].date
        end = line_batch[-1].date

        headers = {
            "X-Pvoutput-Apikey": self.pvoutputApiKey,
            "X-Pvoutput-SystemId": self.pvoutputSystemId,
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
        }

        pvoutputdata = "data="
        line: LivoltekLine
        for line in line_batch:
            date = line.date
            date_str = date.strftime("%Y%m%d")
            hour_str = date.strftime("%H:%M")
            pv1_watts = line.pv1Power * 1000
            load_watts = line.loadPower * 1000
            battery_min_temp = line.batteryMinTemperature
            pv1_voltage = line.pv1Voltage

            s = f"{date_str},{hour_str},,{pv1_watts},,{load_watts},{battery_min_temp},{pv1_voltage};"
            pvoutputdata += s
        if pvoutputdata.endswith(";"):
            pvoutputdata = pvoutputdata[:-1]

        pvoutput_result = requests.post(
            self.pvoutputUrl,
            data=pvoutputdata,
            headers=headers,
        )
        logger.info(
            "PvOutput response %s %s %s %s %s",
            pvoutput_result.status_code,
            "start",
            start,
            "end",
            end,
        )

        if pvoutput_result.status_code != 200:
            logger.info("Error posting to PvOutput")
            return
