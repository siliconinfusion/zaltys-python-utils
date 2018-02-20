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
##  A pure python driver for the Zaltys DVB-S2 Baseband Modulator.
##

# 
# Legacy mode RRC coefficients
#
# Assumes a 49-tap filter with 14-bit coefficients, centre tap of 8192.
#
legacy_rrc_20 = [ 4871, -408, -1435, 362, 659, -293, -295, 213, 95, -132,  10, 62,
                   -53,   -9,    57, -23, -39,   35,   15, -31,  6,   19, -18, -5 ]

legacy_rrc_25 = [ 4768, -493, -1306, 407, 501, -288, -140, 163, -22, -58, 71, -12,
                   -58,   41,    22, -39,   9,   19,  -24,   2,  21, -16, -9,  17 ]

legacy_rrc_30 = [ 4659, -568, -1163, 429, 341, -251, -14, 90, -83, 14, 65, -51,
                   -14,   38,   -23,  -7,  28,  -17, -12, 20,  -7, -9, 15,  -5 ]

legacy_rrc_35 = [ 4544, -633, -1011, 427, 192, -190, 72, 15, -87, 56, 21, -44,
                    28,    2,   -29,  23,   4,  -18, 15, -1, -14, 13,  0,  -9 ]

legacy_rrc_40 = [ 4424, -688, -853, 404,  63, -117, 111, -43, -52, 60, -24, -9,
                    34,  -26,   -2,  18, -19,    7,  10, -15,   7,  3, -11,  9 ]

legacy_rrc_select = { 20 : legacy_rrc_20,
                      25 : legacy_rrc_25,
                      30 : legacy_rrc_30,
                      35 : legacy_rrc_35,
                      40 : legacy_rrc_40 }

#
# Standard RRC coefficients
#
# Assumes a 181-tap filter with 16-bit coefficients, centre tap of 32768.
#
rrc05_181tap_16bit_coeffs = [20560,  -441, -6802,   437,  4020,  -432, -2807,   425,  2117,  -415, -1666,   404,  1344,  -391, -1101,
                               376,   909,  -360,  -753,   343,   624,  -324,  -515,   305,   422,  -285,  -342,   264,   273,  -243,
                              -214,   221,   162,  -200,  -118,   178,    80,  -158,   -48,   137,    21,  -118,     1,    99,   -19,
                               -81,    33,    64,   -44,   -49,    52,    34,   -57,   -21,    60,     9,   -61,     1,    60,   -10,
                               -57,    17,    54,   -24,   -49,    28,    44,   -32,   -38,    35,    32,   -36,   -25,    36,    19,
                               -36,   -13,    35,    7,    -33,    -1,    30,    -4,   -27,     8,    24,   -12,   -20,    15,    16]

rrc10_181tap_16bit_coeffs = [20230,  -863, -6542,   838,  3691,  -797, -2397,   743,  1633,  -677, -1120,   602,   751,  -521,  -479,
                               436,   275,  -352,  -126,   271,    19,  -195,    52,   127,   -96,   -67,   116,    19,  -120,    19,
                               110,   -47,   -92,    63,    68,   -71,   -43,    71,    19,   -64,     2,    53,   -20,   -39,    32,
                                24,   -39,    -9,    42,    -4,   -40,    15,    34,   -23,   -26,    28,    17,   -30,    -7,    28,
                                -2,   -25,    10,    19,   -16,   -12,    19,     5,   -21,     1,    20,    -7,   -18,    12,    14,
                               -15,    -9,    16,     4,   -16,     1,    14,    -6,   -11,     9,     7,   -12,    -3,    13,    -1]

