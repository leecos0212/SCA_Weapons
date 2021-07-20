from iTraces import formats
from Leakage_Detection.ttest import *
#import pytest
import numpy as np
from matplotlib import pylab as plt
plt.rcParams["figure.figsize"] = [12, 4]
plt.rcParams["figure.dpi"] = 96

'''define traces with fixed plaintext from RAM'''
#@pytest.fixture
# 模拟生成200条曲线，每条曲线100个sample，其中明文是固定的16字节数据
def ths_1():
    shape = (200, 100)
    sample = np.random.randint(0, 255, (100,), dtype='uint8')
    plain = np.random.randint(0, 255, (16), dtype='uint8')
    samples = np.array([sample for i in range(shape[0])], dtype='uint8')
    plaintext = np.array([plain for i in range(shape[0])], dtype='uint8')
    #print(plaintext)
    return formats.read_ths_from_ram(samples=samples, plaintext=plaintext)

'''define traces with randomized plaintext from RAM'''
#@pytest.fixture
# 模拟生成200条曲线，每条曲线100个sample，其中明文是随机的16字节数据
def ths_2():
    shape = (200, 100)
    samples = np.random.randint(0, 255, shape, dtype='uint8')
    plaintext = np.random.randint(0, 255, (shape[0], 16), dtype='uint8')
    #print(plaintext)
    return formats.read_ths_from_ram(samples=samples, plaintext=plaintext)

# 读取两条曲线，进行T-test统计计算
def test_ttest_analysis_run(ths_1, ths_2):
    cont = TTestContainer(ths_1, ths_2)
    analysis = TTestAnalysis(precision='float64')
    analysis.run(cont)
    print(analysis.result)
    TtestResult = []

    t_1 = ths_1.samples[:].astype('float64')
    t_2 = ths_2.samples[:].astype('float64')

    mean_1 = np.sum(t_1, axis=0) / len(ths_1)
    mean_2 = np.sum(t_2, axis=0) / len(ths_2)
    var_1 = (np.sum(t_1 ** 2, axis=0) / len(ths_1) - mean_1 ** 2) / len(ths_1)
    var_2 = (np.sum(t_2 ** 2, axis=0) / len(ths_2) - mean_2 ** 2) / len(ths_2)
    expected = (mean_1 - mean_2) / np.sqrt(var_1 + var_2)
    #print(expected)
    #print(max(abs(expected)))
    #print(np.argpartition(abs(expected),len(expected)-1)[len(expected)-1])
    '''返回ttest统计中的最大值，以及对应Sample index'''
    TtestResult.append(max(abs(expected)))
    TtestResult.append(np.argpartition(abs(expected),len(expected)-1)[len(expected)-1])
    print("The T-Test result and the sample position is:", TtestResult)
    return TtestResult
    #assert analysis.result is not None
    #assert np.array_equal(expected, analysis.result)

# 实例化两个曲线集合
trace_setA = ths_1()
trace_setB = ths_2()
'''
    曲线格式解析
'''
# 曲线头格式
print(trace_setA)
# 曲线条数
print("Trace number....:", len(trace_setA))
# 曲线点数
print("Sample of trace....:", len(trace_setA[0]))
# 曲线格式
print("\nTrace format....", trace_setA[0])
# 曲线tag显示
print("\nplaintext.....:", trace_setA[0].plaintext)
# 多组显示
print("\nplaintext of multi traces", trace_setA[0:5].plaintext)
# 选取全部曲线sample
print(trace_setA.samples[:])
# 选取部分曲线的部分sample
print(trace_setA[0:5].samples[0:50])
# 前10条波形显示
plt.title('Trace_SetA')
plt.plot(trace_setA[0:10].samples.T)
plt.show()

# 计算T-test结果，并返回统计值最高的index
test_ttest_analysis_run(trace_setA, trace_setB)
