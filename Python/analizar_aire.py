from operator import mod
import numpy as np
import csv
import matplotlib.pyplot as plt

import uncertainties as uc
import uncertainties.umath as um

from scipy.signal import find_peaks

import scipy.optimize

plt.rcParams['font.size'] = '14'

def freqfase(z, v):
    plt.plot(z, v)
    plt.show()
    N = len(z)
    Ts = (max(z)-min(z))/len(z)
    print(Ts)
    k = np.fft.fftfreq(N, Ts)[1:int(N/2)]
    V = np.fft.fft(v)[1:int(N/2)]
    plt.plot(k, np.real(V), k, np.imag(V))
    plt.show()
    nmax = np.argmax(np.abs(V))
    k0 = k[nmax]*2*np.pi
    fase = -np.angle(V[nmax])
    return [k0, fase]


def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])  
    guess_freq = 0.5 # excluding the zero frequency "peak", which is related to offset
    A = (max(yy)-min(yy))/2
    c = (max(yy)+min(yy))/2
    guess = np.array([2.*np.pi*guess_freq, 0., A, c])

    def sinfunc(t, w, p, A, c):  return -A * np.cos(w*t - p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    w, p, A, c= popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t - p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "cov": pcov, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

#def sort_arrays(z, v):
#    args = z.argsort()
#    return [z[args], v[args]]


data2 = np.genfromtxt('sistema_desadaptado2.csv', delimiter=' ')
#data3 = np.genfromtxt('sistema_adaptado2.csv', delimiter=' ')
#z2, v2, s2 = data2[:,0], data2[:, 1], data2[:, 3]
x, v, s = data2[:,0], data2[:, 1], data2[:, 3]
#x2, v2, s2 = data3[:,0], data3[:, 1], data3[:, 3]
#z3, v3 = sort_arrays(data3[:,0], data3[:, 1])

v = v*1000
x = x + 0.5958336695473103-0.055836036880428416-0.5706994355396638


params = fit_sin(x, v)  #Fitea la curva de V(x)

print(params)
x0 = np.linspace(-1, 19, 10000)
#z0 = z2


vmax = (params["offset"]+params["amp"])
vmin = (params["offset"]-params["amp"])

lg = 2/params["freq"] #Longitud de onda en la guía

delta = params["phase"]/(2*np.pi)*lg/2 #Desviación respecto al plano de carga

print(f"vmax: {vmax*1e3} \nvmin: {vmin*1e3} \nlambda: {lg} \ndelta: {delta} \ndelta/lg = {delta/lg}")

roe = vmax/vmin

Zv = 376.73        #Impedancia intrínseca del espacio libre
co = 299792458*100 #Velocidad de la luz en cm/s
f = 10.53e9        #Frecuencia de emisión del diodo Gunn
Zo = Zv/co*f*lg

print(f"roe: {roe} \nZo = {Zo}")

mod_gamma = (roe - 1)/(roe + 1)
fase_gamma = -params["phase"]+np.pi
gamma = mod_gamma * np.exp(1j*fase_gamma)  #Coeficiente de reflexión

zl = (1+gamma)/(1-gamma)
Zl = zl*Zo

print(f"coef reflexion: {gamma} = {mod_gamma}*exp({fase_gamma}j) \nzL = {zl} = {np.abs(zl)}*exp({np.angle(zl)}j)\nyL = {1/zl} = {np.abs(1/zl)}*exp({np.angle(1/zl)}j)")


v_fit = -params["amp"]*np.cos(params["omega"]*x0-params["phase"])+params["offset"]

plt.plot(x, v)
plt.plot(x0, v_fit, 'b:')
plt.xlim([min(x0), max(x0)])
#plt.plot(z3, v3)
plt.plot([0, 0], [0, vmax], 'k', [delta, delta], [0, vmax], '--k')
plt.xlabel("x [cm]")
plt.ylabel("V [mV]")
plt.title("Antena de Bocina")
plt.legend(["Señal Medida", "Proyección"], loc='lower left')
plt.gca().invert_xaxis()
plt.tight_layout()
plt.show()

z = (Zl+1j*Zo*np.tan(2*np.pi*x0/lg))/(Zo+1j*Zl*np.tan(2*np.pi*x0/lg))
z = np.divide(1+gamma*np.exp(-1j*params["omega"]*x0), 1-gamma*np.exp(-1j*params["omega"]*x0))
y = 1./z


rg, xg = np.real(z), np.imag(z)
gg, bg = np.real(y), np.imag(y)

#indexC = np.nonzero([z if 0.99 < np.real(y) < 1.01 and np.imag(y) < 0 else 0 for z, y in zip(x0, yg)])[0][0]
#indexL = np.nonzero([z if 0.99 < np.real(y) < 1.01 and np.imag(y) > 0 else 0 for z, y in zip(x0, yg)])[0][0]

eps = 0.01
indices = range(len(x0))
indexC = list(filter(lambda i: 1-eps < np.real(y[i]) < 1+eps and np.imag(y[i]) < 0, indices))

l = x0[indexC]
y_a = np.conj(y[indexC])

#z_L = x0[indexL]
#y_L = np.conj(yg[indexL])

#axs[0].plot(x0, np.real(zg), x0, np.imag(zg), 'b', x0, x0*0+1, '--k')
#axs[0].plot([0, 0], [min(xg), max(rg)], 'k')
#
#axs[1].plot(x0, np.real(yg), x0, np.imag(yg), 'b', x0, x0*0+1, '--k')
#axs[1].plot([0, 0], [min(bg), max(gg)], 'k')

fig, axs = plt.subplots(2,1, sharex=True)

axs[0].plot(x0, np.real(y), x0, x0*0+1, ':k')
axs[1].plot(x0, np.imag(y), x0, x0*0, ':k')
axs[1].set_xlim([-0.01, max(x0)])

for i in indexC:
    print(f"ell = {x0[i]} \ny_a = {y[i]}")
    axs[0].plot([x0[i], x0[i]], [0, max(gg)*1.1], '--b')
    axs[1].plot([x0[i], x0[i]], [min(bg)*1.1, max(bg)*1.1], '--b')

axs[0].plot([0, 0], [-0.1, max(gg)*1.1], 'k')
axs[1].plot([0, 0], [min(bg)*1.1, max(bg)*1.1], 'k')
axs[0].set_ylim([-0.1, max(gg)*1.1])
axs[1].set_ylim([min(bg)*1.1, max(bg)*1.1])

axs[0].set_title("Admitancia Normalizada: y=g+jb")
axs[0].legend(["g", "1", "ℓ"], loc='upper left')
axs[1].legend(["b", "0", "ℓ"], loc='upper left')
axs[1].set_xlabel("x [cm]")
axs[1].invert_xaxis()
plt.show()


#for i in range(10):
#    z_adapL = z_L+i*lg/2
#    z_adapC = z_C+i*lg/2
#    axs[0].plot([z_adapL, z_adapL], [min(xg), max(rg)], ':b')
#    axs[1].plot([z_adapL, z_adapL], [min(bg), max(gg)], ':b')
#    print(f"Pos. adaptador: {z_adapL} cm = {z_adapL/lg} lg - y Adaptador: {y_L}")
#    axs[0].plot([z_adapC, z_adapC], [min(xg), max(rg)], ':r')
#    axs[1].plot([z_adapC, z_adapC], [min(bg), max(gg)], ':r')
#    print(f"Pos. adaptador: {z_adapC} cm = {z_adapC/lg} lg - y Adaptador: {y_C}")


w_err, p_err, A_err, c_err = np.sqrt(np.diag(params["cov"]))
print("w err = ", np.sqrt(np.diag(params["cov"])[0]))

f = uc.ufloat(params["freq"], w_err)
lg = 2/f
f = uc.ufloat(10.53e9, 0.05e9)

A = uc.ufloat(params["amp"], A_err*2)
c = uc.ufloat(params["offset"], c_err)
p = uc.ufloat(params["phase"], p_err)

vmax = c+A
vmin = c-A

Zo = Zv/co*f*lg

roe = vmax/vmin

delta = p/(2*np.pi)*lg/2


mod_gamma = (roe - 1)/(roe + 1)
fase_gamma = -p+np.pi
print(mod_gamma, fase_gamma)
re_gamma = mod_gamma*um.cos(fase_gamma) 
im_gamma = mod_gamma*um.sin(fase_gamma)

a = 1+re_gamma
b = im_gamma
c = 1-re_gamma
d = -im_gamma

Zo = uc.ufloat(562, 3)
rl = (a*c+b*d)/(c**2+d**2)*Zo
xl = (b*c-a*d)/(c**2+d**2)*Zo  #Coeficiente de reflexión


#zl = (1+gamma)/(1-gamma)
#Zl = zl*Zo


print(f"lambda = {lg} \nZo = {Zo} \nROE = {roe} \ndelta = {delta/lg} lg, \nRL = {rl}\nXL= {xl}")