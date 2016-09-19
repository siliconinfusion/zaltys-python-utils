##
##  Author        : Paul Onions
##  Creation date : 15 September 2016
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
##  A pure python driver for the Zaltys HDRM Modulator.
##
import math

#
# Standard constellations -- as documented in HDRMD programming guide
# (mappings as used by HDRMD stats block)
#
zaltys_bpsk_constellation = [ 0x0C000C00, 0x04000400 ]

zaltys_qpsk_constellation = [ 0x0C000C00, 0x0C000400, 0x04000C00, 0x04000400 ]

zaltys_8psk_constellation = [ 0x02d402d4, 0x00000400, 0x0000fc00, 0xfd2cfd2c,
                              0x04000000, 0xfd2c02d4, 0x02d4fd2c, 0xfc000000 ]

zaltys_16qam_constellation = [ 0x06000600, 0x06000200, 0x02000600, 0x02000200,
                               0x06000A00, 0x06000E00, 0x02000A00, 0x02000E00,
                               0x0A000600, 0x0A000200, 0x0E000600, 0x0E000200,
                               0x0A000A00, 0x0A000E00, 0x0E000A00, 0x0E000E00 ]

zaltys_oqpsk_constellation = [ 0x0C000C00, 0x0C000400, 0x04000C00, 0x04000400 ]

zaltys_8qam_constellation = [ 0x06000200, 0x02000600, 0x06000A00, 0x02000E00,
                              0x0A000600, 0x0E000200, 0x0A000E00, 0x0E000A00 ]

zaltys_16apsk_constellation = [ 0x039E039E, 0x0C62039E, 0x039E0C62, 0x0C620C62,
                                0x015304F1, 0x0EAD04F1, 0x01530B0F, 0x0EAD0B0F,
                                0x04F10153, 0x0B0F0153, 0x04F10EAD, 0x0B0F0EAD,
                                0x01260126, 0x0EDA0126, 0x01260EDA, 0x0EDA0EDA ]

zaltys_32apsk_constellation = [ 0x02060206, 0x02C300BD, 0x0DFA0206, 0x0D3D00BD,
                                0x02060DFA, 0x02C30F43, 0x0DFA0DFA, 0x0D3D0F43,
                                0x020604E8, 0x04E80206, 0x0C3F03C1, 0x0AB00000,
                                0x03C10C3F, 0x05500000, 0x0DFA0B18, 0x0B180DFA,
                                0x00BD02C3, 0x00B600B6, 0x0F4302C3, 0x0F4A00B6,
                                0x00BD0D3D, 0x00B60F4A, 0x0F430D3D, 0x0F4A0F4A,
                                0x00000550, 0x03C103C1, 0x0DFA04E8, 0x0B180206,
                                0x02060B18, 0x04E80DFA, 0x00000AB0, 0x0C3F0C3F ]

zaltys_8apsk_constellation = [ 0x00000500, 0x01D501D5, 0x01D5FE2B, 0x05000000,
                               0xFE2B01D5, 0xFB000000, 0x0000FB00, 0xFE2BFE2B ]

zaltys_64qam_constellation = [ 0x05400540, 0x054003C0, 0x03C00540, 0x03C003C0,
                               0x054000C0, 0x05400240, 0x03C000C0, 0x03C00240,
                               0x00C00540, 0x00C003C0, 0x02400540, 0x024003C0,
                               0x00C000C0, 0x00C00240, 0x024000C0, 0x02400240,
                               0x05400AC0, 0x05400C40, 0x03C00AC0, 0x03C00C40,
                               0x05400F40, 0x05400DC0, 0x03C00F40, 0x03C00DC0,
                               0x00C00AC0, 0x00C00C40, 0x02400AC0, 0x02400C40,
                               0x00C00F40, 0x00C00DC0, 0x02400F40, 0x02400DC0,
                               0x0AC00540, 0x0AC003C0, 0x0C400540, 0x0C4003C0,
                               0x0AC000C0, 0x0AC00240, 0x0C4000C0, 0x0C400240,
                               0x0F400540, 0x0F4003C0, 0x0DC00540, 0x0DC003C0,
                               0x0F4000C0, 0x0F400240, 0x0DC000C0, 0x0DC00240,
                               0x0AC00AC0, 0x0AC00C40, 0x0C400AC0, 0x0C400C40,
                               0x0AC00F40, 0x0AC00DC0, 0x0C400F40, 0x0C400DC0,
                               0x0F400AC0, 0x0F400C40, 0x0DC00AC0, 0x0DC00C40,
                               0x0F400F40, 0x0F400DC0, 0x0DC00F40, 0x0DC00DC0 ]

