import usbtmc
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
from time import sleep


inst1 = usbtmc.Instrument(0x1ab1,0x0c94, "DM3O163050394")
inst2 = usbtmc.Instrument(0x1ab1,0x0c94, "DM3O163250415")
inst3 = usbtmc.Instrument(0x1ab1,0x0c94, "DM3O163050385")

inst1.write(':FUNC:RES')
inst2.write(':FUNC:VOLT:DC')
inst3.write(':FUNC:VOLT:DC')

ino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1e-8)
ino.reset_input_buffer()
ino.reset_output_buffer()

ino.write('a'.encode())

v = []
z = []

filename = 'sistema_desadaptado.csv'
file = open(filename, 'w', newline='')
writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

def rtoz(x):
    return 0.01273637345*x+5.230928738

start = False
finish = False

i = 0
while not(finish):
    reading = ino.read_until('\n')
    if reading != b'':
        print(reading)
        
    if reading == b'R\r\n' or reading == b'L\r\n' or reading == b'L' or reading == b'R':
        i += 1
        print(i)
        if i == 1:
            start = True
        if i == 2:
            finish = True

    if start:
        r_in = float(inst1.ask(':MEAS:RES?'))
        v_in = float(inst2.ask(':MEAS:VOLT:DC?'))
        s_in = float(inst3.ask(':MEAS:VOLT:DC?'))
        z_in = rtoz(r_in)
        print(z_in, v_in, s_in, start, finish)
        writer.writerow([z_in, v_in, r_in, s_in])
        v.append(v_in)
        z.append(z_in)

time.sleep(5)
ino.write('s'.encode())

plt.plot(z, v)
plt.show()

