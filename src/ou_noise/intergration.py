from scipy.integrate import quad

from sympy import *
x = symbols('x')
def f(u):
    return u**(0.06/0.055-1)*exp(sqrt(2*0.055/(0.328**2))*(x-2.473)*u-u**2/2)
f_x,err = quad(f,0,oo)
def Df(u):
    return u**(0.06/0.055)*sqrt(2*0.055/(0.328**2))*exp(sqrt(2*0.055/(0.328**2))*(x-2.473)*u-u**2/2)
Df_x,err = quad(Df,0,oo)

b=solve(f_x-(x-0.5)*Df_x,x)
print(b)
