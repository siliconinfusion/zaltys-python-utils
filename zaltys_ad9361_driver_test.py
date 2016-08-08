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
##  A test for the Zaltys AD9361 driver wrapper.
##
##  Invoke at a shell prompt with:-
##    python3 zaltys_ad9361_driver_test.py
##

import os
import sys

import zaltys_zwire
import zaltys_smpi_gateway
import zaltys_ad9361_driver

zwire   = zaltys_zwire.ZwireSPI(dspi=0)
gateway = zaltys_smpi_gateway.ZwireSmpiGateway(zwire)
ad9361  = zaltys_ad9361_driver.AD9361Driver(gateway, smpi2spi_base_address=0x00080000)

print("Initializing AD9361...\n")
ad9361.init_ad9361(interface="LVDS")
print("Done\n")

print("Writing configuration (sample_rate=100000000, tx_carrier_freq=1000000000, rx_carrier_freq=1000000000)...\n")
ad9361.set_ad9361_configuration(sample_rate=100000000, tx_carrier_freq=1000000000, rx_carrier_freq=1000000000)
print("Done\n")

print("Reading back configuration...")
config = ad9361.get_ad9361_configuration()
print("tx_sample_freq =", str(config[0]))
print("rx_sample_freq =", str(config[1]))
print("tx_rf_bandwidth =", str(config[2]))
print("rx_rf_bandwidth =", str(config[3]))
print("tx_lo_freq =", str(config[4]))
print("rx_lo_freq =", str(config[5]))
print("Done")
