import pandas as pd
import numpy as np
from dateutil.parser import parse
import time

# 生成样例数据
table = {}
table['time'] = ['2021-01-04 09:30', '2021-02-10 09:30', '2021-03-03 09:30', '2021-03-29 09:30', '2021-04-19 09:30', '2021-05-31 09:30']
table['value'] = [1000, 1005, 1018, 1025, 1030, 1020]
table['price_H'] = [47.7, 64.7, 59.3, 60.9, 59.2, 71.2]
table['price_A'] = [41.6, 54.7, 49.2, 50.5, 48.6, 56.5]
table['signal'] = [1, -1, 1, -1, 1, -1]
table = pd.DataFrame(table)

Return = [None] * len(table)
Return_acc = [None] * len(table)

for i in range(len(table)):
    if table['signal'][i] == -1:
        Return[i] = table['value'][i]/table['value'][i - 1] - 1
        if i == 1:
            Return_acc[i] = Return[i]
        else:
            Return_acc[i] = Return[i] + Return_acc[i - 2]

Return = pd.DataFrame(Return)
Return_acc = pd.DataFrame(Return_acc)
table = pd.merge(table, Return, left_index=True, right_index=True)
table = pd.merge(table, Return_acc, left_index=True, right_index=True)
table = table.rename(columns= {'0_x': 'return', '0_y': 'return_acc'})

# 计算年化收益率
# 表格中的时间格式为YY-mm-dd HH:MM
# 返回年化收益率的pandas数据
def annualized_return(table):
    Annualized_return = [None] * len(table)
    for i in range(len(table)):
        if table['signal'][i] == -1:
            start_time = parse(table['time'][i - 1])
            end_time = parse(table['time'][i])
            Annualized_return[i] = table['return'][i] / (end_time - start_time).total_seconds() * 60 * 60 * 24 * 365
    return pd.DataFrame(Annualized_return)

# 计算累计年化收益率
# 表格中的时间格式为YY-mm-dd HH:MM
# 返回累计年化收益率的pandas数据
def annualized_return_acc(table):
    Annualized_return_acc = [None] * len(table)
    for i in range(len(table)):
        if table['signal'][i] == -1:
            start_time = parse(table['time'][i - 1])
            end_time = parse(table['time'][i])
            Annualized_return_acc[i] = table['return_acc'][i] / (end_time - start_time).total_seconds() * 60 * 60 * 24 * 365
    return pd.DataFrame(Annualized_return_acc)

# 计算最大回撤及其开始时间与结束时间
# 返回值为最大回撤及其开始时间与结束时间
def maxdown(table):
    Maxdown = 0
    for i in range(len(table)):
        if table['signal'][i] == -1:
            profit = table['value'][i] - table['value'][i - 1]
            if profit < Maxdown:
                Maxdown = profit
                start_time = table['time'][i - 1]
                end_time = table['time'][i]
    return Maxdown, start_time, end_time

# 统计盈亏次数，计算盈亏比
# 返回值为盈利次数，亏损次数与盈亏次数比
def count_profit_loss(table):
    profit_times = 0
    loss_tims = 0
    for i in range(len(table)):
        if table['return'][i] > 0:
            profit_times += 1
        if table['return'][i] < 0:
            loss_tims += 1
    profit_loss_rate = profit_times / loss_tims * 1.0
    return profit_times, loss_tims, profit_loss_rate

# 计算最大收益率
def max_profit(table):
    return table['return'][table['return'].argmax()]

# 计算最大亏损率
def max_loss(table):
    return table['return'][table['return'].argmin()]

# 利用滑动窗口计算收益率的移动平均
# 返回值为增加了平均收益率的table
def MA(table):
    # 滑动窗口大小设为4，意为取最近2次交易的收益率做平均
    window_size = 4
    table['process_return'] = table['return'].fillna(0)
    # 滑动窗口计算平均收益率
    table['MA'] = table['process_return'].rolling(window_size).mean()
    # 去除重复的值
    table['MA'] = table.MA.mask(table.MA.diff().eq(0))
    table = table.drop('process_return', axis=1)
    return table

# 择时策略
# 对比平均收益率与单次交易的收益率生成择时
# 返回值为新的交易策略
def timing_strategy(table):
    table['opration'] = table['signal']
    for i in range(len(table)):
        if table['return'][i] < table['MA'][i]:
            table['opration'][i] = 0
            table['opration'][i - 1] = 0
    return table