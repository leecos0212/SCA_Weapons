# -*- coding: utf-8 -*-
"""
    提供所有针对曲线格式的属性定义和操作方法
"""

from .traces import Trace, TraceHeaderSet, Samples, Metadatas, build_trace_header_set, AbstractReader
from .formats import (
    read_ths_from_bin_filenames_list,
    read_ths_from_bin_filenames_pattern,
    read_ths_from_ets_file,
    read_ths_from_trs_file,
    read_ths_from_ram,
    read_ths_from_multiple_ths,
    read_ths_from_sqlite,
    bin_extractor
)
from .formats.ets_writer import ETSWriter, ETSWriterException, compress_ets
from .formats.bin_format import PaddingMode

__all__ = [
    "Trace",
    "TraceHeaderSet",
    "Samples",
    "Metadatas",
    "read_ths_from_bin_filenames_list",
    "read_ths_from_bin_filenames_pattern",
    "read_ths_from_trs_file",
    "bin_extractor",
    "read_ths_from_ets_file",
    "read_ths_from_ram",
    "ETSWriter",
    "ETSWriterException",
    "AbstractReader",
    "build_trace_header_set",
    "PaddingMode",
    "compress_ets",
    "read_ths_from_multiple_ths",
    "read_ths_from_sqlite"
]

# Set default logging handler to avoid "No handler found" warnings.
import logging
from .__version__ import __author__ as AUTHOR, __version__ as VERSION, __author_email__ as AUTHOR_EMAIL  # noqa: F401, N812

logging.getLogger(__name__).addHandler(logging.NullHandler())
