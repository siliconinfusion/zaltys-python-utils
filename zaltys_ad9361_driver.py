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
##  A wrapper for the Zaltys AD9361 driver (libzaltys-ad9361.so).
##

import ctypes

#
# Callback functions (called from libzaltys-ad9361 C code)
#
# The following variables and functions need to be module functions,
# not class attributes/methods.  This is because a class method
# invoked from C has no notion of self, so cannot find other methods
# or attributes.
#
g_smpi_gateway = None

g_smpi2spi_base_address = 0

g_lib = None

g_rf_phy = None

def spi_init(device_id, clk_pha, clk_pol):
    return 0

def spi_read(bytes_number):
    return 0

def spi_write_then_read(txbuf, n_tx, n_rx):
    global g_lib, g_smpi_gateway, g_smpi2spi_base_address

    if n_tx == 2:
        # Perform a read
        if n_rx >= 1 and n_rx <= 8:
            nbi = n_rx - 1
            cmd_addr = (nbi/4)*2**28 + 2**27 + (nbi%4)*2**25 + 2**24 + txbuf[0]*2**8 + txbuf[1]
            wait_for_spi_ready()
            g_smpi_gateway.register_write(g_smpi2spi_base_address, cmd_addr)
            wait_for_spi_ready()
            dat_hi = g_smpi_gateway.register_read(g_smpi2spi_base_address+5)
            dat_lo = g_smpi_gateway.register_read(g_smpi2spi_base_address+2)
            dat = dat_hi*2**32 + dat_lo
            for n in range(n_rx):
                g_lib.ad9361_write_rxbuf(ctypes.c_ubyte((dat >> (8*(n_rx-1-n))) & 0xFF), ctypes.c_uint(n))

    elif n_tx >= 3 and n_tx <= 10:
        # Perform a write
        nbi = n_tx-3
        cmd_addr = (nbi/4)*2**28 + 2**27 + (nbi%4)*2**25 +  txbuf[0]*2**8 + txbuf[1]
        dat = 0
        for n in range(2,n_tx):
            dat = dat + ((txbuf[n] & 0xFF) << (8*(n_tx-1-n)))
        dat_hi = dat / 2**32
        dat_lo = dat % 2**32
        wait_for_spi_ready()
        g_smpi_gateway.register_write(g_smpi2spi_base_address+4, dat_hi)
        g_smpi_gateway.register_write(g_smpi2spi_base_address+1, dat_lo)
        g_smpi_gateway.register_write(g_smpi2spi_base_address, cmd_addr)
    return 0

def wait_for_spi_ready():
    while (g_smpi_gateway.register_read(g_smpi2spi_base_address+3)%2 == 1):
        None

#
# Base class for AD9361 objects
#
class AD9361 (object):
    def __init__(self):
        pass

