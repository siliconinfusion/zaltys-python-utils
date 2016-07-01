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

    A test for the Zaltys AD9361 driver wrapper.
'''

import os
import sys

import zwire
import smpi_gateway
import zaltys_ad9361_driver

zwire   = zwire.ZwireSPI(dspi=0)
gateway = smpi_gateway.ZwireSmpiGateway(zwire)
ad9361  = zaltys_ad9361_driver.ZaltysAD9361Driver(gateway, smpi2spi_base_address=0x00080000)

print("Initializing AD9361...\n")
ad9361.init_ad9361(interface="CMOS")
print("Done\n")

print("Writing configuration (sample_rate=61440000, tx_carrier_freq=1000000000, rx_carrier_freq=1000000000)...\n")
ad9361.set_ad9361_configuration(sample_rate=61440000, tx_carrier_freq=1000000000, rx_carrier_freq=1000000000)
print("Done\n")

print("Reading back configuration...")
config = ad9361.get_ad9361_configuration()
print "tx_sample_freq =", str(config[0])
print "rx_sample_freq =", str(config[1])
print "tx_rf_bandwidth =", str(config[2])
print "rx_rf_bandwidth =", str(config[3])
print "tx_lo_freq =", str(config[4])
print "rx_lo_freq =", str(config[5])
print "Done"
