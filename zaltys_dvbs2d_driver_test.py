##
##  Author        : Paul Onions
##  Creation date : 19 February 2018
##
##  Copyright 2018 Silicon Infusion Limited
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
##  Test the Zaltys DVB-S2 Demodulator driver wrapper.
##
##  Invoke at a shell prompt with:-
##    python zaltys_dvbs2d_driver_test.py
##

import os
import sys

import zaltys_smpi_gateway
import zaltys_dvbs2d_driver

gateway = zaltys_smpi_gateway.DummySmpiGateway()
dvbs2d  = zaltys_dvbs2d_driver.Dvbs2dDriver(gateway, base_address=0x00000400)

dvbs2d.sample_rate = 125e6
dvbs2d.symbol_rate = 10e6
dvbs2d.configure_demod()
