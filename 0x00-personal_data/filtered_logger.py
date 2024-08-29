#!/usr/bin/env python3
"""
Module containing the filter_datum function for log message obfuscation.
"""
from typing import List
import re


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    pattern = r'(' + '|'.join(fields) + r')=[^' + separator + r']*'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