rrc15_181tap_16bit_coeffs = [19871, -1262, -6184,  1180,  3216, -1053, -1823,   891,  1000,  -709,  -475,   521,   141,  -343,    55,
                               187,  -152,   -62,   178,   -29,  -157,    83,   110,  -105,   -55,   101,     4,   -79,    34,    47,
                               -56,   -14,    61,   -15,   -53,    34,    35,   -43,   -14,    42,    -6,   -33,    21,    18,   -30,
                                -3,    30,   -11,   -25,    20,    15,   -24,    -3,    22,    -7,   -17,    15,     8,   -18,     1,
                                18,    -9,   -13,    14,     7,   -15,     0,    14,    -7,    -9,    11,     3,   -12,     2,    11,
                                -7,    -8,    10,     3,   -10,     2,     9,    -6,    -5,     8,     1,    -9,     3,     7,    -6]

rrc20_181tap_16bit_coeffs = [19484, -1633, -5740,  1447,  2637, -1172, -1179,   850,   379,  -527,    40,   246,  -211,   -36,   226,
                               -91,  -157,   139,    61,  -126,    22,    77,   -70,   -18,    80,   -30,   -59,    55,    23,   -55,
                                12,    37,   -35,   -10,    41,   -14,   -31,    29,    12,   -31,     7,    22,   -21,    -7,    24,
                                -8,   -19,    18,     7,   -20,     5,    14,   -14,    -5,    16,    -6,   -13,    12,     5,   -14,
                                 4,    10,   -10,    -3,    12,    -4,    -9,     9,     4,   -10,     3,     8,    -7,    -3,     9,
                                -3,    -7,     7,     3,    -8,     2,     6,    -6,    -2,     7,    -2,    -5,     5,     2,    -6]

rrc25_181tap_16bit_coeffs = [19072, -1970, -5223,  1627,  2003, -1151,  -561,   651,   -90,  -230,   285,   -46,  -233,   164,    89,
                              -155,    38,    77,   -97,    10,    86,   -63,   -34,    68,   -19,   -38,    48,    -4,   -44,    33,
                                18,   -38,    12,    23,   -29,     2,    27,   -20,   -11,    24,    -8,   -15,    19,    -1,   -18,
                                14,     7,   -17,     6,    11,   -14,     1,    13,   -10,    -5,    12,    -4,    -8,    10,     0,
                               -10,     7,     4,   -10,     3,     6,    -8,     0,     8,    -6,    -3,     8,    -3,    -5,     6,
                                 0,    -6,     5,     3,    -6,     2,     4,    -5,     0,     5,    -4,    -2,     5,    -2,    -3]

rrc30_181tap_16bit_coeffs = [18636, -2271, -4652,  1714,  1363, -1003,   -55,   360,  -331,    55,   261,  -203,   -55,   152,   -91,
                               -27,   113,   -66,   -48,    81,   -28,   -35,    60,   -21,   -39,    46,    -4,   -32,    33,    -2,
                               -31,    26,     6,   -26,    18,     7,   -23,    14,    10,   -20,     8,    10,   -17,     6,    12,
                               -15,     2,    11,   -12,     0,    11,   -10,    -2,    10,    -7,    -3,    10,    -6,    -4,     9,
                                -4,    -5,     8,    -3,    -6,     7,    -1,    -6,     6,     0,    -6,     5,     1,    -6,     4,
                                 2,    -5,     3,     2,    -5,     2,     3,    -5,     1,     3,    -4,     1,     3,    -4,     0]

rrc35_181tap_16bit_coeffs = [18177, -2533, -4042,  1708,   766,  -761,   286,    61,  -348,   224,    82,  -175,   112,     8,  -117,
                                92,    15,   -72,    62,    -5,   -55,    52,    -1,   -37,    39,    -9,   -30,    34,    -6,   -20,
                                27,    -9,   -17,    23,    -8,   -12,    20,    -9,   -10,    17,    -8,    -7,    15,    -9,    -6,
                                13,    -8,    -3,    11,    -8,    -3,     9,    -7,    -1,     8,    -7,    -1,     7,    -7,     0,
                                 6,    -6,     0,     5,    -6,     1,     5,    -6,     1,     4,    -5,     2,     3,    -5,     2,
                                 3,    -5,     2,     2,    -4,     2,     2,    -4,     2,     1,    -4,     2,     1,    -3,     2]

