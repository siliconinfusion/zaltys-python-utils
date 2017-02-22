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
##  Expose SMPI register read/write methods via a gateway object.
##  This extra level of indirection allows easily changing to alternative
##  access mechanisms (e.g. SPI or PCI).
##
##  Note SmpiGateway objects work with *register* addresses
##  (register_address = byte_address // 4).
##

class SmpiGateway(object):
    '''
        Coordinate accesses to/from SMPI bus registers
    '''
    def __init__(self):
        pass


class ZwireSmpiGateway(SmpiGateway):
    '''
    Coordinate access to SMPI registers via a Zwire interface object
    '''
    def __init__(self, zwire):
        self.zwire = zwire
        zwire.open()

    def close(self):
        self.zwire.close()

    def register_write(self, address, data):
        '''
        Write a single integer data value to a 32-bit register.
        '''
        self.zwire.write(address, data)

    def register_multi_write(self, address, data, sequential=False):
        '''
        Write a list of integer data values to 32-bit register(s).
        If sequential is true then increment the address for each write,
        otherwise keep the address constant (the default).
        Length of data should be less than 2**16.
        '''
        if sequential:
            self.zwire.seqWrite(address, data)
        else:
            self.zwire.rptWrite(address, data)

    def register_read(self, address):
        '''
        Read a single data value from a 32-bit register.  Return an integer.
        '''
        return self.zwire.read(address)

    def register_multi_read(self, address, count, sequential=False):
        '''
        Read multiple data values from 32-bit register(s).
        If sequential is true then increment the address for each read,
        otherwise keep the address constant (the default).
        Returns a list of integers.
        Length of data should be less than 2**16.
        '''
        if sequential:
            return self.zwire.seqRead(address, count)
        else:
            return self.zwire.rptRead(address, count)


class DummySmpiGateway(SmpiGateway):
    '''
        Fake access to SMPI registers
    '''
    def __init__(self):
        print("DummySmpiGateway __init__ ")

    def register_write(self, address, data):
        print("DummySmpiGateway write 0x{0:08x}".format(address) + " 0x{0:08x}".format(data))

    def register_multi_write(self, address, data, sequential=False):
        if sequential:
            print("DummySmpiGateway multi write seq 0x{0:08x}".format(address) + " {}".format(data))
        else:
            print("DummySmpiGateway multi write rpt 0x{0:08x}".format(address) + " {}".format(data))

    def register_read(self, address):
        print("DummySmpiGateway read  0x{0:08x}".format(address))
        return 0

    def register_multi_read(self, address, count, sequential=False):
        if sequential:
            print("DummySmpiGateway multi read seq  0x{0:08x}".format(address) + " {}".format(count))
        else:
            print("DummySmpiGateway multi read rpt  0x{0:08x}".format(address) + " {}".format(count))
        return [0]*count
