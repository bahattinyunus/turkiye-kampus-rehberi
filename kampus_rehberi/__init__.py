# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Python SDK, REST API & YKS Tercih Ekosistemi
"""

from .core import KampusRehberi, Campus
from .advisor import TercihDanismani
from .budget import CostCalculator
from .yks import TercihListesi
from .geo_data import PROVINCE_COORDINATES, get_province_geo
from .api import run_api_server

__version__ = "2.1.0"
__all__ = [
    "KampusRehberi",
    "Campus",
    "TercihDanismani",
    "CostCalculator",
    "TercihListesi",
    "PROVINCE_COORDINATES",
    "get_province_geo",
    "run_api_server"
]