rrc40_181tap_16bit_coeffs = [17697, -2752, -3413,  1616,   251,  -469,   444,  -172,  -207,   239,   -98,   -35,   138,  -104,    -9,
                                71,   -76,    27,    42,   -59,    29,    12,   -43,    34,     2,   -27,    30,   -11,   -17,    26,
                               -14,    -6,    21,   -17,    -1,    14,   -16,     6,     9,   -15,     8,     4,   -12,    10,     0,
                                -9,    10,    -3,    -6,     9,    -5,    -2,     8,    -7,     0,     6,    -7,     2,     4,    -7,
                                 4,     2,    -6,     5,     0,    -4,     5,    -2,    -3,     5,    -3,    -1,     4,    -4,     0,
                                 3,    -4,     1,     2,    -4,     2,     1,    -3,     3,     0,    -3,     3,    -1,    -2,     3]

standard_rrc_select = {  5 : rrc05_181tap_16bit_coeffs,
                        10 : rrc10_181tap_16bit_coeffs,
                        15 : rrc15_181tap_16bit_coeffs,
                        20 : rrc20_181tap_16bit_coeffs,
                        25 : rrc25_181tap_16bit_coeffs,
                        30 : rrc30_181tap_16bit_coeffs,
                        35 : rrc35_181tap_16bit_coeffs,
                        40 : rrc40_181tap_16bit_coeffs }

#
# DVB-S2 Modulator driver exceptions
#
class Dvbs2mDriverError(Exception): pass


