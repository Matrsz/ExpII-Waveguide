import pyvisa
rm = pyvisa.ResourceManager()
from time import sleep
import os

supply = rm.open_resource('USB0::0x1AB1::0x0641::DG4E163251532::INSTR')