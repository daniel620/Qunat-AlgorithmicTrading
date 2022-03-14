from ou_noise import ou
import numpy as np
import numpy
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv('src/OU过程/pingan60.csv')  # 包含H A的价格
Hprice = data.iloc[52562:53761,1]# 取H股价格  按周更新
Aprice = data.iloc[52562:53761,4] # 取A股价格
diff=Aprice-0.81*Hprice   # 价差（汇率折算） ---人民币  可以考虑ln
t = numpy.arange(0, 1199, 1)  # 时间长 拟合的时间段， 可以考虑滑动
print(t)
# exit()
plt.plot(t,diff)  #价差过程图
plt.show()
params = ou.mle(t,diff) #输出 回归速度，均值，波动率（方差）
print(type(params), params)
# res = pd.DataFrame(params)
# res.to_excel('src/OU过程/ou_result.xlsx')
