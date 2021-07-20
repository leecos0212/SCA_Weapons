# -*- coding: utf-8 -*-
from iTraces.formats import ets_format as _ets_format
import warnings as _warnings


def _ets_reader(filename):
    _warnings.warn(
        'ETSReader 和 read_ths_from_ets 都可读取ets文件，推荐使用read_ths_from_ets.',
        DeprecationWarning
    )

    return _ets_format.read_ths_from_ets_file(filename=filename)


ETSReader = _ets_reader
