#
# Author        : Paul Onions
# Creation date : 16 December 2015
#
# Copyright 2015 - 2016 Silicon Infusion Limited
#
# Silicon Infusion Limited                 
# CP House
# Otterspool Way
# Watford WD25 8HP
# Hertfordshire, UK
# Tel: +44 (0)1923 650404
# Fax: +44 (0)1923 650374
# Web: www.siliconinfusion.com
#
# Licence: MIT, see LICENCE file for details.
#

#
# Running Zwire protocol over SPI and UART links.
#
# SPI routines interface to C SPI functions in libzaltys-zwire.so
#

import ctypes
import ctypes.util
import serial


#
# Zwire base class
#
class Zwire(object):
    '''
        Base class for Zwire SPI/other serial interfaces
    '''
    def __init__(self):
        pass


#
# Zwire over SPI
#        
class ZwireSPI(Zwire):
    '''
        Interface to ZwireSPI library functions
    '''
    def __init__(self, dspi=0, libzaltys_zwire_path=None):
        '''
            Initialises .so library
        '''
        self.bus  = 'SPI'
        self.dspi = dspi

        if libzaltys_zwire_path:
            self.libzaltys_zwire_path = libzaltys_zwire_path
        else:
            self.libzaltys_zwire_path = ctypes.util.find_library("libzaltys-zwire.so")

        self.lib = ctypes.CDLL(self.libzaltys_zwire_path)
       
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


#
# Zwire over UART
#
# Note: for legacy compatibility reasons, the manner in which commands
# and data values are encoded and transported over the serial link are
# somewhat unusual.
#
class ZwireUART(Zwire):
    '''
        Zwire protocol over a UART serial line
    '''
    def __init__(self, port, baud=115200):
        self.CMD_GETVER   = "$00"    # Read software ID & revision
        self.CMD_SETEEP   = "$01"    # Write EEPROM data
        self.CMD_GETEEP   = "$02"    # Read EEPROM data
        self.CMD_SETBAUD  = "$03"    # Set Serial / USB BAUD rate
        self.CMD_CFGFPGA  = "$04"    # Configure FPGA
        self.CMD_GETRFPGA = "$05"    # Read FPGA SPI locations repetitively
        self.CMD_GETSFPGA = "$06"    # Read FPGA SPI locations sequentially
        self.CMD_SETRFPGA = "$07"    # Write FPGA SPI locations repetitively
        self.CMD_SETSFPGA = "$08"    # Write FPGA SPI locations sequentially

        self.port = port
        self.baud = baud

    def open(self):
        '''
            Open serial connection.  Return an 18-character version string
            obtained from the remote endpoint.
        '''
        self.uart = serial.Serial(self.port, self.baud, timeout=1, writeTimeout=1)
        self.uart.flushInput()
        cmd = self.appendCmdChkSum(self.CMD_GETVER)
        self.uart.write(bytes(cmd, encoding='ascii'))

        # read the 18-byte response
        response = ""
        for n in range(18):
            byte = self.uart.read()
            response = response + byte.decode('ascii')
        return response

    def appendCmdChkSum(self, cmd):
        check_sum = 0
        for character in cmd:
            check_sum = check_sum + ord(character)              
        check_sum = check_sum % 256
        full_cmd = cmd + ":" + hex(check_sum)[2:].zfill(2)
        return full_cmd
        
    def read(self, address):
        '''
            Read integer value from 32-bit register.
        '''
        self.uart.flushInput()
        count = 1
        cmd = self.appendCmdChkSum(self.CMD_GETRFPGA + hex(address)[2:].zfill(8) + hex(count)[2:].zfill(4))
        self.uart.write(bytes(cmd, encoding='ascii'))

        # read the 4-byte response
        response = [0]*4
        for n in range(4):
            response[n] = self.uart.read()[0]
        
        return response[0]*2**24 + response[1]*2**16 + response[2]*2**8 + response[3]

    def write(self, address, data):
        '''
            Write integer data value to 32-bit register.
        '''
        self.uart.flushInput()
        count = 1
        cmd = self.appendCmdChkSum(self.CMD_SETRFPGA + hex(address)[2:].zfill(8) + hex(count)[2:].zfill(4))
        byts = [0]*4
        byts[0] = (data // 2**24) % 256
        byts[1] = (data // 2**16) % 256
        byts[2] = (data // 2**8) % 256
        byts[3] = data % 256
        self.uart.write(bytes(cmd, encoding='ascii'))
        self.uart.write(bytearray(byts))

    def close(self):
        '''
            Close serial connection.
        '''
        self.uart.close()


#
# A dummy Zwire connection for test purposes
#
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

