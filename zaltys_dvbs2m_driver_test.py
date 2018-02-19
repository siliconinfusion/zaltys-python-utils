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
##  Test the Zaltys DVB-S2 Baseband Modulator driver wrapper.
##
##  Invoke at a shell prompt with:-
##    python zaltys_dvbs2m_driver_test.py
##

import zaltys_smpi_gateway
import zaltys_dvbs2m_driver

gateway = zaltys_smpi_gateway.DummySmpiGateway()
dvbs2m  = zaltys_dvbs2m_driver.Dvbs2mDriver(gateway, base_address=0x00001000)

dvbs2m.sample_rate = 125e6
dvbs2m.symbol_rate = 10e6
dvbs2m.configure_mod()
