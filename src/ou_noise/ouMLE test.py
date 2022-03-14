from ou_noise import ou
import numpy as np
import numpy
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
data = pd.read_csv('E:/AHdata/000002.XSHE.csv')
x1 = data.iloc[1482:1607,6].values
y1 = data.iloc[1482:1607,7].values

X = sm.add_constant(x1)
result = (sm.OLS(y1,X)).fit()
x=y1-0.85*x1


t = numpy.arange(0, 125, 1)
plt.plot(t,x)
plt.show()

params = ou.mle(t, x)
print(params)