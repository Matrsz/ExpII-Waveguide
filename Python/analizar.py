import numpy as np
import csv
import matplotlib.pyplot as plt

from scipy.signal import find_peaks

import scipy.optimize


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
    guess = np.array([2.*np.pi*guess_freq, 0.1])

    def sinfunc(t, w, p):  return -A * np.cos(w*t - p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    w, p= popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t - p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

def sort_arrays(z, v):
    args = z.argsort()
    return [z[args], v[args]]


data2 = np.genfromtxt('corneta_relento.csv', delimiter=' ')
z2, v2 = sort_arrays(data2[:,0], data2[:, 1])

z2 = z2 + 0.5958336695473103

params = fit_sin(z2, v2)
print(params)
z0 = np.linspace(-1, 19, 10000)
#z0 = z2


vmax = (params["offset"]+params["amp"])
vmin = (params["offset"]-params["amp"])
lg = 2/params["freq"]

delta = (params["phase"]/params["omega"])

print(f"vmax: {vmax*1e3}\n vmin: {vmin*1e3}\n lambda: {lg}\n delta: {delta}\n delta/lg = {delta/lg}")

roe = vmax/vmin
gamma_abs = (roe-1)/(roe+1)

Zv = 376.73
co = 299792458*100
f = 10.53e9
Zo = Zv/co*f*lg

print(f"roe: {roe}\n Zo = {Zo}")

x = -params["amp"]*np.cos(params["omega"]*z0-params["phase"])+params["offset"]
plt.plot(z2, v2, z0, x, 'b:', z0, x*0+params["offset"], '--k')
plt.plot([0, 0], [0, vmax], 'k', [delta, delta], [0, vmax], '--k')
plt.gca().invert_xaxis()
plt.show()

