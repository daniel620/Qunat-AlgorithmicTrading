from Stock import Stock
import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
"""
Draw Chinese characters on plot pics
"""
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

"""
Read washed data
"""
df_AH = pd.read_excel('data/df_AH.xlsx')

"""
Evaluate the result 
"""
stock1 = Stock('招商银行',df_AH=df_AH[['招商银行','招商银行.1']])
stock2 = Stock('工商银行',df_AH=df_AH[['工商银行','工商银行.1']])
stock3 = Stock('农业银行',df_AH=df_AH[['农业银行','农业银行.1']])

stock1.trading_rule(show_transaction=True)
