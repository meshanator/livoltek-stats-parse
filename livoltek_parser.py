import datetime
import json
import logging
import os
import re
import time
import urllib

import dateutil
import pandas as pd
import requests

from livoltek_file import LivoltekFile
from livoltek_line import LivoltekLine

logger = logging.getLogger(__name__)


class LivoltekParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_value(value):
        # sometimes columns have blank values

        if value == "* 0.0" or value == "-":
            value = 0
        try:
            return float(value)
        except ValueError:
            try:
                return int(value)
            except ValueError:
                pass
        return value

    @staticmethod
    def process_file(file_name):
        logger.info("Processing file %s", file_name)
        timestamp = str(datetime.datetime.now().timestamp())
        df = pd.read_excel(file_name, skiprows=[0])
        lines = []
        for row_index in df.index:
            # ignore blank rows
            if (
                df[df.keys()[2]][row_index] == "-"
                or df[df.keys()[2]][row_index] == "* 0.0"
            ):
                continue

            row_datetime = df["Datetime"][row_index]
            # running_status = df["Running Status"][row_index]
            date = dateutil.parser.parse(row_datetime)
            # ts = date.strftime("%Y-%m-%dT%H:%M:%SZ")

            # fields = {"time": ts}
            # print(df.keys())
            line = LivoltekLine(
                date=date,
                runningStatus=LivoltekParser.parse_value(
                    df["Running Status"][row_index]
                ),
                pv1Current=LivoltekParser.parse_value(df["PV1 Current(A)"][row_index]),
                pv1Voltage=LivoltekParser.parse_value(df["PV1 Voltage(V)"][row_index]),
                pv1Power=LivoltekParser.parse_value(df["PV1 Power(kW)"][row_index]),
                pv2Current=LivoltekParser.parse_value(df["PV2 Current(A)"][row_index]),
                pv2Voltage=LivoltekParser.parse_value(df["PV2 Current(A)"][row_index]),
                pv2Power=LivoltekParser.parse_value(df["PV2 Power(kW)"][row_index]),
                acCurrent=LivoltekParser.parse_value(df["AC Current(A)"][row_index]),
                acVoltage=LivoltekParser.parse_value(df["AC Voltage(V)"][row_index]),
                acPower=LivoltekParser.parse_value(df["AC Power(kW)"][row_index]),
                acFrequency=LivoltekParser.parse_value(
                    df["AC Frequency(Hz)"][row_index]
                ),
                gridCurrent=LivoltekParser.parse_value(
                    df["Grid Current(A)"][row_index]
                ),
                gridVoltage=LivoltekParser.parse_value(
                    df["Grid Voltage(V)"][row_index]
                ),
                gridPower=LivoltekParser.parse_value(df["Grid Power(kW)"][row_index]),
                loadCurrent=LivoltekParser.parse_value(
                    df["Load Current(A)"][row_index]
                ),
                loadVoltage=LivoltekParser.parse_value(
                    df["Load Voltage(V)"][row_index]
                ),
                loadPower=LivoltekParser.parse_value(df["Load Power(kW)"][row_index]),
                batteryCurrent=LivoltekParser.parse_value(
                    df["Battery Current(A)"][row_index]
                ),
                batteryVoltage=LivoltekParser.parse_value(
                    df["Battery Voltage(V)"][row_index]
                ),
                batteryPower=LivoltekParser.parse_value(
                    df["Battery Power(kW)"][row_index]
                ),
                batterySOC=LivoltekParser.parse_value(
                    df["Battery SoC(SoC)"][row_index]
                ),
                busVoltage=LivoltekParser.parse_value(df["BUS Voltage(V)"][row_index]),
                epsCurrent=LivoltekParser.parse_value(df["EPS Current(A)"][row_index]),
                epsVoltage=LivoltekParser.parse_value(df["EPS Voltage(V)"][row_index]),
                epsActivePower=LivoltekParser.parse_value(
                    df["EPS Active Power(kW)"][row_index]
                ),
                epsApparentPower=LivoltekParser.parse_value(
                    df["EPS ApparentPower(VA)"][row_index]
                ),
                epsFrequency=LivoltekParser.parse_value(
                    df["EPS.Frequency(Hz)"][row_index]
                ),
                epsL1Voltage=LivoltekParser.parse_value(
                    df["EPS L1 Voltage(V)"][row_index]
                ),
                epsL1Current=LivoltekParser.parse_value(
                    df["EPS L1 Current(A)"][row_index]
                ),
                epsL1Power=LivoltekParser.parse_value(
                    df["EPS L1 Power(kW)"][row_index]
                ),
                epsL2Voltage=LivoltekParser.parse_value(
                    df["EPS L2 Voltage(V)"][row_index]
                ),
                epsL2Current=LivoltekParser.parse_value(
                    df["EPS L2 Current(A)"][row_index]
                ),
                epsL2Power=LivoltekParser.parse_value(
                    df["EPS L2 Power(kW)"][row_index]
                ),
                epsL1L2Frequency=LivoltekParser.parse_value(
                    df["EPS L1/L2 Frequency(Hz)"][row_index]
                ),
                batteryMaxTemperature=LivoltekParser.parse_value(
                    df["Battery max temperature(℃)"][row_index]
                ),
                batteryMinTemperature=LivoltekParser.parse_value(
                    df["Battery min temperature(℃)"][row_index]
                ),
            )
            lines.append(line)
        ll_file = LivoltekFile(livoltekLines=lines)
        return ll_file
