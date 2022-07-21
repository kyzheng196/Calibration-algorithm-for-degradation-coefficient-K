import math
import pandas as pd
from numpy import *
import time

# 异常值过滤更新机制
def err_filter(arr):
    arr1 = arr[:]
    a = 0.6 # 异常值范围
    i = 0
    n = len(arr)
    m = 0

    while n != m: # 判别遍历后arr长度是否相等，若相等则已完成过滤，输出结果
        n = len(arr)
        while i < len(arr):
            arr1.pop(i)
            if arr[i] > mean(arr1) * (1+a) or arr[i] < mean(arr1) * (1-a): # 误差范围计算
                arr.pop(i)
            else:
                i += 1

            arr1 = arr[:]

        m = len(arr)

    return arr


# 计算C、Co
def avg(pollu, day):

    fpath1 = r'...\浓度_时间数据.xlsx'

    if pollu == 'COD':
        df = pd.read_excel(fpath1, sheet_name="COD", header=0)
    elif pollu == 'NH4':
        df = pd.read_excel(fpath1, sheet_name="NH4", header=0)
    elif pollu == 'TN':
        df = pd.read_excel(fpath1, sheet_name="TN", header=0)
    elif pollu == 'TP':
        df = pd.read_excel(fpath1, sheet_name="TP", header=0)

    a = list(df.columns)[1:-1] # 表头截取

    for i in range(len(a)-1):
        if a[i] >= day and a[i] < day+1: # df列判别
            a1 = list(df[a[i]])
            a2 = list(df[a[i+1]])

            # 求C0、C--异常值未过滤
            C0 = round(mean(a1), 2)
            C = round(mean(a2), 2)
            print("第" + str(i) + "至" + str(i+1) + "天， " + pollu + " 异常值未过滤求得C0值为：" + str(C0))
            print("第" + str(i) + "至" + str(i+1) + "天， " + pollu + " 异常值未过滤求得C值为：" + str(C))

            # 求C0、C--过滤异常值--轮询更新机制
            C0 = round(mean(err_filter(a1)), 2)
            C = round(mean(err_filter(a2)), 2)
            print("第" + str(i) + "至" + str(i+1) + "天， " + pollu + " 异常值过滤后求得C0值为：" + str(C0))
            print("第" + str(i) + "至" + str(i+1) + "天， " + pollu + " 异常值过滤后求得C值为：" + str(C))

            break

    return C0, C


# 迭代求解
def iterate(i, C0, C):

    # 公式求K
    a1 = -math.log(C/C0) / 86400
    print(i + " 公式求得K值为：" + str(a1) + "\n")

    return round(a1, 9)

    #----------------------------------------------------------------------------#
    #迭代法（优化前后）仅适用于C0>C的情况，后续试验需使用公式求K值

    cnt = 0

    '''
    # for循环迭代
    start_time = time.time()
    
    for k in arange(0, 0.01, 0.0000000001):
        cnt += 1
        m = abs(C-C0*exp(-k*86400))
        if abs(C-C0*exp(-k*86400)) < 0.001: # 误差判别
            print(i + " 初始算法迭代求得K值为：" + str(k))
            print(i + " 初始算法迭代次数为：" + str(cnt))
            
            end_time = time.time()

            print("初始算法运行时间为：" + str(round(end_time-start_time, 4)) + "秒" + "\n")
            
            return k
        #elif C-C0*exp(-k*86400) > 0.001:
            #break

    k = 0.005
    a = 0.003
    delta = 1

    start_time = time.time()

    while(delta > 0.001):
        k1 = k * (1+a)
        k2 = k * (1-a)
        # 定义梯度表达式
        f1 = C - C0 * exp(-k1 * 86400)
        f2 = C - C0 * exp(-k2 * 86400)
        delta = min(f1, f2)
        cnt += 1

        if k1 <= k2:
            k = k1
        elif k1 > k2:
            k = k2

    end_time = time.time()

    print(i + " 梯度下降算法迭代求得K值为：" + str(k))
    print(i + " 梯度下降算法迭代次数为：" + str(cnt))
    print("梯度下降算法运行时间为：" + str(round(end_time - start_time, 4)) + "秒" + "\n")

    return k
    '''


pollu_list = ['COD', 'NH4', 'TN', 'TP']
pollu_dic = {} # 污染物C、C0字典
K_dic = {} # 污染物K值字典
C_list = [[] for i in range(6)]
K_list = [[] for j in range(6)]

for day in range(0, 6):
    for i in pollu_list:
        #pollu_dic[i] = avg(i, day)
        #K_dic[i] = iterate(i, pollu_dic[i][0], pollu_dic[i][1])
        C_list[day].append(avg(i, day))
        i1, day1 = avg(i, day)
        K_list[day].append(iterate(i, i1, day1))

#print(pollu_dic)
#print(K_dic)
print(C_list)
print(K_list)

name = ['COD', 'NH4', 'TN', 'TP']
df = pd.DataFrame(columns = name, data =K_list)
df.to_csv(r'...\K值输出结果')