zaltys_os8qam_constellation = [ 0x0400FC00, 0x03940000, 0x00000394, 0x04000400,
                                0x0000FC6C, 0xFC00FC00, 0xFC000400, 0xFC6C0000 ]

zaltys_32qam_constellation = [ 0x04520316, 0x03160452, 0x0452009E, 0x031601DA,
                               0x009E0452, 0x01DA0316, 0x009E01DA, 0x01DA009E,
                               0x04520BAE, 0x03160CEA, 0x04520E26, 0x03160F62,
                               0x009E0CEA, 0x01DA0BAE, 0x009E0F62, 0x01DA0E26,
                               0x0BAE0452, 0x0CEA0316, 0x0BAE01DA, 0x0CEA009E,
                               0x0F620316, 0x0E260452, 0x0F62009E, 0x0E2601DA,
                               0x0BAE0CEA, 0x0CEA0BAE, 0x0BAE0F62, 0x0CEA0E26,
                               0x0F620BAE, 0x0E260CEA, 0x0F620E26, 0x0E260F62 ]

zaltys_c32qam_constellation = [ 0x00E500E5, 0x00E502AF, 0x047902AF, 0x00E50479,
                                0x02AF00E5, 0x02AF02AF, 0x047900E5, 0x02AF0479,
                                0xFF1B00E5, 0xFD5100E5, 0xFD510479, 0xFB8700E5,
                                0xFF1B02AF, 0xFD5102AF, 0xFF1B0479, 0xFB8702AF,
                                0x00E5FF1B, 0x02AFFF1B, 0x02AFFB87, 0x0479FF1B,
                                0x00E5FD51, 0x02AFFD51, 0x00E5FB87, 0x0479FD51,
                                0xFF1BFF1B, 0xFF1BFD51, 0xFB87FD51, 0xFF1BFB87,
                                0xFD51FF1B, 0xFD51FD51, 0xFB87FF1B, 0xFD51FB87 ]

zaltys_c128qam_constellation = [ 0x00710071, 0x00710153, 0x01530071, 0x01530153,
                                 0x00710318, 0x00710235, 0x01530318, 0x01530235,
                                 0x03FA0318, 0x03FA0235, 0x04DC0318, 0x04DC0235,
                                 0x007103FA, 0x007104DC, 0x015303FA, 0x015304DC,
                                 0x03180071, 0x03180153, 0x02350071, 0x02350153,
                                 0x03180318, 0x03180235, 0x02350318, 0x02350235,
                                 0x03FA0071, 0x03FA0153, 0x04DC0071, 0x04DC0153,
                                 0x031803FA, 0x031804DC, 0x023503FA, 0x023504DC,
                                 0xFF8F0071, 0xFEAD0071, 0xFF8F0153, 0xFEAD0153,
                                 0xFCE80071, 0xFDCB0071, 0xFCE80153, 0xFDCB0153,
                                 0xFCE803FA, 0xFDCB03FA, 0xFCE804DC, 0xFDCB04DC,
                                 0xFC060071, 0xFB240071, 0xFC060153, 0xFB240153,
                                 0xFF8F0318, 0xFEAD0318, 0xFF8F0235, 0xFEAD0235,
                                 0xFCE80318, 0xFDCB0318, 0xFCE80235, 0xFDCB0235,
                                 0xFF8F03FA, 0xFEAD03FA, 0xFF8F04DC, 0xFEAD04DC,
                                 0xFC060318, 0xFB240318, 0xFC060235, 0xFB240235,
                                 0x0071FF8F, 0x0153FF8F, 0x0071FEAD, 0x0153FEAD,
                                 0x0318FF8F, 0x0235FF8F, 0x0318FEAD, 0x0235FEAD,
                                 0x0318FC06, 0x0235FC06, 0x0318FB24, 0x0235FB24,
                                 0x03FAFF8F, 0x04DCFF8F, 0x03FAFEAD, 0x04DCFEAD,
                                 0x0071FCE8, 0x0153FCE8, 0x0071FDCB, 0x0153FDCB,
                                 0x0318FCE8, 0x0235FCE8, 0x0318FDCB, 0x0235FDCB,
                                 0x0071FC06, 0x0153FC06, 0x0071FB24, 0x0153FB24,
                                 0x03FAFCE8, 0x04DCFCE8, 0x03FAFDCB, 0x04DCFDCB,
                                 0xFF8FFF8F, 0xFF8FFEAD, 0xFEADFF8F, 0xFEADFEAD,
                                 0xFF8FFCE8, 0xFF8FFDCB, 0xFEADFCE8, 0xFEADFDCB,
                                 0xFC06FCE8, 0xFC06FDCB, 0xFB24FCE8, 0xFB24FDCB,
                                 0xFF8FFC06, 0xFF8FFB24, 0xFEADFC06, 0xFEADFB24,
                                 0xFCE8FF8F, 0xFCE8FEAD, 0xFDCBFF8F, 0xFDCBFEAD,
                                 0xFCE8FCE8, 0xFCE8FDCB, 0xFDCBFCE8, 0xFDCBFDCB,
                                 0xFC06FF8F, 0xFC06FEAD, 0xFB24FF8F, 0xFB24FEAD,
                                 0xFCE8FC06, 0xFCE8FB24, 0xFDCBFC06, 0xFDCBFB24 ]

