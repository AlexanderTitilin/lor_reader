from dataclasses import dataclass
import datetime

@dataclass
class Article:
    name: str
    url: str
    date: datetime.date
