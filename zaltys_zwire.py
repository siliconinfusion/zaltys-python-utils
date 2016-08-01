##
##  Author        : Paul Onions
##  Creation date : 16 December 2015
##
##  Copyright 2015 - 2016 Silicon Infusion Limited
##
##  Silicon Infusion Limited                 
##  CP House
##  Otterspool Way
##  Watford WD25 8HP
##  Hertfordshire, UK
##  Tel: +44 (0)1923 650404
##  Fax: +44 (0)1923 650374
##  Web: www.siliconinfusion.com
##
##  Licence: MIT, see LICENCE file for details.
##

##
##  Interfaces to C SPI functions in /usr/lib/libzaltys-zwire.so
##

import os
import ctypes


class Zwire(object):
    '''
        Base class for Zwire SPI/other serial interfaces
    '''
    def __init__(self):
        pass

        
class ZwireSPI(Zwire):
    '''
        Interface to ZwireSPI library functions
    '''
    def __init__(self, dspi=0):
        '''
            Initialises .so library
        '''
        self.bus = 'SPI'
        self.dspi=dspi
        self.lib = ctypes.CDLL('/usr/lib/libzaltys-zwire.so')
       
    def open(self):
        '''
            Opens the sysfs device file for the SPI device.
            Class variable fd set to the returned file descriptor (fd).
            Assumes dspi class variable already set
        '''
        self.fd = self.lib.zwspiOpen(ctypes.c_int(self.dspi))
                
    def read(self, _addr):
        '''
            Read a single value at _addr using SPI bus.  Return value read.
        '''
        longArray = ctypes.c_ulong * 1
        data = longArray(0)
        if self.fd != -1:
            val = self.lib.zwspiRead(ctypes.c_int(self.fd), ctypes.c_ulong(_addr), ctypes.c_ushort(1), data)
        return data[0]
        
    def seqRead(self, _addr, _count):
        '''
            Read multiple values from _addr using SPI bus.  Return list of values read.
        '''
        longArray = ctypes.c_ulong * _count
        data = longArray(0)
        if self.fd != -1:
            val = self.lib.zwspiSeqRead(ctypes.c_int(self.fd), ctypes.c_ulong(_addr), ctypes.c_ushort(_count), data)
        return data
    
    def write(self, _addr, _data):
        '''
            Write a single value, _data, to _addr using SPI bus.
        '''
        longArray = ctypes.c_ulong * 1
        data = longArray(_data)
        if self.fd != -1:
            val = self.lib.zwspiWrite(ctypes.c_int(self.fd), ctypes.c_ulong(_addr), ctypes.c_ushort(1), data)
        return val
        
    def seqWrite(self, _addr, _data):
        '''
            Write a list of values, _data, to _addr using SPI bus.
        '''
        ret = []
        longArray = ctypes.c_ulong * len(_data)
        data = longArray(0)
        for n in range(0, len(_data)):
            data[n] = ctypes.c_uint(_data[n])
        if self.fd != -1:
            val = self.lib.zwspiSeqWrite(ctypes.c_int(self.fd), ctypes.c_ulong(_addr), ctypes.c_ushort(len(_data)), data)
        return val
        
    def close(self):
        '''
            Closes the sysfs device file for the SPI device
        '''
        self.lib.zwspiClose(ctypes.c_int(self.fd))


class ZwireDummy(Zwire):
    '''
        A dummy Zwire interface for development purposes
    '''
    def __init__(self, dspi=0):
        '''
            Initialise
        '''
        print("ZwireDummy __init__ " + str(dspi))
        self.bus = 'Dummy'
        self.dspi=dspi

    def open(self):
        '''
            Do nothing
        '''
        print("ZwireDummy open")
                
    def read(self, _addr):
        '''
            Pretend to read the single value at _addr.  Return the value read.
        '''
        print("ZwireDummy read " + str(_addr))
        return 0
        
    def seqRead(self, _addr, _count):
        '''
            Pretend to read multiple values from _addr.  Return a list of values read.
        '''
        print("ZwireDummy SeqRead " + str(_addr) + " " + str(_count))
        ret = []
        for n in range(0, _count):
            ret.append(0)
        return ret
    
    def write(self, _addr, _data):
        '''
            Pretend to write a single value, _data, to _addr.
        '''
        print("ZwireDummy write " + str(_addr) + " " + str(_data))
        return 0
        
    def seqWrite(self, _addr, _data):
        '''
            Pretend to write a list of values, _data, to _addr.
        '''
        print("ZwireDummy seqWrite " + str(_addr) + " " + str(_data))
        return 0
        
    def close(self):
        '''
            Do nothing
        '''
        print("ZwireDummy close")

