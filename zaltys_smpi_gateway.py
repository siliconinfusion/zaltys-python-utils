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

import time

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

    def __del__(self):
        self.zwire.close()

    def register_write(self, address, data):
        self.zwire.write(address, data)

    def register_read(self, address):
        rdata = self.zwire.read(address)
        return rdata


class DummySmpiGateway(SmpiGateway):
    '''
        Fake access to SMPI registers
    '''
    def __init__(self):
        print("DummySmpiGateway __init__ ")

    def register_write(self, address, data):
        print("DummySmpiGateway write 0x{0:08x}".format(address) + " 0x{0:08x}".format(data))

    def register_read(self, address):
        print("DummySmpiGateway read  0x{0:08x}".format(address))
        return 0