zaltys_constellation_select = { "BPSK"    : zaltys_bpsk_constellation,
                                "QPSK"    : zaltys_qpsk_constellation,
                                "8PSK"    : zaltys_8psk_constellation,
                                "16QAM"   : zaltys_16qam_constellation,
                                "OQPSK"   : zaltys_oqpsk_constellation,
                                "8QAM"    : zaltys_8qam_constellation,
                                "16APSK"  : zaltys_16apsk_constellation,
                                "32APSK"  : zaltys_32apsk_constellation,
                                "8APSK"   : zaltys_8apsk_constellation,
                                "64QAM"   : zaltys_64qam_constellation,
                                "OS8QAM"  : zaltys_os8qam_constellation,
                                "32QAM"   : zaltys_32qam_constellation,
                                "C32QAM"  : zaltys_c32qam_constellation,
                                "C128QAM" : zaltys_c128qam_constellation }

#
# IESS modem constellations
#
iess_bpsk_constellation = [ 0x00000400, 0x00000C00 ]

iess_qpsk_constellation = [ 0x04000400, 0x0C000400, 0x04000C00, 0x0C000C00 ]

iess_8psk_constellation = [ 0x018803B2, 0x03B20188, 0x0188FC4E, 0x03B2FE78,
                            0xFE78FC4E, 0xFC4EFE78, 0xFE7803B2, 0xFC4E0188 ]

iess_16qam_constellation = [ 0x06000600, 0x06000200, 0x06000A00, 0x06000E00,
                             0x02000600, 0x02000200, 0x02000A00, 0x02000E00,
                             0x0A000600, 0x0A000200, 0x0A000A00, 0x0A000E00,
                             0x0E000600, 0x0E000200, 0x0E000A00, 0x0E000E00 ]

iess_constellation_select = { "BPSK"  : iess_bpsk_constellation,
                              "QPSK"  : iess_qpsk_constellation,
                              "8PSK"  : iess_8psk_constellation,
                              "16QAM" : iess_16qam_constellation }

#
# Alternative modem constellations
#
gray_8psk_constellation = [ 0x018803B2, 0xFE7803B2, 0x0188FC4E, 0xFE78FC4E,
                            0x03B20188, 0xFC4E0188, 0x03B2FE78, 0xFC4EFE78 ]

gray_constellation_select = { "8PSK" : gray_8psk_constellation }

# 
# Legacy mode RRC coefficients
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
# HDRM Modulator driver exceptions
#
class HdrmmDriverError(Exception): pass


