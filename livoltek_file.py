from dataclasses import dataclass

from livoltek_line import LivoltekLine


@dataclass
class LivoltekFile:
    livoltekLines: [LivoltekLine]
