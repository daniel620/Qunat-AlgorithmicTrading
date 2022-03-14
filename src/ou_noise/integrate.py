import sympy
from sympy import *

x = sympy.symbols('x')
u = sympy.symbols('u')
f = integrate(u**(0.06/0.055-1)*exp(sqrt(2*0.055/(0.328**2))*(x-2.473)*u-u**2/2),(u,0,oo))
df = integrate(u**(0.06/0.055)*sqrt(2*0.055/(0.328**2))*exp(sqrt(2*0.055/(0.328**2))*(x-2.473)*u-u**2/2),(u,0,oo))

b = sympy.nsolve(f-(x-0.5)*df,0)

print(b)
