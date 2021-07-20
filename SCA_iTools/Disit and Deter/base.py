import abc
import numpy as _np
import logging
import psutil

logger = logging.getLogger(__name__)

def _initialize_distinguisher(obj, precision, processed_traces):
    _set_precision(obj, precision)
    obj.processed_traces = processed_traces
    obj._is_checked = False

def _set_precision(obj, precision):
    try:
        precision = _np.dtype(precision)
    except TypeError:
        raise TypeError(f'precision should be a valid dtype, not {precision}.')

    if precision.kind != 'f':
        raise ValueError(f'precision should be a float dtype, not {precision.kind}.')
    obj.precision = precision