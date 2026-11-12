# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Python SDK & REST API
"""

from .core import KampusRehberi, Campus
from .advisor import TercihDanismani
from .api import run_api_server

__version__ = "2.0.0"
__all__ = ["KampusRehberi", "Campus", "TercihDanismani", "run_api_server"]
