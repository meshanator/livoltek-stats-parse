import datetime
import json
import os
import re
import time
import urllib

import dateutil
import pandas as pd
import requests

from livoltek_file import LivoltekFile
from livoltek_line import LivoltekLine


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


def process_file(file_name):
    print("importing file", file_name)
    timestamp = str(datetime.datetime.now().timestamp())
    df = pd.read_excel(file_name, skiprows=[0])
    lines = []
    for row_index in df.index:
        # ignore blank rows
        if df[df.keys()[2]][row_index] == "-" or df[df.keys()[2]][row_index] == "* 0.0":
            continue

        row_datetime = df["Datetime"][row_index]
        # running_status = df["Running Status"][row_index]
        date = dateutil.parser.parse(row_datetime)
        # ts = date.strftime("%Y-%m-%dT%H:%M:%SZ")

        # fields = {"time": ts}
        # print(df.keys())
        line = LivoltekLine(
            date=date,
            runningStatus=parse_value(df["Running Status"][row_index]),
            pv1Current=parse_value(df["PV1 Current(A)"][row_index]),
            pv1Voltage=parse_value(df["PV1 Voltage(V)"][row_index]),
            pv1Power=parse_value(df["PV1 Power(kW)"][row_index]),
            pv2Current=parse_value(df["PV2 Current(A)"][row_index]),
            pv2Voltage=parse_value(df["PV2 Current(A)"][row_index]),
            pv2Power=parse_value(df["PV2 Power(kW)"][row_index]),
            acCurrent=parse_value(df["AC Current(A)"][row_index]),
            acVoltage=parse_value(df["AC Voltage(V)"][row_index]),
            acPower=parse_value(df["AC Power(kW)"][row_index]),
            acFrequency=parse_value(df["AC Frequency(Hz)"][row_index]),
            gridCurrent=parse_value(df["Grid Current(A)"][row_index]),
            gridVoltage=parse_value(df["Grid Voltage(V)"][row_index]),
            gridPower=parse_value(df["Grid Power(kW)"][row_index]),
            loadCurrent=parse_value(df["Load Current(A)"][row_index]),
            loadVoltage=parse_value(df["Load Voltage(V)"][row_index]),
            loadPower=parse_value(df["Load Power(kW)"][row_index]),
            batteryCurrent=parse_value(df["Battery Current(A)"][row_index]),
            batteryVoltage=parse_value(df["Battery Voltage(V)"][row_index]),
            batteryPower=parse_value(df["Battery Power(kW)"][row_index]),
            batterySOC=parse_value(df["Battery SoC(SoC)"][row_index]),
            busVoltage=parse_value(df["BUS Voltage(V)"][row_index]),
            epsCurrent=parse_value(df["EPS Current(A)"][row_index]),
            epsVoltage=parse_value(df["EPS Voltage(V)"][row_index]),
            epsActivePower=parse_value(df["EPS Active Power(kW)"][row_index]),
            epsApparentPower=parse_value(df["EPS ApparentPower(VA)"][row_index]),
            epsFrequency=parse_value(df["EPS.Frequency(Hz)"][row_index]),
            epsL1Voltage=parse_value(df["EPS L1 Voltage(V)"][row_index]),
            epsL1Current=parse_value(df["EPS L1 Current(A)"][row_index]),
            epsL1Power=parse_value(df["EPS L1 Power(kW)"][row_index]),
            epsL2Voltage=parse_value(df["EPS L2 Voltage(V)"][row_index]),
            epsL2Current=parse_value(df["EPS L2 Current(A)"][row_index]),
            epsL2Power=parse_value(df["EPS L2 Power(kW)"][row_index]),
            epsL1L2Frequency=parse_value(df["EPS L1/L2 Frequency(Hz)"][row_index]),
            batteryMaxTemperature=parse_value(
                df["Battery max temperature(℃)"][row_index]
            ),
            batteryMinTemperature=parse_value(
                df["Battery min temperature(℃)"][row_index]
            ),
        )
        lines.append(line)
    ll_file = LivoltekFile(livoltekLines=lines)
    return ll_file
