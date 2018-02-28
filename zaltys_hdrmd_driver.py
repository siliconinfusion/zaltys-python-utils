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
## A wrapper for the Zaltys HDRM Demodulator driver (libzaltys-hdrmd.so).
##
## Requires demodulator version 7.7 or compatible.
##
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
    g_smpi_gateway.register_write(int(address)//4, int(data))

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
# HDRM Demodulator driver exceptions
#
class HdrmdDriverError(Exception): pass


#
# HDRM Demodulator driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and appropriate base_address and datapath_extension values.
#
class HdrmdDriver (object):
    '''
        Configuration wrapper for the Zaltys HDRM Demodulator

        Example usage:-
          hdrmd = HdrmdDriver(gateway, base_address=0x400)
          hdrmd.modulation_scheme = "16QAM"
          hdrmd.sample_rate = 125e6
          hdrmd.symbol_rate = 10e6
          hdrmd.configure_demod()
    '''
    def __init__(self, smpi_gateway, base_address=0, datapath_extension=4):
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
        self.reg_done_callback = DONECBTYPE(register_done)
        g_lib.zaltys_hdrm_demod_set_callback_reg_done(self.reg_done_callback)

        # Set default driver parameters
        self.modulation_scheme      = "QPSK"
        self.base_address           = base_address
        self.sample_rate            = 100000000
        self.datapath_extension     = datapath_extension
        self.symbol_rate            = 0
        self.if_freq_offset         = 0
        self.spectral_inversion     = False
        self.ragc_enable            = True
        self.ragc_invert            = False
        self.tmtf_is_programmable   = False
        self.tmtf_tap_length        = 0
        self.tmtf_coeff_size        = 0
        self.rrc_alpha              = 20
        self.output_amplitude       = 1024
        self.mer_period             = 10000
        self.reacq_holdoff          = False
        self.reacq_activation_delay = 0.5
        self.reacq_restart_delay    = 1.0
        self.falsedet_enable        = True
        self.falsedet_oneshot       = True
        self.falsedet_thresh        = 0.5
        self.falsedet_period        = 2.0
        self.apsk_rr_oi             = 0.0
        self.apsk_rr_mi             = 0.0
        self.aeq_bypass             = True
        self.aeq_adpt_enable        = False
        self.aeq_cma_enable         = False
        self.aeq_2x_rate            = False
        self.cfe_enable             = False
        self.cfe_range              = 0
        self.search_range           = 5
        self.coarse_steps           = 10

        # Initialize driver structure
        self.hdrmd_config = HDRMDCONFIG()
        self.fill_driver_struct()

    def fill_driver_struct(self):
        self.hdrmd_config.base_address           = ctypes.c_ulong(4*int(self.base_address))  # convert to byte adress
        self.hdrmd_config.sample_rate            = ctypes.c_uint(int(self.sample_rate))
        self.hdrmd_config.datapath_extension     = ctypes.c_uint(int(self.datapath_extension))
        self.hdrmd_config.symbol_rate            = ctypes.c_uint(int(self.symbol_rate))
        self.hdrmd_config.if_freq_offset         = ctypes.c_uint(int(self.if_freq_offset))
        self.hdrmd_config.spectral_inversion     = ctypes.c_byte(self.spectral_inversion)
        self.hdrmd_config.ragc_enable            = ctypes.c_byte(self.ragc_enable)
        self.hdrmd_config.ragc_invert            = ctypes.c_byte(self.ragc_invert)
        self.hdrmd_config.tmtf_is_programmable   = ctypes.c_byte(self.tmtf_is_programmable)
        self.hdrmd_config.tmtf_tap_length        = ctypes.c_uint(int(self.tmtf_tap_length))
        self.hdrmd_config.tmtf_coeff_size        = ctypes.c_uint(int(self.tmtf_coeff_size))
        self.hdrmd_config.rrc_alpha              = ctypes.c_uint(int(self.rrc_alpha))
        self.hdrmd_config.output_amplitude       = ctypes.c_uint(int(self.output_amplitude))
        self.hdrmd_config.mer_period             = ctypes.c_uint(int(self.mer_period))
        self.hdrmd_config.reacq_holdoff          = ctypes.c_byte(self.reacq_holdoff)
        self.hdrmd_config.reacq_activation_delay = ctypes.c_double(self.reacq_activation_delay)
        self.hdrmd_config.reacq_restart_delay    = ctypes.c_double(self.reacq_restart_delay)
        self.hdrmd_config.falsedet_enable        = ctypes.c_byte(self.falsedet_enable)
        self.hdrmd_config.falsedet_oneshot       = ctypes.c_byte(self.falsedet_oneshot)
        self.hdrmd_config.falsedet_thresh        = ctypes.c_double(self.falsedet_thresh)
        self.hdrmd_config.falsedet_period        = ctypes.c_double(self.falsedet_period)
        self.hdrmd_config.apsk_rr_oi             = ctypes.c_double(self.apsk_rr_oi)
        self.hdrmd_config.apsk_rr_mi             = ctypes.c_double(self.apsk_rr_mi)
        self.hdrmd_config.aeq_bypass             = ctypes.c_byte(self.aeq_bypass)
        self.hdrmd_config.aeq_adpt_enable        = ctypes.c_byte(self.aeq_adpt_enable)
        self.hdrmd_config.aeq_cma_enable         = ctypes.c_byte(self.aeq_cma_enable)
        self.hdrmd_config.aeq_2x_rate            = ctypes.c_byte(self.aeq_2x_rate)
        self.hdrmd_config.cfe_enable             = ctypes.c_byte(self.cfe_enable)
        self.hdrmd_config.cfe_range              = ctypes.c_uint(int(self.cfe_range))
        self.hdrmd_config.search_range           = ctypes.c_uint(int(self.search_range))
        self.hdrmd_config.coarse_steps           = ctypes.c_uint(int(self.coarse_steps))

    def configure_demod(self):
        self.fill_driver_struct()

        if self.modulation_scheme.upper() == "BPSK":
            g_lib.zaltys_hdrm_demod_utils_config_bpsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "QPSK":
            g_lib.zaltys_hdrm_demod_utils_config_qpsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "8PSK":
            g_lib.zaltys_hdrm_demod_utils_config_8psk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "16QAM":
            g_lib.zaltys_hdrm_demod_utils_config_16qam(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "OQPSK":
            g_lib.zaltys_hdrm_demod_utils_config_oqpsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "CQPSK":
            g_lib.zaltys_hdrm_demod_utils_config_cqpsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "DQPSK":
            g_lib.zaltys_hdrm_demod_utils_config_dqpsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "8QAM":
            g_lib.zaltys_hdrm_demod_utils_config_8qam(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "16APSK":
            g_lib.zaltys_hdrm_demod_utils_config_16apsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "32APSK":
            g_lib.zaltys_hdrm_demod_utils_config_32apsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "8APSK":
            g_lib.zaltys_hdrm_demod_utils_config_8apsk(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "64QAM":
            g_lib.zaltys_hdrm_demod_utils_config_64qam(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "OS8QAM":
            g_lib.zaltys_hdrm_demod_utils_config_os8qam(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "32QAM":
            g_lib.zaltys_hdrm_demod_utils_config_32qam(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "C32QAM":
            g_lib.zaltys_hdrm_demod_utils_config_c32qam(ctypes.byref(self.hdrmd_config))
        elif self.modulation_scheme.upper() == "C128QAM":
            g_lib.zaltys_hdrm_demod_utils_config_c128qam(ctypes.byref(self.hdrmd_config))
        else:
            raise HdrmdDriverError('Unknown modulation scheme: {}'.format(self.modulation_scheme))