#
# DVB-S2 Modulator driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and appropriate base_address value.
#
class Dvbs2mDriver (object):
    '''
        Configuration wrapper for the Zaltys DVB-S2 Modulator

        Example usage:-
          dvbs2m = Dvbs2mDriver(gateway, base_address=0x100)
          dvbs2m.ccm_mode = True
          dvbs2m.pls_value = 4
          dvbs2m.sample_rate = 125e6
          dvbs2m.symbol_rate = 10e6
          dvbs2m.configure_mod()
    '''
    def __init__(self, smpi_gateway, base_address=0, legacy_mode=False, txfilt_num_taps=181, txfilt_full_coeff_width=14):
        self.smpi_gateway            = smpi_gateway

        # Set hardware configuration parameters
        self.base_address            = base_address
        self.legacy_mode             = legacy_mode
        self.txfilt_num_taps         = txfilt_num_taps
        self.txfilt_full_coeff_width = txfilt_full_coeff_width

        # Set default driver parameters
        self.sample_rate        = 100000000
        self.symbol_rate        = 1000000
        self.rrc_alpha          = 20
        self.free_running       = True
        self.spectral_inversion = False
        self.ccm_mode           = False
        self.pls_value          = 0

    def configure_mod(self):
        # Hold datapath in reset
        enc_control = 0x00000001
        self.smpi_gateway.register_write(self.base_address + 0x100, enc_control) # FE: ENC_CONTROL
        self.smpi_gateway.register_write(self.base_address + 0x200, 0x00000001)  # PLF: PLF_CONTROL
        self.smpi_gateway.register_write(self.base_address + 0x304, 0x00010000)  # HDRMM: FIFO_CTRL
        self.smpi_gateway.register_write(self.base_address + 0x300, 0x00000001)  # HDRMM: SYS_CTRL

        # DVBS2FE CCM/VCM mode, enable BB scrambler
        enc_control = enc_control | (self.pls_value << 16) | ((1 if self.ccm_mode else 0) << 6) | (1 << 5)
        self.smpi_gateway.register_write(self.base_address + 0x100, enc_control) # ENC_CONTROL

        # HDRMM symbol mapper bypass
        self.smpi_gateway.register_write(self.base_address + 0x305, 0x00010000) # MAP_CBASE

        # HDRMM interpolation filter and SPLL setup
        self.smpi_gateway.register_write(self.base_address + 0x310, 0x00000001) # SPLL_CTRL, hold SPLL in reset

        sr = self.sample_rate/5
        iif = 0
        while self.symbol_rate < sr:
            sr = sr/2
            iif = iif + 1
        nco = int(round((self.symbol_rate / self.sample_rate) * 2**iif * 2**28))
        self.smpi_gateway.register_write(self.base_address + 0x308, iif)   # IIF_CTRL
        self.smpi_gateway.register_write(self.base_address + 0x311, nco)   # SPLL_INCR

        self.smpi_gateway.register_write(self.base_address + 0x312, 1024)  # SPLL_LOCK_THRESH
        self.smpi_gateway.register_write(self.base_address + 0x313, 32768) # SPLL_UNLOCK_THRESH
        self.smpi_gateway.register_write(self.base_address + 0x314, 4)     # SPLL_PROP_SHIFT
        self.smpi_gateway.register_write(self.base_address + 0x315, 18)    # SPLL_INTEG_SHIFT

        self.smpi_gateway.register_write(self.base_address + 0x318, 10)    # SPLL_SHIFTADJ_MAX
        self.smpi_gateway.register_write(self.base_address + 0x319, 512)   # SPLL_SHIFTADJ_PERIOD
        self.smpi_gateway.register_write(self.base_address + 0x31A, 2048)  # SPLL_SHIFTADJ_THRESH
        self.smpi_gateway.register_write(self.base_address + 0x31B, 32768) # SPLL_SHIFTADJ_RST_THRESH

        if self.free_running:
            self.smpi_gateway.register_write(self.base_address + 0x310, 0x00000010)  # enable SPLL (free running)
        else:
            self.smpi_gateway.register_write(self.base_address + 0x310, 0x00000000)  # enable SPLL

        # HDRMM DAC control setup
        dac_ctrl = 0x00000302
        if self.spectral_inversion: dac_ctrl = dac_ctrl | 0x00000020
        self.smpi_gateway.register_write(self.base_address + 0x309, dac_ctrl)    # DAC_CTRL
        self.smpi_gateway.register_write(self.base_address + 0x30A, 0x00000000)  # DAC_IOFFSET
        self.smpi_gateway.register_write(self.base_address + 0x30B, 0x00000000)  # DAC_QOFFSET
        self.smpi_gateway.register_write(self.base_address + 0x30C, 0x00000000)  # DAC_GAIN_CAL
        self.smpi_gateway.register_write(self.base_address + 0x30D, 0x00002000)  # DAC_GAIN
        
        # HDRMM transmit filter setup
        if self.legacy_mode:
            rrc_coeffs = legacy_rrc_select.get(self.rrc_alpha)
            if rrc_coeffs:
                for offset in range(0,24):
                    self.smpi_gateway.register_write(self.base_address + 0x320 + offset, rrc_coeffs[offset] % 65536)
            else:
                raise Dvbs2mDriverError('Illegal legacy RRC roll-off: {}, only 20%, 25%, 30%, 35%, 40% supported'.format(self.rrc_alpha))
        else:
            rrc_coeffs = standard_rrc_select.get(self.rrc_alpha)
            if rrc_coeffs:
                for offset in range(89,-1,-1):
                    self.smpi_gateway.register_write(self.base_address + 0x320, int(round(float(rrc_coeffs[offset])/float(2**(16-self.txfilt_full_coeff_width)))) % 65536)
            else:
                raise Dvbs2mDriverError('Illegal RRC roll-off: {}, only 5%, 10%, 15%, 20%, 25%, 30%, 35%, 40% supported'.format(self.rrc_alpha))

        self.smpi_gateway.register_write(self.base_address + 0x338, 0x00000000)
            
        # Release datapath from reset
        self.smpi_gateway.register_write(self.base_address + 0x300, 0x00000000)  # HDRMM: SYS_CTRL
        self.smpi_gateway.register_write(self.base_address + 0x304, 0x00000000)  # HDRMM: FIFO_CTRL
        self.smpi_gateway.register_write(self.base_address + 0x200, 0x00000000)  # PLF: PLF_CONTROL
        enc_control = enc_control & 0xFFFFFFFE
        self.smpi_gateway.register_write(self.base_address + 0x100, enc_control) # FE: ENC_CONTROL
