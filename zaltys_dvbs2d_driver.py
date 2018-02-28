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
## A wrapper for the Zaltys DVB-S2 Demodulator driver (libzaltys-dvbs2d.so).
##
## Requires demodulator version 7.0 or compatible.
##
import ctypes

#
# Callback functions (called from libzaltys-dvbs2d C code)
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
# The DVB-S2 demodulator driver parameter structure.
#
class DVBS2DCONFIG(ctypes.Structure):
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
                ("aeq_bypass",             ctypes.c_byte),
                ("aeq_adpt_enable",        ctypes.c_byte),
                ("aeq_cma_enable",         ctypes.c_byte),
                ("ccm_mode",               ctypes.c_byte),
                ("config.pls_value",       ctypes.c_uint),
                ("config.s2p_enable",      ctypes.c_byte)]


#
# DVB-S2 Demodulator driver exceptions
#
class Dvbs2dDriverError(Exception): pass


#
# DVB-S2 Demodulator driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and appropriate base_address and datapath_extension values.
#
class Dvbs2dDriver (object):
    '''
        Configuration wrapper for the Zaltys DVB-S2 Demodulator

        Example usage:-
          dvbs2d = Dvbs2dDriver(gateway, base_address=0x400)
          dvbs2d.sample_rate = 125e6
          dvbs2d.symbol_rate = 10e6
          dvbs2d.configure_demod()
    '''
    def __init__(self, smpi_gateway, base_address=0, datapath_extension=4, tmtf_is_programmable=True, tmtf_tap_length=101, tmtf_coeff_size=12):
        global g_smpi_gateway, g_lib

        # Initialize module variables
        g_smpi_gateway = smpi_gateway
        g_lib = ctypes.CDLL('/usr/lib/libzaltys-dvbs2d.so')

        # Setup callback functions
        #
        # Note: callback objects assigned to self attributes to
        # prevent garbage collection -- these are the objects that the
        # C code calls, which then redirect to their associated global
        # python functions.
        INITCBTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(DVBS2DCONFIG))
        self.reg_init_callback = INITCBTYPE(register_init)
        g_lib.zaltys_dvbs2_demod_set_callback_reg_init(self.reg_init_callback)

        WRITECBTYPE = ctypes.CFUNCTYPE(None, ctypes.c_ulong, ctypes.c_uint)
        self.reg_write_callback = WRITECBTYPE(register_write)
        g_lib.zaltys_dvbs2_demod_set_callback_reg_write(self.reg_write_callback)

        BARRIERCBTYPE = ctypes.CFUNCTYPE(None)
        self.reg_barrier_callback = BARRIERCBTYPE(register_barrier)
        g_lib.zaltys_dvbs2_demod_set_callback_reg_barrier(self.reg_barrier_callback)

        DONECBTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(DVBS2DCONFIG))
        self.reg_done_callback = DONECBTYPE(register_done)
        g_lib.zaltys_dvbs2_demod_set_callback_reg_done(self.reg_done_callback)

        # Set default driver parameters
        self.base_address           = base_address
        self.sample_rate            = 100000000
        self.datapath_extension     = datapath_extension
        self.symbol_rate            = 0
        self.if_freq_offset         = 0
        self.spectral_inversion     = False
        self.ragc_enable            = True
        self.ragc_invert            = False
        self.tmtf_is_programmable   = tmtf_is_programmable
        self.tmtf_tap_length        = tmtf_tap_length
        self.tmtf_coeff_size        = tmtf_coeff_size
        self.rrc_alpha              = 20
        self.output_amplitude       = 1024
        self.mer_period             = 10000
        self.reacq_holdoff          = False
        self.reacq_activation_delay = 0.5
        self.reacq_restart_delay    = 1.0
        self.aeq_bypass             = False
        self.aeq_adpt_enable        = True
        self.aeq_cma_enable         = True
        self.ccm_mode               = False
        self.pls_value              = 0
        self.s2p_enable             = False

        # Initialize driver structure
        self.dvbs2d_config = DVBS2DCONFIG()
        self.fill_driver_struct()

    def fill_driver_struct(self):
        self.dvbs2d_config.base_address           = ctypes.c_ulong(4*int(self.base_address))  # convert to byte adress
        self.dvbs2d_config.sample_rate            = ctypes.c_uint(int(self.sample_rate))
        self.dvbs2d_config.datapath_extension     = ctypes.c_uint(int(self.datapath_extension))
        self.dvbs2d_config.symbol_rate            = ctypes.c_uint(int(self.symbol_rate))
        self.dvbs2d_config.if_freq_offset         = ctypes.c_uint(int(self.if_freq_offset))
        self.dvbs2d_config.spectral_inversion     = ctypes.c_byte(self.spectral_inversion)
        self.dvbs2d_config.ragc_enable            = ctypes.c_byte(self.ragc_enable)
        self.dvbs2d_config.ragc_invert            = ctypes.c_byte(self.ragc_invert)
        self.dvbs2d_config.tmtf_is_programmable   = ctypes.c_byte(self.tmtf_is_programmable)
        self.dvbs2d_config.tmtf_tap_length        = ctypes.c_uint(int(self.tmtf_tap_length))
        self.dvbs2d_config.tmtf_coeff_size        = ctypes.c_uint(int(self.tmtf_coeff_size))
        self.dvbs2d_config.rrc_alpha              = ctypes.c_uint(int(self.rrc_alpha))
        self.dvbs2d_config.output_amplitude       = ctypes.c_uint(int(self.output_amplitude))
        self.dvbs2d_config.mer_period             = ctypes.c_uint(int(self.mer_period))
        self.dvbs2d_config.reacq_holdoff          = ctypes.c_byte(self.reacq_holdoff)
        self.dvbs2d_config.reacq_activation_delay = ctypes.c_double(self.reacq_activation_delay)
        self.dvbs2d_config.reacq_restart_delay    = ctypes.c_double(self.reacq_restart_delay)
        self.dvbs2d_config.aeq_bypass             = ctypes.c_byte(self.aeq_bypass)
        self.dvbs2d_config.aeq_adpt_enable        = ctypes.c_byte(self.aeq_adpt_enable)
        self.dvbs2d_config.aeq_cma_enable         = ctypes.c_byte(self.aeq_cma_enable)
        self.dvbs2d_config.ccm_mode               = ctypes.c_byte(self.ccm_mode)
        self.dvbs2d_config.pls_value              = ctypes.c_uint(int(self.pls_value))
        self.dvbs2d_config.s2p_enable             = ctypes.c_byte(self.s2p_enable)

    def configure_demod(self):
        self.fill_driver_struct()
        g_lib.zaltys_dvbs2_demod_utils_config_dvbs2(ctypes.byref(self.dvbs2d_config))
