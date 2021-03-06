import warnings
import typing

'根据metadata中的tags进行操作'
class TraceHeaderSetDeprecated:

    @property
    def metadata_tags(self):
        return list(self.metadatas.keys())

    def get_trace_by_index(self, x):
        warnings.warn(
            "推荐使用ths[x]简化表示替换TraceHeaderSet.get_trace_by_index.",
            DeprecationWarning
        )
        return self[x]

    def get(self, attr, *args, **kwargs):
        warnings.warn(
            "推荐使用.sample 和 .metadatas 替换 TraceHeaderSet.get.",
            DeprecationWarning
        )
        if attr in ('data', 'points'):
            return self.get_points(*args, **kwargs)
        '读取data和point中的数值'
        try:
            attribute = getattr(self, attr, *args, **kwargs)
        except AttributeError:
            attribute = getattr(self._reader, attr, *args, **kwargs)
        if isinstance(attribute, typing.Callable):
            return attribute()
        return attribute

    def get_attr(self, attr, *args, **kwargs):
        warnings.warn(
            "TraceHeaderSet.get_attr method is deprecated. Use .samples or .metadatas attributes instead.",
            DeprecationWarning
        )
        return self.get(attr, *args, **kwargs)

    def get_points(self, frame=slice(None, None)):
        warnings.warn(
            "TraceHeaderSet.get_points method is deprecated. Use samples attribute.",
            DeprecationWarning
        )
        if frame is None:
            frame = ...
        if isinstance(frame, range):
            frame = slice(frame.start, frame.stop, frame.step)
        if isinstance(frame, tuple):
            frame = list(frame)
        return self.samples[:, frame]

    def __getattr__(self, name):
        if "get_" in name:
            key = "".join("_".join(name.split("_")[1:]))
            try:
                metadata_value = self.metadatas[key]

                def _():
                    return metadata_value

                warnings.warn(
                    f'TraceHeaderSet.{name} method is deprecated. Use .samples or .metadatas attributes instead.',
                    DeprecationWarning
                )
                return _
            except KeyError:
                raise AttributeError(f'Attribute {name} does not exist on {self}.')
        raise AttributeError(f'Attribute {name} does not exist on {self}.')

    @property
    def h5_file(self):
        try:
            return self._reader._h5_file
        except AttributeError:
            pass

    def close(self):
        try:
            self._reader._h5_file.close()
        except AttributeError:
            pass
