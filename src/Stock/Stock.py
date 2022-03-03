import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import os
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

"""港股通的交易费用包含佣金、股票印花税、交易徵费、交易费、中央结算收费。
1、佣金：每宗交易金额的0.25%，支付予证券公司  
2、股票印花税：每宗交易金额的0.1%，支付予香港政府  
3、交易徵费：每宗交易金额的0.003%，支付予证监会  
4、交易费：每宗交易金额的0.005%，支付予交易所  
5、中央结算收费：每宗交易金额的0.002%，支付予结算所(最低港币2元,最高港币100元)"""

class Stock:
    def __init__(self, name, df_AH):
        self.transaction_rate = np.sum([0.0025, 0.001, 0.00003, 0.00005, 0.00002])
        self.name = name
        self.df_AH = df_AH
        self.n = len(self.df_AH)
        self.df_AH.columns = ['A','H']
        self.rolling_window_size = 60 * 24 * 3
        self.df_AH['DR'] =1 - (self.df_AH['H'])/self.df_AH['A']
        self.__adjust_boundry__()
        self.df_AH['DR_mean'] = self.df_AH['DR'].rolling(self.rolling_window_size).mean()
        self.df_AH['DR_std'] = self.df_AH['DR_adjust'].rolling(self.rolling_window_size).std()
        self.df_AH['DR_ub'] = self.df_AH['DR_mean']+self.df_AH['DR_std'] * 1
        self.df_AH['DR_lb'] = self.df_AH['DR_mean']-self.df_AH['DR_std'] * 0.25
        
    def __adjust_boundry__(self):
        H = self.df_AH['H'].values
        for t in range(self.n):
            if H[t] > self.df_AH['A'][t]:
                H[t] *= 1 + self.transaction_rate
            elif H[t] < self.df_AH['A'][t]:
                H[t] *= 1 - self.transaction_rate
        self.df_AH['H_adjust'] = H
        self.df_AH['DR_adjust'] = 1 - self.df_AH['H_adjust']/self.df_AH['A']


    def draw_price(self, is_save = False, save_path='../output'):
        plt.plot(self.df_AH.dropna()['A'],linewidth=1,label='A')
        plt.plot(self.df_AH.dropna()['H'],linewidth=1,label='HK')
        plt.legend()
        plt.title(self.name)
        if is_save:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            plt.savefig(save_path+ '/' + self.name + 'price.png',dpi=600, bbox_inches='tight')
        plt.show()
    
    def draw_DR(self, is_save = False, save_path='../output'):
        plt.plot(self.df_AH.dropna()['DR'], color='steelblue', label='DiscountRate',linewidth=0.8)
        plt.plot(self.df_AH.dropna()['DR_mean'], color='orange', label='Mean')
        plt.plot(self.df_AH.dropna()['DR_ub'], color='orange',linestyle='--', label='ub')
        plt.plot(self.df_AH.dropna()['DR_lb'], color='orange',linestyle='--', label='lb')
        plt.legend()
        plt.title(self.name + '\nDiscount Rate')
        if is_save:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            plt.savefig(save_path + '/' + self.name + 'DR.png',dpi=600, bbox_inches='tight')
        plt.show()

    """
    output:
        
    """
    def trading_rule(self, psntValue=100,show_transaction=False,save_path=''):
        # extract data
        df = self.df_AH
        df = df.dropna(how='any')
        close = df['H'].values
        open = df['H'].values
        ub = df['DR_ub'].values
        lb = df['DR_lb'].values
        DR = df['DR'].values
        n = len(df)
        # initialize state
        value = np.zeros(n)
        buyPoint = np.zeros(n)
        sellPoint = np.zeros(n)
        psntVolm = psntValue/open[0]
        isAllIn = True
        isSell = False
        isBuy = False
        for t in range(n):
            # cal present value
            if isAllIn:
                psntValue = psntVolm * open[t]
            value[t] = psntValue
            # no operation
            if not (isBuy or isSell):
                if DR[t] < lb[t] and isAllIn:
                    isSell = True
                    # all in
                elif DR[t] > ub[t] and not isAllIn:
                    # all out
                    isBuy = True
            # operation
            elif isBuy:
                buyPoint[t] = 1
                isBuy = False
                psntVolm = psntValue/(open[t] * (1 + self.transaction_rate))
                isAllIn = True
            else:# sell
                sellPoint[t] = 1
                psntValue *= (1 - self.transaction_rate)
                isSell = False
                isAllIn = False
        # value, psntValue, buyPoint, sellPoint = trading_rule(df_AH)

        plt.plot(value, label='Value',linewidth=1)
        if show_transaction:
            plt.scatter(np.arange(len(value))[buyPoint == 1],value[buyPoint == 1],color='red',label='Buy',s=10)
            plt.scatter(np.arange(len(value))[sellPoint == 1],value[sellPoint == 1],color='green',label='Sell',s=10)
        plt.legend()
        plt.title(self.name + '\nFinal Value: {:.2f}'.format(psntValue))
        if save_path != '':
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            plt.savefig(save_path+ '/' + self.name + 'value.png',dpi=600, bbox_inches='tight')
        plt.show()

        if show_transaction:
            plt.plot(df['DR'], color='gray', label='DiscountRate',linewidth=0.2,zorder=1)
            plt.plot(df['DR_mean'], color='orange', label='Mean')
            plt.plot(df['DR_ub'], color='orange',linestyle='--', label='ub')
            plt.plot(df['DR_lb'], color='orange',linestyle='--', label='lb')
            plt.scatter(df.index[buyPoint == 1],df['DR'][buyPoint == 1],color='red',label='Buy',s=10,zorder=2)
            plt.scatter(df.index[sellPoint == 1],df['DR'][sellPoint == 1],color='green',label='Sell',s=10,zorder=2)
            plt.legend()
            plt.title(self.name + '\nDiscount Rate')
            # if save_path != '':
            #     if not os.path.exists(save_path):
            #         os.makedirs(save_path)
            #     plt.savefig(save_path + '/' + self.name + 'DR_transaction.png',dpi=600, bbox_inches='tight')
            plt.show()
        return value, psntValue, buyPoint, sellPoint
