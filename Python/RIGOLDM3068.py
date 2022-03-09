import pyvisa
import serial
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
rm = pyvisa.highlevel.ResourceManager()


resources = rm.list_resources()
print(resources)

MULT1 = rm.open_resource("USB0::6833::3220::DM3O163250415::0::INSTR")
MULT2 = rm.open_resource("USB0::6833::3220::DM3O163050394::0::INSTR")

MULT1.write(':FUNC:RES')
MULT2.write(':FUNC:VOLT:DC')

ino = serial.Serial('/dev/ttyUSB0', 9600)
ino.reset_input_buffer()
ino.reset_output_buffer()

ino.write('a'.encode())

v = []
z = []

def z(r):
    0.1291*r-3.272

while ino.read() != 'L':
    r_in = MULT1.query(':MEAS:RES?')
    v_in = MULT2.query(':MEAS:VOLT:DC?')
    v.append(float(v_in))
    z.append(z(float(r_in)))
    print(v)

ino.write('s'.encode)

plt.plot()
plt.show()
