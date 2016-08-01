##
##  Author        : Paul Onions
##  Creation date : 24 September 2015
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
##  Test the Zaltys HDRM Demodulator driver wrapper.
##
##  Invoke at a shell prompt with:-
##    python3 zaltys_hdrmd_driver_test.py
##

import os
import sys

import zaltys_zwire
import zaltys_smpi_gateway
import zaltys_hdrmd_driver

zwire   = zaltys_zwire.ZwireDummy()
gateway = zaltys_smpi_gateway.ZwireSmpiGateway(zwire)
hdrmd   = zaltys_hdrmd_driver.HdrmdDriver(gateway, base_address=0x00000400, sample_rate=125000000)

print('Configuring demodulator (modulation_scheme="QPSK", symbol_rate=1000000, rrc_alpha=20)...\n')
hdrmd.configure_demod(modulation_scheme="QPSK", symbol_rate=1000000, rrc_alpha=20)
print('Done\n')
