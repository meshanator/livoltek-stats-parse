from dataclasses import dataclass
from datetime import datetime

from livoltek_line import LivoltekLine


@dataclass
class LivoltekFile:
    livoltekLines: [LivoltekLine]
