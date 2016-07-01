#!/usr/bin/python3

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

    A test command for the smpi_gateway module.
'''

import os
import time
import sys

import zaltys_zwire
import zaltys_smpi_gateway

if len(sys.argv) != 4:
    print '''usage: zaltys_smpi_gateway_test <dspi_number> <address> <data>'''
    exit(1)

dspi    = int(sys.argv[1],0)
address = int(sys.argv[2],0)
wrdat   = int(sys.argv[3],0)

zwire = zaltys_zwire.ZwireSPI(dspi)
gateway = zaltys_smpi_gateway.ZwireSmpiGateway(zwire)

gateway.register_write(address, wrdat)
print 'WROTE: 0x{0:08x} : '.format(address), '0x{0:08x}'.format(wrdat)

time.sleep(1)

rddat = gateway.register_read(address)
print 'READ : 0x{0:08x} : '.format(address), '0x{0:08x}'.format(rddat)
