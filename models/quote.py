from dataclasses import dataclass
from datetime import datetime

@dataclass
class DollarQuote:
    """
    Representa una cotización del dólar en una fecha dada.
    - date: fecha como datetime
    - value: valor en CLP en float
    - raw_value: valor original entregado por la API (string con coma decimal)
    """
    date: datetime
    value: float
    raw_value: str
