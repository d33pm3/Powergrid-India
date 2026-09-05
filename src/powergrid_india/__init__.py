"""Powergrid-India — PAN India RE substation master and workbook builder."""

from .parser import parse_master_table
from .reconcile import reconcile, SCHEMA_FIELDS, norm_key, coerce_mw
from .workbook import build_workbook_data, create_workbook, write_dashboard

__version__ = "2.1.2"
__all__ = [
    "parse_master_table",
    "reconcile",
    "SCHEMA_FIELDS",
    "norm_key",
    "coerce_mw",
    "build_workbook_data",
    "create_workbook",
    "write_dashboard",
    "__version__",
]
