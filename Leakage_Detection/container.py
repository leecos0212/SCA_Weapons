from iTraces import traces
import numpy as _np

class Container:

    def __init__(self, ths, frame=None, preprocesses=[]):

        self._set_ths(ths)
        self._set_frame(frame)
        self._set_preprocesses(preprocesses)
        self._trace_size = None

    @property
    def trace_size(self):
        """获取曲线frame内的sample点数"""
        if self._trace_size is None:
            try:
                wrapper = _TracesBatchWrapper(self._ths[0:1], self.frame, self.preprocesses)
                self._trace_size = len(wrapper.samples[0])
            except TypeError:
                self._trace_size = 1
        return self._trace_size
    '''读取后处理方式'''
    def _set_preprocesses(self, preprocesses):
        if (not isinstance(preprocesses, list) or len([p for p in preprocesses if not callable(p)]) > 0) and not callable(preprocesses):
            raise TypeError(f'preprocesses should be a list of preprocess or a single preprocess function, not {type(preprocesses)}.')
        self.preprocesses = [preprocesses] if not isinstance(preprocesses, list) else preprocesses
    '''判断曲线格式合法'''
    def _set_ths(self, ths):
        if not isinstance(ths, traces.TraceHeaderSet):
            raise TypeError(f'ths must be an instance of TraceHeaderSet, not {type(ths)}')
        self._ths = ths
    '''判断frame格式合法，不允许为none或者非法选项'''
    def _set_frame(self, frame):
        if frame is not None and not isinstance(frame, traces.Samples.SUPPORTED_INDICES_TYPES):
            raise TypeError(f'frame should be of type {traces.Samples.SUPPORTED_INDICES_TYPES}, not {type(frame)}.')
        self.frame = frame if frame is not None else ...

    '''保证ref_sizes在以下几个范围内，并且为从小到大的顺序'''
    def _compute_batch_size(self, trace_size):
        ref_sizes = [
            (0, 25000),
            (1001, 5000),
            (5001, 2500),
            (10001, 1000),
            (50001, 250),
            (100001, 100)
        ]
        try:
            input_size = len(self._ths[0].samples[self.frame])
        except AttributeError:
            input_size = 0
        max_size = max(trace_size, input_size)
        for i in range(len(ref_sizes)):
            try:
                if max_size >= ref_sizes[i][0] and max_size < ref_sizes[i + 1][0]:
                    return ref_sizes[i][1]
            except IndexError:
                return ref_sizes[-1][1]

    '''计算frame内的batch_size'''
    @property
    def batch_size(self):
        """Default size of sub-ths provided by `batches` method."""
        return self._compute_batch_size(self.trace_size)
    '''将frame内的ths以及batch_size交给_TracesBatchIterable()'''
    def batches(self, batch_size=None):

        if batch_size and batch_size < 0:
            raise ValueError(f'batch_size must be a positive integer, not {batch_size}.')
        batch_size = batch_size if batch_size else self.batch_size
        return _TracesBatchIterable(
            ths=self._ths,
            batch_size=batch_size,
            frame=self.frame,
            preprocesses=self.preprocesses
        )

    '''返回frame范围数值，f-string{}，其中{}表示需要被替换的部分'''
    def _frame_str(self):
        if isinstance(self.frame, _np.ndarray):
            return f'{str(self.frame)[:20]} ... {str(self.frame)[-20:]}'.replace('\n', '')
        elif self.frame == ...:
            return 'All'
        else:
            return str(self.frame)

    '''使用self属性曲线对template_str进行替换'''
    def __str__(self):
        template_str = f'''Traces container:
    Number of traces: {len(self._ths)}
    Traces size     : {len(self._ths.samples[0])}
    Metadata        : {list(self._ths.metadatas.keys())}
    Frame           : {self._frame_str}
    Preprocesses    : {[p.__name__ for p in self.preprocesses] if len(self.preprocesses) > 0 else 'None'}
        '''
        return template_str

''''''
class _TracesBatchWrapper:

    def __init__(self, ths, frame, preprocesses):
        self.ths = ths
        self.frame = frame
        self.preprocesses = preprocesses

    @property
    def samples(self):
        samples = self.ths.samples[:, self.frame]
        for preprocess in self.preprocesses:
            samples = preprocess(samples)
        return samples

    @property
    def metadatas(self):
        return self.ths.metadatas

    def __len__(self):
        return len(self.ths)

'''获取新的frame属性'''
class _TracesBatchIterable:
    def __init__(self, ths, batch_size, frame, preprocesses):
        self._ths = ths
        '''slice(start, stop[, step]),按照batch_size进行分割，步进选择为1'''
        self._slices = [
            slice(start * batch_size, (start + 1) * batch_size, 1)
            for start in range(len(ths) // batch_size)
        ]
        if len(ths) % batch_size != 0:
            self._slices.append(
                slice(len(ths) // batch_size * batch_size, None, 1)
            )
        self.frame = frame
        self.preprocesses = preprocesses

    '''定义iterable对象，使用yield将其变成一个generator'''
    def __iter__(self):
        for sl in self._slices:
            yield _TracesBatchWrapper(self._ths[sl], frame=self.frame, preprocesses=self.preprocesses)

    def __getitem__(self, key):
        return _TracesBatchWrapper(self._ths[self._slices[key]], frame=self.frame, preprocesses=self.preprocesses)

    def __len__(self):
        return len(self._slices)

