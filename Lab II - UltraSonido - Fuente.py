import pyvisa
rm = pyvisa.ResourceManager()
from time import sleep
import os

supply = rm.open_resource('USB0::0x1AB1::0x0641::DG4E163251532::INSTR')

#supply.write(':OUTPut OFF')
supply.write(':APPLy:SIN 38900,20,0,0')
#supply.write(':PULSe:DCYCle 10')

# medicion cada 2 grados, distancia de los tubitos = 8 cm
# d = 35.5 cm (-8)
# v = 19 vpp
# f = 39.1 kHz

for i in range(10):
    supply.write(':OUTPut ON')
    sleep(0.05)
    supply.write(':OUTPut OFF')
    sleep(0.05) 
    
