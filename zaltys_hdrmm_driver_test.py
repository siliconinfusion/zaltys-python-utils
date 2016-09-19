##
##  Author        : Paul Onions
##  Creation date : 19 September 2016
##
##  Copyright 2016 Silicon Infusion Limited
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
##  Test the Zaltys HDRM Modulator driver wrapper.
##
##  Invoke at a shell prompt with:-
##    python zaltys_hdrmm_driver_test.py
##

import os
import sys

import zaltys_smpi_gateway
import zaltys_hdrmm_driver

gateway = zaltys_smpi_gateway.DummySmpiGateway()
hdrmm   = zaltys_hdrmm_driver.HdrmmDriver(gateway, base_address=0x00001000)

hdrmm.select_constellation_map(modulation_scheme="16QAM", map_scheme="IESS")
hdrmm.sample_rate = 125e6
hdrmm.symbol_rate = 10e6
hdrmm.configure_mod()
