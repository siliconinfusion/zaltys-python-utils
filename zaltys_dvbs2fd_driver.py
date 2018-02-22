##
##  Author        : Paul Onions
##  Creation date : 22 February 2018
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
##  A pure python driver for the Zaltys DVB-S2 FEC Decoder.
##
import math

# PLSV indexed information = [bits_per_symbol, code_id]
plsv_infos = {  4: [2, 36],   6: [2, 12],   8: [2, 39],  10: [2, 20],  12: [2, 41],  14: [2, 21],  16: [2, 44],  18: [2, 23],
               20: [2, 52],  22: [2, 28],  24: [2, 58],  26: [2, 30],  28: [2, 67],  30: [2, 32],  32: [2, 71],  34: [2, 33],
               36: [2, 72],  38: [2, 34],  40: [2, 74],  42: [2, 35],  44: [2, 75],  48: [3, 52],  50: [3, 28],  52: [3, 58],
               54: [3, 30],  56: [3, 67],  58: [3, 32],  60: [3, 72],  62: [3, 34],  64: [3, 74],  66: [3, 35],  68: [3, 75],
               72: [4, 52],  74: [4, 28],  76: [4, 58],  78: [4, 30],  80: [4, 67],  82: [4, 32],  84: [4, 72],  86: [4, 34],
               88: [4, 74],  90: [4, 35],  92: [4, 75],  96: [5, 58],  98: [5, 30], 100: [5, 67], 102: [5, 32], 104: [5, 72],
              106: [5, 34], 108: [5, 74], 110: [5, 35], 112: [5, 75], 132: [2, 37], 134: [2, 43], 136: [2, 47], 138: [3, 49],
              140: [3, 51], 142: [3, 56], 144: [3, 61], 146: [3, 64], 148: [4, 45], 150: [4, 46], 152: [4, 49], 154: [4, 50],
              156: [4, 52], 158: [4, 53], 160: [4, 54], 162: [4, 56], 164: [4, 59], 166: [4, 61], 168: [4, 64], 170: [4, 69],
              172: [4, 73], 174: [5, 58], 178: [5, 63], 180: [5, 65], 182: [5, 69], 184: [6, 63], 186: [6, 65], 190: [6, 70],
              194: [6, 71], 198: [6, 72], 200: [7, 68], 202: [7, 69], 204: [8, 57], 206: [8, 59], 208: [8, 60], 210: [8, 63],
              212: [8, 66], 214: [8, 68], 216: [2, 15], 218: [2, 17], 220: [2, 19], 222: [2, 24], 224: [2, 25], 226: [2, 31],
              228: [3, 24], 230: [3, 25], 232: [3, 27], 234: [3, 31], 236: [4, 24], 238: [4, 25], 240: [4, 27], 242: [4, 28],
              244: [4, 31], 246: [5, 24], 248: [5, 25]}
 
