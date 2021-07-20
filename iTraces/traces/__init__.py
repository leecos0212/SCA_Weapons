from iTraces.traces.trace import Trace
from iTraces.traces.trace_header_set import TraceHeaderSet, build_trace_header_set
from iTraces.traces.samples import Samples
from iTraces.traces.metadatas import Metadatas
from iTraces.traces.abstract_reader import AbstractReader
from iTraces.traces import headers

'''定义曲线属性用到的所有函数
    Trace{TraceHeaderSet|build_trace_header_set|Samples|Metadatas|AbstractReader}
'''
__all__ = [
    "Trace",
    "TraceHeaderSet",
    "build_trace_header_set",
    "Samples",
    "Metadatas",
    "AbstractReader"
]
