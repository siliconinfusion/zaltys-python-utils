'''
    Author        : Paul Onions
    Creation date : 16 December 2015

    COMMERCIAL IN CONFIDENCE
    (C) 2015 - 2016 Silicon Infusion Limited

    Silicon Infusion Limited                 
    CP House
    Otterspool Way
    Watford WD25 8HP
    Hertfordshire, UK
    Tel: +44 (0)1923 650404
    Fax: +44 (0)1923 650374
    Web: www.siliconinfusion.com

    This is an unpublished work the copyright of which vests in Silicon Infusion
    Limited. All rights reserved. The information contained herein is the
    property of Silicon Infusion Limited and is supplied without liability for
    errors or omissions. No part may be reproduced or used except as authorised
    by contract or other written permission. The copyright and the foregoing
    restriction on reproduction and use extend to all media in which the
    information may be embodied.

    Expose SMPI register read/write methods via a gateway object.
    Allow alternative access mechanisms to the SMPI bus (e.g. SPI or PCI).
'''

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
