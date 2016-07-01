'''
    Author        : Paul Onions
    Creation date : 24 September 2015

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

    Test the Zaltys HDRM Demodulator driver wrapper.
'''

import os
import sys

import zwire
import smpi_gateway
import hdrmd_driver

zwire   = zwire.ZwireDummy()
gateway = smpi_gateway.ZwireSmpiGateway(zwire)
hdrmd   = zaltys_hdrmd_driver.ZaltysHdrmdDriver(gateway, base_address=0x00000400, sample_rate=125000000)

print('Configuring demodulator (modulation_scheme="QPSK", symbol_rate=1000000, rrc_alpha=20)...\n')
hdrmd.configure_demod(modulation_scheme="QPSK", symbol_rate=1000000, rrc_alpha=20)
print('Done\n')
