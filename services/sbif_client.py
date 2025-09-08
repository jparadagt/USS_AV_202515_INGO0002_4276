# services/sbif_client.py
from __future__ import annotations
import requests
from typing import List
from datetime import datetime
from models.quote import DollarQuote

def _parse_chilean_number(s: str) -> float | None:
    """
    Convierte strings como "$ 1.234,56" o "1.234,56" a float 1234.56
    """
    if s is None:
        return None
    s = s.strip().replace("$", "").replace(" ", "")
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def _parse_sbif_date(s: str) -> datetime | None:
    """
    La API SBIF puede entregar 'YYYY-MM-DD' o 'DD-MM-YYYY'.
    """
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

def fetch_dollar_month(year: int, month: int, api_key: str, timeout: int = 15) -> List[DollarQuote]:
    """
    Obtiene todas las cotizaciones del dólar (CLP) para un año/mes dado.
    Retorna una lista de DollarQuote ordenada por fecha ascendente.
    """
    base = "https://api.sbif.cl/api-sbifv3/recursos_api/dolar"
    url = f"{base}/{year:04d}/{month:02d}"
    params = {"apikey": api_key, "formato": "json"}

    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    data = r.json()

    registros = data.get("Dolares", []) or []
    quotes: List[DollarQuote] = []

    for row in registros:
        date_str = row.get("Fecha")
        raw_value = row.get("Valor")
        dt = _parse_sbif_date(date_str) if date_str else None
        val = _parse_chilean_number(raw_value) if raw_value else None
        if dt and val is not None:
            quotes.append(DollarQuote(date=dt, value=val, raw_value=raw_value))

    quotes.sort(key=lambda q: q.date)
    return quotes

def latest_quote(quotes: List[DollarQuote]) -> DollarQuote | None:
    """
    Devuelve la última cotización del período si existe.
    """
    return quotes[-1] if quotes else None
