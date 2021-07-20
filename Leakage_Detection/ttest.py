from SCA_iTools import distinguishers
from Leakage_Detection import container as _container
import numpy as _np
import logging

logger = logging.getLogger(__name__)


class TTestContainer:

    def __init__(self, ths_1, ths_2, frame=None, preprocesses=[]):
        self.containers = [
            _container.Container(ths=ths_1, frame=frame, preprocesses=preprocesses),
            _container.Container(ths=ths_2, frame=frame, preprocesses=preprocesses)
        ]

    def __str__(self):
        return f'''Container for ths_1:
    {self.containers[0]}
Container for ths_2:
    {self.containers[1]}
    '''


class TTestAnalysis:

    def __init__(self, precision='float32'):

        self.accumulators = [TTestAccumulator(precision=precision), TTestAccumulator(precision=precision)]

    def run(self, ttest_container):

        if not isinstance(ttest_container, TTestContainer):
            raise TypeError(f'ttest_container should be a type TTestContainer, not {type(ttest_container)}.')

        nb_iterations = sum([max(int(len(cont._ths) / cont.batch_size), 1) for cont in ttest_container.containers])
        logger.info(f'Start run t-test on container {ttest_container}, with {nb_iterations} iterations', {'nb_iterations': nb_iterations})
        for i in range(2):
            container = ttest_container.containers[i]
            logger.info(f'Start processing t-test on ths number {i}.')
            for batch in container.batches():
                self.accumulators[i].update(batch.samples)
                logger.info('t-test iteration finished.')
            self.accumulators[i].compute()

        self._compute()

    '''accu_1, accu_2目标accumulators是两个TTestAccumulator类型的实例化
       TTestAccumulator属性包括processed_traces计算的曲线条数、sum、sum_squared
    '''
    def _compute(self):
        accu_1, accu_2 = self.accumulators
        self.result = (accu_1.mean - accu_2.mean) / _np.sqrt(accu_1.var / accu_1.processed_traces + accu_2.var / accu_2.processed_traces)

    def __str__(self):
        return 't-Test analysis'


class TTestAccumulator:

    def __init__(self, precision):
        distinguishers._initialize_distinguisher(self, precision=precision, processed_traces=0)

    def _initialize(self, traces):
        self.sum = _np.zeros(traces.shape[-1], dtype=self.precision)
        self.sum_squared = _np.zeros(traces.shape[-1], dtype=self.precision)

    def update(self, traces):
        if not isinstance(traces, _np.ndarray):
            raise TypeError(f'traces must be numpy ndarray, not {type(traces)}.')

        traces = traces.astype(self.precision)

        try:
            self.sum
        except AttributeError:
            self._initialize(traces)

        '''traces是二维ndarray shape[0]: trace条数；shape[-1]：trace点数'''
        self.processed_traces += traces.shape[0]
        self.sum += _np.sum(traces, axis=0)
        self.sum_squared += _np.sum(traces ** 2, axis=0)

    def compute(self):
        try:
            assert self.processed_traces > 0
        except (AttributeError, AssertionError):
            raise TTestError('TTestAccumulator has not been initialized, or no traces have been processed.\
                Please initialize and update the accumulator before trying to use compute function.')
        self.mean = self.sum / self.processed_traces
        self.var = self.sum_squared / self.processed_traces - self.mean ** 2


class TTestError(Exception):
    pass
