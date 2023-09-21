from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class LivoltekLine:
    date: datetime
    runningStatus: str

    pv1Current: Decimal
    pv1Voltage: Decimal
    pv1Power: Decimal

    pv2Current: Decimal
    pv2Voltage: Decimal
    pv2Power: Decimal

    acCurrent: Decimal
    acVoltage: Decimal
    acPower: Decimal
    acFrequency: Decimal

    gridCurrent: Decimal
    gridVoltage: Decimal
    gridPower: Decimal

    loadCurrent: Decimal
    loadVoltage: Decimal
    loadPower: Decimal

    batteryCurrent: Decimal
    batteryVoltage: Decimal
    batteryPower: Decimal
    batterySOC: Decimal

    busVoltage: Decimal

    epsCurrent: Decimal
    epsVoltage: Decimal
    epsActivePower: Decimal
    epsApparentPower: Decimal
    epsFrequency: Decimal

    epsL1Voltage: Decimal
    epsL1Current: Decimal
    epsL1Power: Decimal

    epsL2Voltage: Decimal
    epsL2Current: Decimal
    epsL2Power: Decimal

    epsL1L2Frequency: Decimal

    batteryMaxTemperature: Decimal
    batteryMinTemperature: Decimal


# ['Datetime', 'Running Status', 'PV1 Current(A)', 'PV1 Voltage(V)',
#        'PV1 Power(kW)', 'PV2 Current(A)', 'PV2 Voltage(V)', 'PV2 Power(kW)',
#        'AC Current(A)', 'AC Voltage(V)', 'AC Power(kW)', 'AC Frequency(Hz)',
#        'Grid Current(A)', 'Grid Voltage(V)', 'Grid Power(kW)',
#        'Load Current(A)', 'Load Voltage(V)', 'Load Power(kW)',
#        'Battery Current(A)', 'Battery Voltage(V)', 'Battery Power(kW)',
#        'Battery SoC(SoC)', 'BUS Voltage(V)', 'EPS Current(A)',
#        'EPS Voltage(V)', 'EPS Active Power(kW)', 'EPS ApparentPower(VA)',
#        'EPS.Frequency(Hz)', 'EPS L1 Voltage(V)', 'EPS L1 Current(A)',
#        'EPS L1 Power(kW)', 'EPS L2 Voltage(V)', 'EPS L2 Current(A)',
#        'EPS L2 Power(kW)', 'EPS L1/L2 Frequency(Hz)',
#        'Battery max temperature(℃)', 'Battery min temperature(℃)']
