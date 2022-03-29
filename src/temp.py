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
df_AH = pd.read_excel('data/df_AH_week.xlsx')

from Stock import Stock

# stock1 = Stock('招商银行',df_AH=df_AH[['time','招商银行','招商银行.1','week_num']],week=True)
stock1 = Stock('工商银行',df_AH=df_AH[['time','工商银行','工商银行.1','week_num']],week=True)


stock1.trading_rule(show_transaction=True, is_save=False, show_time=1)

show_bar=True
rtnRate = stock1.record['rtnRate'].values.astype(float)
accRtnRate = stock1.record['accRtnRate'].values.astype(float)
n = len(rtnRate)
if not show_bar:
    plt.subplot(2,1,1)
    plt.plot(np.arange(n)[np.isnan(rtnRate)==False], rtnRate[np.isnan(rtnRate)==False])
    plt.grid()
    plt.xlim(0, n)
    lim = max(rtnRate[np.isnan(rtnRate)==False])
    if abs(min(rtnRate[np.isnan(rtnRate)==False])) > lim:
        lim = abs(min(rtnRate[np.isnan(rtnRate)==False]))
    lim *= 1.1
    plt.ylim(-lim,lim)
    plt.title('Return Rate')
    plt.subplot(2,1,2)
    plt.plot(np.arange(n)[np.isnan(accRtnRate)==False], accRtnRate[np.isnan(accRtnRate)==False])
    plt.grid()
    plt.xlim(0, n)

    plt.title('Accumulative Return Rate')
    
    plt.tight_layout()
    plt.show()
else:
    plt.bar(np.arange(n)[(np.isnan(rtnRate)==False) & (rtnRate>0)], rtnRate[(np.isnan(rtnRate)==False) & (rtnRate>0)], width=200, color='r',label='win')
    plt.bar(np.arange(n)[(np.isnan(rtnRate)==False) & (rtnRate<=0)], rtnRate[(np.isnan(rtnRate)==False) & (rtnRate<=0)], width=200, color='g',label='lose')

    plt.plot(np.arange(n)[np.isnan(accRtnRate)==False], accRtnRate[np.isnan(accRtnRate)==False],linewidth=1,label='acc_return')

    plt.legend()
    plt.title('Return')
    plt.grid()
    plt.tight_layout()
    plt.show()