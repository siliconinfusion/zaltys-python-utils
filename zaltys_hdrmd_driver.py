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
##  A wrapper for the Zaltys HDRM Demodulator driver (libzaltys-hdrmd.so).
##

import os
import ctypes

#
# Callback functions (called from libzaltys-hdrmd C code)
#
# The following variables and functions need to be module functions,
# not class attributes/methods.  This is because a class method
# invoked from C has no notion of self, so cannot find other methods
# or attributes.
#
g_smpi_gateway = None

g_lib = None

def register_init(config):
    None

def register_write(address, data):
    # C driver supplies byte-address, need to convert to SMPI register-address
    g_smpi_gateway.register_write(address//4, data)

def register_barrier():
    None

def register_done(config):
    None

#
# The HDRM demodulator driver parameter structure.
#
class HDRMDCONFIG(ctypes.Structure):
    _fields_ = [("base_address",           ctypes.c_ulong),
                ("sample_rate",            ctypes.c_uint),
                ("datapath_extension",     ctypes.c_uint),
                ("symbol_rate",            ctypes.c_uint),
                ("if_freq_offset",         ctypes.c_uint),
                ("spectral_inversion",     ctypes.c_byte),
                ("ragc_enable",            ctypes.c_byte),
                ("ragc_invert",            ctypes.c_byte),
                ("tmtf_is_programmable",   ctypes.c_byte),
                ("tmtf_tap_length",        ctypes.c_uint),
                ("tmtf_coeff_size",        ctypes.c_uint),
                ("rrc_alpha",              ctypes.c_uint),
                ("output_amplitude",       ctypes.c_uint),
                ("mer_period",             ctypes.c_uint),
                ("reacq_holdoff",          ctypes.c_byte),
                ("reacq_activation_delay", ctypes.c_double),
                ("reacq_restart_delay",    ctypes.c_double),
                ("falsedet_enable",        ctypes.c_byte),
                ("falsedet_oneshot",       ctypes.c_byte),
                ("falsedet_thresh",        ctypes.c_double),
                ("falsedet_period",        ctypes.c_double),
                ("apsk_rr_oi",             ctypes.c_double),
                ("apsk_rr_mi",             ctypes.c_double),
                ("aeq_bypass",             ctypes.c_byte),
                ("aeq_adpt_enable",        ctypes.c_byte),
                ("aeq_cma_enable",         ctypes.c_byte),
                ("aeq_2x_rate",            ctypes.c_byte),
                ("cfe_enable",             ctypes.c_byte),
                ("cfe_range",              ctypes.c_uint),
                ("search_range",           ctypes.c_uint),
                ("coarse_steps",           ctypes.c_uint)]


#
# HDRM Demodulator driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and appropriate base_address and datapath_extension values.
#
class HdrmdDriver (object):
    '''
        Configuration wrapper for the Zaltys HDRM Demodulator
    '''
    def __init__(self, smpi_gateway, base_address, datapath_extension=4):
        global g_smpi_gateway, g_lib

        # Initialize module variables
        g_smpi_gateway = smpi_gateway
        g_lib = ctypes.CDLL('/usr/lib/libzaltys-hdrmd.so')

        # Setup callback functions
        #
        # Note: callback objects assigned to self attributes to
        # prevent garbage collection -- these are the objects that the
        # C code calls, which then redirect to their associated global
        # python functions.
        INITCBTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(HDRMDCONFIG))
        self.reg_init_callback = INITCBTYPE(register_init)
        g_lib.zaltys_hdrm_demod_set_callback_reg_init(self.reg_init_callback)

        WRITECBTYPE = ctypes.CFUNCTYPE(None, ctypes.c_ulong, ctypes.c_uint)
        self.reg_write_callback = WRITECBTYPE(register_write)
        g_lib.zaltys_hdrm_demod_set_callback_reg_write(self.reg_write_callback)

        BARRIERCBTYPE = ctypes.CFUNCTYPE(None)
        self.reg_barrier_callback = BARRIERCBTYPE(register_barrier)
        g_lib.zaltys_hdrm_demod_set_callback_reg_barrier(self.reg_barrier_callback)

        DONECBTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(HDRMDCONFIG))
        self.reg_done_callback = INITCBTYPE(register_done)
        g_lib.zaltys_hdrm_demod_set_callback_reg_done(self.reg_done_callback)

        # Initialize default driver parameters
        self.hdrmd_config = HDRMDCONFIG()
        self.hdrmd_config.base_address           = ctypes.c_ulong(4*base_address)  # convert to byte adress
        self.hdrmd_config.sample_rate            = ctypes.c_uint(100000000)
        self.hdrmd_config.datapath_extension     = ctypes.c_uint(datapath_extension)
        self.hdrmd_config.symbol_rate            = ctypes.c_uint(0)
        self.hdrmd_config.if_freq_offset         = ctypes.c_uint(0)
        self.hdrmd_config.spectral_inversion     = ctypes.c_byte(0)
        self.hdrmd_config.ragc_enable            = ctypes.c_byte(1)
        self.hdrmd_config.ragc_invert            = ctypes.c_byte(1)
        self.hdrmd_config.tmtf_is_programmable   = ctypes.c_byte(0)
        self.hdrmd_config.tmtf_tap_length        = ctypes.c_uint(0)
        self.hdrmd_config.tmtf_coeff_size        = ctypes.c_uint(0)
        self.hdrmd_config.rrc_alpha              = ctypes.c_uint(20)
        self.hdrmd_config.output_amplitude       = ctypes.c_uint(1024)
        self.hdrmd_config.mer_period             = ctypes.c_uint(10000)
        self.hdrmd_config.reacq_holdoff          = ctypes.c_byte(0)
        self.hdrmd_config.reacq_activation_delay = ctypes.c_double(0.5)
        self.hdrmd_config.reacq_restart_delay    = ctypes.c_double(1.0)
        self.hdrmd_config.falsedet_enable        = ctypes.c_byte(1)
        self.hdrmd_config.falsedet_oneshot       = ctypes.c_byte(1)
        self.hdrmd_config.falsedet_thresh        = ctypes.c_double(0.5)
        self.hdrmd_config.falsedet_period        = ctypes.c_double(2.0)
        self.hdrmd_config.apsk_rr_oi             = ctypes.c_double(0.0)
        self.hdrmd_config.apsk_rr_mi             = ctypes.c_double(0.0)
        self.hdrmd_config.aeq_bypass             = ctypes.c_byte(1)
        self.hdrmd_config.aeq_adpt_enable        = ctypes.c_byte(1)
        self.hdrmd_config.aeq_cma_enable         = ctypes.c_byte(1)
        self.hdrmd_config.aeq_2x_rate            = ctypes.c_byte(0)
        self.hdrmd_config.cfe_enable             = ctypes.c_byte(0)
        self.hdrmd_config.cfe_range              = ctypes.c_uint(0)
        self.hdrmd_config.search_range           = ctypes.c_uint(5)
        self.hdrmd_config.coarse_steps           = ctypes.c_uint(10)

    def configure_demod(self, sample_rate, symbol_rate, modulation_scheme, rrc_alpha=20, if_freq_offset=0, aeq_enable=False):
        self.hdrmd_config.sample_rate     = ctypes.c_uint(sample_rate)
        self.hdrmd_config.symbol_rate     = ctypes.c_uint(symbol_rate)
        self.hdrmd_config.rrc_alpha       = ctypes.c_uint(rrc_alpha)
        self.hdrmd_config.if_freq_offset  = ctypes.c_uint(if_freq_offset)
        self.hdrmd_config.aeq_bypass      = ctypes.c_byte(0 if aeq_enable else 1)
        self.hdrmd_config.aeq_adpt_enable = ctypes.c_byte(aeq_enable)
        self.hdrmd_config.aeq_cma_enable  = ctypes.c_byte(aeq_enable)
        
        if modulation_scheme.upper() == "BPSK":
            g_lib.zaltys_hdrm_demod_utils_config_bpsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "QPSK":
            g_lib.zaltys_hdrm_demod_utils_config_qpsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "8PSK":
            g_lib.zaltys_hdrm_demod_utils_config_8psk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "16QAM":
            g_lib.zaltys_hdrm_demod_utils_config_16qam(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "OQPSK":
            g_lib.zaltys_hdrm_demod_utils_config_oqpsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "CQPSK":
            g_lib.zaltys_hdrm_demod_utils_config_cqpsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "DQPSK":
            g_lib.zaltys_hdrm_demod_utils_config_dqpsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "8QAM":
            g_lib.zaltys_hdrm_demod_utils_config_8qam(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "16APSK":
            g_lib.zaltys_hdrm_demod_utils_config_16apsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "32APSK":
            g_lib.zaltys_hdrm_demod_utils_config_32apsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "8APSK":
            g_lib.zaltys_hdrm_demod_utils_config_8apsk(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "64QAM":
            g_lib.zaltys_hdrm_demod_utils_config_64qam(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "OS8QAM":
            g_lib.zaltys_hdrm_demod_utils_config_os8qam(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "32QAM":
            g_lib.zaltys_hdrm_demod_utils_config_32qam(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "C32QAM":
            g_lib.zaltys_hdrm_demod_utils_config_c32qam(ctypes.byref(self.hdrmd_config))
        elif modulation_scheme.upper() == "C128QAM":
            g_lib.zaltys_hdrm_demod_utils_config_c128qam(ctypes.byref(self.hdrmd_config))