#
# AD9361 driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and an appropriate smpi2spi_base_address value.
#
# When ready to initialize the AD9361 then call the init_ad9361()
# method.  After this you can call set_ad9361_configuration() or
# get_ad9361_configuration() as desired.
#
class AD9361Driver (AD9361):
    '''
        Configuration wrapper for the AD9361 driver
    '''
    def __init__(self, smpi_gateway, smpi2spi_base_address):
        global g_smpi_gateway, g_smpi2spi_base_address, g_lib

        # Initialize module variables
        g_smpi_gateway = smpi_gateway
        g_smpi2spi_base_address = smpi2spi_base_address
        g_lib = ctypes.CDLL('/usr/lib/libzaltys-ad9361.so')
        g_lib.ad9361_cmos_init.restype = ctypes.c_void_p
        g_lib.ad9361_lvds_init.restype = ctypes.c_void_p
        g_lib.ad9361_write_rxbuf.restype = None
        g_lib.ad9361_read_rxbuf.restype  = ctypes.c_ubyte

        # Setup SPI read/write callbacks
        #
        # Note: callback objects assigned to self attributes to
        # prevent garbage collection -- these are the objects that the
        # C code calls, which then redirect to their associated global
        # python functions.
        SPI_INIT_CBTYPE = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_ubyte)
        self.spi_init_callback = SPI_INIT_CBTYPE(spi_init)
        g_lib.ad9361_set_fn_spi_init(self.spi_init_callback)

        SPI_READ_CBTYPE = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_ubyte)
        self.spi_read_callback = SPI_READ_CBTYPE(spi_read)
        g_lib.ad9361_set_fn_spi_read(self.spi_read_callback)

        SPI_WRITE_THEN_READ_CBTYPE = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_uint)
        self.spi_write_then_read_callback = SPI_WRITE_THEN_READ_CBTYPE(spi_write_then_read)
        g_lib.ad9361_set_fn_spi_write_then_read(self.spi_write_then_read_callback)

        # Nullify unused callbacks
        g_lib.ad9361_set_fn_usleep(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_gpio_init(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_gpio_direction(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_gpio_is_valid(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_gpio_set_value(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_udelay(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_mdelay(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_msleep_interruptable(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_axiadc_init(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_axiadc_read(ctypes.c_void_p(0))
        g_lib.ad9361_set_fn_axiadc_write(ctypes.c_void_p(0))

        # Initialize object attributes
        self.sample_rate = 61440000
        self.tx_carrier_freq = 1000000000
        self.rx_carrier_freq = 1000000000
        self.tx_bandwidth = self.sample_rate//2
        self.rx_bandwidth = self.sample_rate//2

    def init_ad9361(self, interface="CMOS"):
        global g_rf_phy

        if interface.upper() == "CMOS":
            g_rf_phy = g_lib.ad9361_cmos_init()
        else:
            g_rf_phy = g_lib.ad9361_lvds_init()

    def set_ad9361_configuration(self, sample_rate=None, tx_carrier_freq=None, rx_carrier_freq=None,
                                 tx_bandwidth=None, rx_bandwidth=None):
        if sample_rate:     self.sample_rate     = int(sample_rate)
        if tx_carrier_freq: self.tx_carrier_freq = int(tx_carrier_freq)
        if tx_carrier_freq: self.rx_carrier_freq = int(rx_carrier_freq)
        if tx_bandwidth:    self.tx_bandwidth    = int(tx_bandwidth)
        if rx_bandwidth:    self.rx_bandwidth    = int(rx_bandwidth)

        self.tx_bandwidth = min(self.sample_rate//2, self.tx_bandwidth)
        self.rx_bandwidth = min(self.sample_rate//2, self.rx_bandwidth)

        g_lib.ad9361_set_tx_sampling_freq(g_rf_phy, ctypes.c_ulong(self.sample_rate))
        g_lib.ad9361_set_rx_sampling_freq(g_rf_phy, ctypes.c_ulong(self.sample_rate))
        g_lib.ad9361_set_tx_rf_bandwidth(g_rf_phy, ctypes.c_ulong(self.tx_bandwidth))
        g_lib.ad9361_set_rx_rf_bandwidth(g_rf_phy, ctypes.c_ulong(self.rx_bandwidth))

        g_lib.ad9361_set_tx_lo_freq(g_rf_phy, ctypes.c_ulonglong(self.tx_carrier_freq))
        g_lib.ad9361_set_rx_lo_freq(g_rf_phy, ctypes.c_ulonglong(self.rx_carrier_freq))

    def get_ad9361_configuration(self):
        tx_sampling_freq = ctypes.c_ulong(0)
        rx_sampling_freq = ctypes.c_ulong(0)
        tx_rf_bandwidth = ctypes.c_ulong(0)
        rx_rf_bandwidth = ctypes.c_ulong(0)
        tx_lo_freq = ctypes.c_ulonglong(0)
        rx_lo_freq = ctypes.c_ulonglong(0)

        g_lib.ad9361_get_tx_sampling_freq(g_rf_phy, ctypes.byref(tx_sampling_freq))
        g_lib.ad9361_get_rx_sampling_freq(g_rf_phy, ctypes.byref(rx_sampling_freq))

        g_lib.ad9361_get_tx_rf_bandwidth(g_rf_phy, ctypes.byref(tx_rf_bandwidth))
        g_lib.ad9361_get_rx_rf_bandwidth(g_rf_phy, ctypes.byref(rx_rf_bandwidth))
        
        g_lib.ad9361_get_tx_lo_freq(g_rf_phy, ctypes.byref(tx_lo_freq))
        g_lib.ad9361_get_rx_lo_freq(g_rf_phy, ctypes.byref(rx_lo_freq))

        return (tx_sampling_freq.value, rx_sampling_freq.value, tx_rf_bandwidth.value, rx_rf_bandwidth.value, tx_lo_freq.value, rx_lo_freq.value)

    def update_ad9361_tx_configuration(self, carrier_freq=None, bandwidth=None):
        if carrier_freq:
            self.tx_carrier_freq = int(carrier_freq)
            g_lib.ad9361_set_tx_lo_freq(g_rf_phy, ctypes.c_ulonglong(self.tx_carrier_freq))

        if bandwidth:
            self.tx_bandwidth = min(self.sample_rate//2, int(bandwidth))
            g_lib.ad9361_set_tx_rf_bandwidth(g_rf_phy, ctypes.c_ulong(self.tx_bandwidth))

    def update_ad9361_rx_configuration(self, carrier_freq=None, bandwidth=None):
        if carrier_freq:
            self.rx_carrier_freq = int(carrier_freq)
            g_lib.ad9361_set_rx_lo_freq(g_rf_phy, ctypes.c_ulonglong(self.rx_carrier_freq))

        if bandwidth:
            self.rx_bandwidth = min(self.sample_rate//2, int(bandwidth))
            g_lib.ad9361_set_rx_rf_bandwidth(g_rf_phy, ctypes.c_ulong(self.rx_bandwidth))


#
# A dummy driver class for testing purposes
#
class AD9361Dummy (AD9361):
    def __init__(self, smpi_gateway, smpi2spi_base_address):
        print("AD9361Dummy __init__")
        if smpi_gateway:          print("  smpi_gateway = " + str(smpi_gateway))
        if smpi2spi_base_address: print("  smpi2spi_base_address = " + str(smpi2spi_base_address) + ')')

    def init_ad9361(self, interface="CMOS"):
        print("AD9361Dummy init_ad9361")
        if interface: print("  interface = " + str(interface))

    def set_ad9361_configuration(self, sample_rate=None, tx_carrier_freq=None, rx_carrier_freq=None,
                                 tx_bandwidth=None, rx_bandwidth=None):
        print("AD9361Dummy set_ad9361_configuration")
        if sample_rate:     print("  sample_rate = " + str(sample_rate))
        if tx_carrier_freq: print("  tx_carrier_freq = " + str(tx_carrier_freq))
        if rx_carrier_freq: print("  rx_carrier_freq = " + str(rx_carrier_freq))
        if tx_bandwidth:    print("  tx_bandwidth = " + str(tx_bandwidth))
        if rx_bandwidth:    print("  rx_bandwidth = " + str(rx_bandwidth))

    def get_ad9361_configuration(self):
        print("AD9361Dummy get_ad9361_configuration")
        print("  sample_rate = " + str(self.sample_rate))
        print("  tx_carrier_freq = " + str(self.tx_carrier_freq))
        print("  rx_carrier_freq = " + str(self.rx_carrier_freq))
        print("  tx_bandwidth = " + str(self.tx_bandwidth))
        print("  rx_bandwidth = " + str(self.rx_bandwidth))

        return (self.tx_sampling_freq, self.rx_sampling_freq, self.tx_rf_bandwidth, self.rx_rf_bandwidth,
                self.tx_lo_freq, self.rx_lo_freq)

    def update_ad9361_tx_configuration(self, carrier_freq=None, bandwidth=None):
        print("AD9361Dummy update_ad9361_tx_configuration")
        print("  carrier_freq = " + str(carrier_freq))
        print("  bandwidth = " + str(bandwidth))

    def update_ad9361_rx_configuration(self, carrier_freq=None, bandwidth=None):
        print("AD9361Dummy update_ad9361_rx_configuration")
        print("  carrier_freq = " + str(carrier_freq))
        print("  bandwidth = " + str(bandwidth))
