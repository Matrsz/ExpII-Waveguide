#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 03:37:26 2020

@author: inox
"""

#Lab DRP library for Rigol instruments management

import os        # for USB test and meassurement control

debug = 0
#GENID=0x00a1

class Multi():
    """
    Base class for a Rigol USB Spectrum Analyzer.
    """

    id_vendor = 0x1ab1
    id_product = None

    def __init__(self, port):
#        if self.id_product is None:
#            raise ValueError('id_product not defined')
        # find our device
        #self.dev = usbtmc.Instrument(idVendor=self.id_vendor,idProduct=self.id_product)
        self.dev = os.open(port,os.O_RDWR)  # "/dev/usbtmc0" o "/dev/usbtmc1"

        # was it found?
        if self.dev is None:
           raise ValueError('Device not found')
    
    def setResistance(self):
        cmd = "FUNC:RES".encode()
        os.write(self.dev, cmd)
        return
    
    def setVoltDC(self):
        cmd = "FUNC:VOLT:DC".encode()
        os.write(self.dev, cmd)
        return
    
    def getVoltDC(self):
        cmd = "MEAS:VOLT:DC?".encode()
        os.write(self.dev, cmd)
        return os.read(self.dev, 20)
    
    def getResistance(self):
        cmd = "MEAS:RES?".encode()
        os.write(self.dev, cmd)
        return os.read(self.dev, 20)


class SpAn():
    """
    Base class for a Rigol USB Spectrum Analyzer.
    """

    id_vendor = 0x1ab1
    id_product = None

    def __init__(self):
#        if self.id_product is None:
#            raise ValueError('id_product not defined')
        # find our device
        #self.dev = usbtmc.Instrument(idVendor=self.id_vendor,idProduct=self.id_product)
        self.dev = os.open("/dev/usbtmc0",os.O_RDWR) 

        # was it found?
        if self.dev is None:
           raise ValueError('Device not found')
           
    def setRefLevel(self, level):
        cmd = (":DISP:WIN:TRAC:Y:RLEVEL "+str(level)).encode()
        os.write(self.dev, cmd)
        return self.getRefLevel()
    
    def getRefLevel(self):
        cmd = ":DISP:WIN:TRAC:Y:RLEV?".encode()
        os.write(self.dev, cmd)
        return os.read(self.dev, 20)
    
#    def getPeakTable(self):
#       cmd = ":TRACe:MATH:PEAK:DATA?".encode()
#        os.write(self.dev, cmd)
#        return os.read(self.dev, 20)
        
    def initPeakTable(self):
        cmd = ":TRACe:MATH:PEAK:TABLe:STATe ON".encode()
        os.write(self.dev, cmd)
        cmd = ":TRACe:MATH:PEAK:SORT FREQ".encode()
        os.write(self.dev, cmd)
        return #self.getPeakTable()
    
    def setFreqCenter(self, freq):
        cmd = ("FREQ:CENT "+str(freq)).encode()
        os.write(self.dev, cmd)
        return
    
    def setSpan(self, span):
        cmd = ("FREQ:SPAN" + str(span)).encode()
        os.write(self.dev, cmd)
        return
    
    def setSpanFull(self):
        cmd = ":FREQuency:SPAN:FULL".encode()
        os.write(self.dev, cmd)
        return
    
    def getMarkAmp(self, n):
        cmd = (":CALC:MARK"+str(n)+":Y?").encode();
        os.write(self.dev, cmd)
        return os.read(self.dev, 20)
    
    def setMarkFreq(self, n, freq):
        cmd = (":CALC:MARK"+str(n)+":X " +str(freq)).encode();
        os.write(self.dev, cmd)
        return self.getMarkFreq(n)
    
    def getMarkFreq(self, n):
        cmd = (":CALC:MARK"+str(n)+":X?").encode();
        os.write(self.dev, cmd)
        return os.read(self.dev, 20)
    
    def findPeak(self):
        cmd = ":CALC:MARK1:PEAK:SEARCH:MODE MAX".encode();
        os.write(self.dev, cmd)
        cmd = ":CALC:MARK1:PEAK:MAX:MAX".encode();
        os.write(self.dev, cmd)
        return self.getMarkFreq(1)
