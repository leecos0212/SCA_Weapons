import abc
import typing
import numpy as _np

"""定义合法的数据类型"""

FrameType = typing.Union[....__class__, int, slice, list, _np.ndarray]
MetaType = typing.TypeVar("M")
MetadataTypes = typing.Union[MetaType, typing.Container[MetaType]]
TraceId = typing.TypeVar("I")


class AbstractReader(abc.ABC):
    """定义任意格式曲线读取的基本interface接口"""

    _size = None

    def __len__(self):
        return self._size

    @abc.abstractmethod
    def fetch_samples(self, traces: list, frame=None) -> _np.ndarray:
        pass

    @abc.abstractmethod
    def fetch_metadatas(self, key: typing.Hashable, trace_id: int = None) -> MetadataTypes:
        pass

    @abc.abstractmethod
    def __getitem__(self, key):

        if not isinstance(key, (slice, list, _np.ndarray)):
            raise TypeError('仅允许slice、1维numpy array以及list格式可以被执行')

    @abc.abstractmethod
    def fetch_header(self, key: typing.Hashable):
        pass

    @property
    @abc.abstractmethod
    def metadatas_keys(self):
        pass

    @abc.abstractmethod
    def get_trace_size(self, trace_id):
        pass

    @property
    @abc.abstractmethod
    def headers_keys(self):
        pass