# Code-id indexed information = [frame_size, Kldpc, [clks_per_iter @ par_levels 12, 24, 36, 60, 72, 120, 180]
code_infos = {12: [16200,  3240, [ 8424,   4374,   3024,   2010,  1784,  1392,  1290]],
              15: [16200,  3960, [ 8466,   4386,   3026,   1992,  1756,  1371,  1198]],
              17: [16200,  4320, [12537,   6837,   4937,   3417,  3037,  2385,  1989]],
              19: [16200,  5040, [ 9759,   5049,   3479,   2223,  1909,  1503,  1325]],
              20: [16200,  5400, [ 9360,   4830,   3320,   2112,  1810,  1413,  1242]],
              21: [16200,  6480, [ 9963,   5133,   3523,   2235,  1913,  1323,  1167]],
              23: [16200,  7200, [ 8325,   4275,   2925,   1845,  1575,  1065,   861]],
              24: [16200,  7560, [12396,   6666,   4756,   3228,  2846,  2154,  1748]],
              25: [16200,  8640, [12729,   6474,   4389,   2841,  2504,  1893,  1535]],
              27: [16200,  9360, [11571,   5946,   4071,   2649,  2326,  1734,  1393]],
              28: [16200,  9720, [12042,   6102,   4122,   2616,  2272,  1671,  1338]],
              30: [16200, 10800, [ 9135,   4650,   3155,   2025,  1770,  1296,  1029]],
              31: [16200, 11520, [10257,   5187,   3497,   2163,  1837,  1314,  1045]],
              32: [16200, 11880, [ 8028,   4083,   2768,   1758,  1523,  1077,   834]],
              33: [16200, 12600, [ 7590,   3840,   2590,   1590,  1340,   888,   662]],
              34: [16200, 13320, [ 8292,   4182,   2812,   1716,  1442,   927,   722]],
              35: [16200, 14400, [ 8145,   4095,   2745,   1665,  1395,   855,   585]],
              36: [64800, 16200, [33615,  17415,  12015,   7731,  6675,  4617,  3657]],
              37: [64800, 18720, [39012,  20112,  13812,   8772,  7512,  5121,  3928]],
              39: [64800, 21600, [37170,  19140,  13130,   8322,  7120,  4806,  3654]],
              41: [64800, 25920, [39852,  20412,  13932,   8748,  7452,  4899,  3768]],
              43: [64800, 29160, [42471,  21681,  14751,   9207,  7821,  5049,  3759]],
              44: [64800, 32400, [38610,  19710,  13410,   8370,  7110,  4590,  3384]],
              45: [64800, 32400, [43410,  22110,  15010,   9330,  7910,  5070,  3650]],
              46: [64800, 34560, [45216,  22986,  15576,   9648,  8166,  5202,  3720]],
              47: [64800, 35640, [44469,  22599,  15309,   9477,  8019,  5103,  3645]],
              49: [64800, 36000, [43320,  22020,  14920,   9240,  7820,  4980,  3560]],
              50: [64800, 37440, [46284,  23484,  15884,   9804,  8284,  5244,  3724]],
              51: [64800, 37440, [45924,  23304,  15764,   9732,  8224,  5208,  3700]],
              52: [64800, 38880, [48168,  24408,  16488,  10152,  8568,  5400,  3816]],
              53: [64800, 38880, [48108,  24378,  16468,  10140,  8558,  5394,  3812]],
              54: [64800, 40320, [41412,  21012,  14212,   8772,  7412,  4692,  3332]],
              56: [64800, 41400, [39585,  20085,  13585,   8385,  7085,  4485,  3185]],
              57: [64800, 41760, [45636,  23106,  15596,   9600,  8106,  5148,  3664]],
              58: [64800, 43200, [36540,  18540,  12540,   7740,  6540,  4140,  2940]],
              59: [64800, 43200, [47400,  23970,  16160,   9912,  8350,  5238,  3682]],
              60: [64800, 44640, [46044,  23274,  15684,   9612,  8094,  5214,  3774]],
              61: [64800, 45000, [43395,  21945,  14795,   9075,  7645,  4785,  3355]],
              63: [64800, 46080, [45648,  23058,  15528,   9504,  7998,  5178,  3888]],
              64: [64800, 46800, [42450,  21450,  14450,   8850,  7450,  4650,  3250]],
              65: [64800, 47520, [45852,  23142,  15572,   9516,  8002,  5094,  3916]],
              66: [64800, 47520, [46932,  23682,  15932,   9732,  8182,  5124,  3700]],
              67: [64800, 48600, [38205,  19305,  13005,   7965,  6705,  4185,  2925]],
              68: [64800, 48600, [44505,  22455,  15105,   9225,  7755,  4920,  3777]],
              69: [64800, 50400, [47460,  23910,  16060,   9780,  8210,  5070,  3740]],
              70: [64800, 50400, [43560,  21960,  14760,   9000,  7560,  4692,  3342]],
              71: [64800, 51840, [39204,  19764,  13284,   8100,  6804,  4212,  2946]],
              72: [64800, 54000, [39870,  20070,  13470,   8190,  6870,  4230,  2910]],
              73: [64800, 55440, [45774,  23004,  15414,   9342,  7824,  4788,  3270]],
              74: [64800, 57600, [32580,  16380,  10980,   6660,  5580,  3420,  2340]],
              75: [64800, 58320, [32562,  16362,  10962,   6642,  5562,  3402,  2322]]}

#
# DVB-S2 Decoder driver exceptions
#
class Dvbs2fdDriverError(Exception): pass


#
# DVB-S2 FEC Decoder driver class
#
# Instantiate a single instance of this class with an smpi_gateway
# object and appropriate base_address value.
#
class Dvbs2fdDriver (object):
    '''
        Configuration wrapper for the Zaltys DVB-S2 FEC Decoder

        Example usage:-
          dvbs2fd = Dvbs2fdDriver(gateway, base_address=0x100, sysclk=200e6, par_level=180)
          dvbs2fd.symbol_rate = 10e6
          dvbs2fd.configure_dec()
    '''
    def __init__(self, smpi_gateway, base_address=0, sysclk=200e6, par_level=180):
        self.smpi_gateway = smpi_gateway

        # Set hardware configuration parameters
        self.base_address = base_address
        self.sysclk       = sysclk
        self.par_level    = par_level

        # Set default driver parameters
        self.symbol_rate = 1000000

    def configure_dec(self):
        # Hold datapath in reset
        self.smpi_gateway.register_write(self.base_address + 0x00, 0x00000001)

        # Set max iterations at this symbol rate for each PLSV
        par_idx = {12:0, 24:1, 36:2, 60:3, 72:4, 120:5, 180:6}.get(self.par_level, None)
        if par_idx:
            for plsv in range(0,512,2):
                plsv_info = plsv_infos.get(plsv, None)

                if plsv_info:
                    bits_per_sym = plsv_info[0]
                    code_idx = plsv_info[1]
                    fsize = code_infos.get(code_idx)[0]
                    kldpc = code_infos.get(code_idx)[1]
                    clks = code_infos.get(code_idx)[2][par_idx]
                    par = self.par_level

                    avail = (self.sysclk/self.symbol_rate)*(fsize/bits_per_sym)
                    ovhd = (kldpc/par)*math.ceil(par/8) + (360/par)*(par+9)*math.ceil((fsize-kldpc)/2880) + 2*fsize/par + 500
                    max_iters = int(min(math.floor((avail-ovhd)/clks)-1,255))
                else:
                    max_iters = 50

                self.smpi_gateway.register_write(self.base_address + 0x04, (plsv << 16) + 1)
                self.smpi_gateway.register_write(self.base_address + 0x05, max_iters)
        else:
            raise Dvbs2fdDriverError('Illegal par_level: {}, only 12, 24, 36, 60, 72, 120, or 180 supported'.format(self.par_level))

        # Release datapath from reset
        self.smpi_gateway.register_write(self.base_address + 0x00, 0x00000000)