#
# HDRM Modulator driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and appropriate base_address value.
#
class HdrmmDriver (object):
    '''
        Configuration wrapper for the Zaltys HDRM Modulator

        Example usage:-
          hdrmm = HdrmmDriver(gateway, base_address=0x100)
          hdrmm.select_constellation_map(modulation_scheme="16QAM", map_scheme="IESS")
          hdrmm.sample_rate = 125e6
          hdrmm.symbol_rate = 10e6
          hdrmm.configure_mod()
    '''
    def __init__(self, smpi_gateway, base_address=0, legacy_mode=True, txfilt_num_taps=49, txfilt_full_coeff_width=14):
        self.smpi_gateway            = smpi_gateway

        # Set hardware configuration parameters
        self.base_address            = base_address
        self.legacy_mode             = legacy_mode
        self.txfilt_num_taps         = txfilt_num_taps
        self.txfilt_full_coeff_width = txfilt_full_coeff_width

        # Set default driver parameters
        self.sample_rate       = 100000000
        self.symbol_rate       = 1000000
        self.constellation_map = zaltys_qpsk_constellation
        self.rrc_alpha         = 20
        self.free_running      = True
        self.offset_mode       = False   # set to True for OQPSK support

    def select_constellation_map(self, modulation_scheme="QPSK", map_scheme="ZALTYS"):
        if map_scheme.upper() == "ZALTYS":
            self.constellation_map = zaltys_constellation_select.get(modulation_scheme)
        elif map_scheme.upper() == "IESS":
            self.constellation_map = iess_constellation_select.get(modulation_scheme)
        elif map_scheme.upper() == "GRAY":
            self.constellation_map = gray_constellation_select.get(modulation_scheme)
        else:
            raise HdrmmDriverError('Unknown map scheme: {}'.format(map_scheme))

        if not self.constellation_map:
            raise HdrmmDriverError('Unknown modulation/mapping scheme: {}/{}'.format(modulation_scheme, map_scheme))
        
    def configure_mod(self):
        bits_per_symbol = int(round(math.log(len(self.constellation_map))/math.log(2)))

        # hold datapath in reset
        self.smpi_gateway.register_write(self.base_address + 0x00, 0x00000001)

        # hold FIFO in reset
        self.smpi_gateway.register_write(self.base_address + 0x04, 0x00010000)

        # symbol mapper setup
        self.smpi_gateway.register_write(self.base_address + 0x06, 0x00010000)
        for pt in self.constellation_map:
            self.smpi_gateway.register_write(self.base_address + 0x07, pt)
        self.smpi_gateway.register_write(self.base_address + 0x06, 0x00000000)
        self.smpi_gateway.register_write(self.base_address + 0x05, 0x00000000)

        # interpolation filter and SPLL setup
        self.smpi_gateway.register_write(self.base_address + 0x10, 0x00000001) # hold SPLL in reset

        sr = self.sample_rate/5
        iif = 0
        while self.symbol_rate > sr:
            sr = sr/2
            iif = iif + 1
        nco = int(round((self.symbol_rate / self.sample_rate) * 2**iif * 2**28))
        self.smpi_gateway.register_write(self.base_address + 0x08, iif)
        self.smpi_gateway.register_write(self.base_address + 0x11, nco)

        self.smpi_gateway.register_write(self.base_address + 0x12, 1024)  # SPLL_LOCK_THRESH
        self.smpi_gateway.register_write(self.base_address + 0x13, 32768) # SPLL_UNLOCK_THRESH
        self.smpi_gateway.register_write(self.base_address + 0x14, 4)     # SPLL_PROP_SHIFT
        self.smpi_gateway.register_write(self.base_address + 0x15, 18)    # SPLL_INTEG_SHIFT

        self.smpi_gateway.register_write(self.base_address + 0x18, 10)    # SPLL_SHIFTADJ_MAX
        self.smpi_gateway.register_write(self.base_address + 0x19, 512)   # SPLL_SHIFTADJ_PERIOD
        self.smpi_gateway.register_write(self.base_address + 0x1A, 2048)  # SPLL_SHIFTADJ_THRESH
        self.smpi_gateway.register_write(self.base_address + 0x1B, 32768) # SPLL_SHIFTADJ_RST_THRESH

        if self.free_running:
            self.smpi_gateway.register_write(self.base_address + 0x10, 0x00000010)  # enable SPLL (free running)
        else:
            self.smpi_gateway.register_write(self.base_address + 0x10, 0x00000000)  # enable SPLL

        # DAC control setup
        self.smpi_gateway.register_write(self.base_address + 0x09, 0x00000302)  # DAC_CTRL
        self.smpi_gateway.register_write(self.base_address + 0x0A, 0x00000000)  # DAC_IOFFSET
        self.smpi_gateway.register_write(self.base_address + 0x0B, 0x00000000)  # DAC_QOFFSET
        self.smpi_gateway.register_write(self.base_address + 0x0C, 0x00000000)  # DAC_GAIN_CAL
        self.smpi_gateway.register_write(self.base_address + 0x0D, 0x00002000)  # DAC_GAIN
        
        # transmit filter setup
        if self.legacy_mode:
            rrc_coeffs = legacy_rrc_select.get(self.rrc_alpha)
            if rrc_coeffs:
                for offset in range(0,24):
                    self.smpi_gateway.register_write(self.base_address + 0x20 + offset, rrc_coeffs[offset] % 65536)
            else:
                raise HdrmmDriverError('Illegal RRC coefficients specification: {}'.format(rrc_coeffs))
        else:
            raise HdrmmDriverError('Non-legacy transmit-filter programming not yet supported!')  # !!! TODO !!!

        if self.offset_mode:
            self.smpi_gateway.register_write(self.base_address + 0x38, 0x00000001)
        else:
            self.smpi_gateway.register_write(self.base_address + 0x38, 0x00000000)
            
        # release FIFO from reset, setting appropriate symbol size
        self.smpi_gateway.register_write(self.base_address + 0x04, bits_per_symbol-1)

        # release datapath from reset
        self.smpi_gateway.register_write(self.base_address + 0x00, 0x00000000)
