import pyvisa
import numpy as np
import time
import matplotlib.pyplot as plt
rm = pyvisa.ResourceManager()


MULT1 = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O163050394::INSTR')
#MULT2 = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O163250415::INSTR')

MULT1.write(':FUNC:RES')
#MULT2.write(':FUNC:VOLT:DC')

Volts = []
Resist = []
Seconds = []
start = time.time()
while time.time() - start < 90:
    v = MULT1.query(':MEASure:RES?')
    Resist.append(float(v))
    Seconds.append(time.time() - start)
    print(v)



MaxResist, MinResist = np.max(Resist), np.min(Resist)
m = 10.5/(MaxResist-MinResist)
zo = -m*MinResist

def distancia(r, m, zo):
    return m*r+zo

print(m, zo, distancia(MinResist, m ,zo), distancia(MaxResist, m, zo))

#0.012909824848840706 -3.2725556525336135 0.0 10.500000000000002
#USB0::0x1AB1::0x0C94::DM3O163250415::INSTR 
#USB0::0x1AB1::0x0C94::DM3O163050394::INSTR