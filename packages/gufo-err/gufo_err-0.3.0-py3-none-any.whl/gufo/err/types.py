# ---------------------------------------------------------------------
# Gufo Err: Types
# ---------------------------------------------------------------------
# Copyright (C) 2022, Gufo Labs
# ---------------------------------------------------------------------
"""
Public API data types.
"""

# Python modules
from typing import Any, Optional, List, Dict
from dataclasses import dataclass
from uuid import UUID
import datetime


@dataclass
class Anchor(object):
    """
    Exact problem position (Python 3.11+).
    Denotes operator of subscript which causes
    the problem
    """

    left: int
    right: int


@dataclass
class CodePosition(object):
    """
    Exact code position for Python 3.11+

    Args:
        start_line: First line of code
        end_line: Last line of code
        start_col: Starting column (on start_line)
        end_col: Ending column (on end_line)
        anchor: Problem anchor
    """

    start_line: int
    end_line: int
    start_col: int
    end_col: int
    anchor: Optional[Anchor]


@dataclass
class SourceInfo(object):
    """
    Source context for frame.

    Args:
        file_name: Normalized file name.
        first_line: first line of source context.
        current_line: current execution line.
        lines: List of lines, starting from `first_line`
        pos: Optional exact code position for Python 3.11+
    """

    file_name: str
    first_line: int
    current_line: int
    lines: List[str]
    pos: Optional[CodePosition] = None


@dataclass
class FrameInfo(object):
    """
    Execution frame.

    Args:
        name: Current callable name.
        source: Optional `SourceInfo` procedure. May be missed
            on loader problems.
        locals: Dicts of local variables.
        module: Python module name.
    """

    name: str
    source: Optional[SourceInfo]
    locals: Dict[str, Any]
    module: Optional[str] = None


@dataclass
class ErrorInfo(object):
    """
    Current execution frame information.

    Args:
        name: Application or service name.
        version: Application or service version.
        fingerprint: Error fingerprint.
        stack: List of `FrameInfo`. Current execution frame is first.
        exception: Exception instance, if caught.
        timestamp: Error timestamp.
    """

    name: str
    version: str
    fingerprint: UUID
    stack: List[FrameInfo]
    exception: BaseException
    timestamp: Optional[datetime.datetime] = None
