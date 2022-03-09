import usbtmc
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
from time import sleep


inst1 = usbtmc.Instrument(0x1ab1,0x0c94, "DM3O163050394")
inst2 = usbtmc.Instrument(0x1ab1,0x0c94, "DM3O163250415")

inst1.write(':FUNC:RES')
inst2.write(':FUNC:VOLT:DC')

ino = serial.Serial('/dev/ttyUSB0', 9600)
ino.reset_input_buffer()
ino.reset_output_buffer()

ino.write('a'.encode())

v = []
z = []

filename = 'corneta.csv'
file = open(filename, 'w', newline='')
writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

def rtoz(x):
    return 0.01273637345*x+5.230928738

time.sleep(5)

start = time.time()
while time.time()-start < 120:
    r_in = float(inst1.ask(':MEAS:RES?'))
    v_in = float(inst2.ask(':MEAS:VOLT:DC?'))
    z_in = rtoz(r_in)
    print(time.time() - start, z_in, v_in)
    writer.writerow([z_in, v_in])
    v.append(v_in)
    z.append(z_in)

plt.plot(z, v)
plt.show()