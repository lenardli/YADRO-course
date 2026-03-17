from dataclasses import dataclass, field
from datetime import date
from typing import Dict


@dataclass
class Currency:
    date: date
    rates: Dict[str, float] = field(default_factory=dict)


@dataclass
class Author:
    name: str


@dataclass
class App:
    version: str
    service: str
