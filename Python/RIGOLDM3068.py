import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
rm = pyvisa.ResourceManager()


MULT1 = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O163050394::INSTR')
MULT2 = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O163250415::INSTR')

MULT1.write(':FUNC:VOLT:DC')
MULT2.write(':FUNC:VOLT:DC')

Volts = []
Resist = []
Seconds = []
for i in range(1, 10, 1):
    v = MULT1.query(':MEASure:VOLT:DC?')
    Volts.append(float(v))
    Seconds.append(i)
    sleep(0.5)
    print(v)

for i in range(1, 10, 1):
    r = MULT2.query(':MEASure:VOLT:DC?') 
    Resist.append(r)
    sleep(0.5)
    print(r)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(Volts, Seconds, "bo")
plt.show()


#USB0::0x1AB1::0x0C94::DM3O163250415::INSTR 
#USB0::0x1AB1::0x0C94::DM3O163050394::INSTR