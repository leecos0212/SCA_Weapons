# -*- coding: utf-8 -*-
from iTraces.formats import bin_format as _bin_format
from iTraces.traces.trace_header_set import build_trace_header_set
import warnings as _warnings


class _LegacyBinFormat(_bin_format.BinFormat):

    @property
    def filename(self):
        return self._filenames


def _bin_reader(filename_pattern, dtype, offset=0, **kwargs):
    _warnings.warn(
        'BinReader 和 read_ths_from_bin都可以使用，建议使用BinReader.',
        DeprecationWarning
    )

    files_list = _bin_format.get_sorted_filenames(pattern=filename_pattern)
    reader = _LegacyBinFormat(
        filenames=files_list,
        offset=offset,
        dtype=dtype,
        metadatas_parsers=kwargs,
    )
    return build_trace_header_set(
        reader=reader,
        name=f'Trace header set with {reader}.'
    )


BinReader = _bin_reader
