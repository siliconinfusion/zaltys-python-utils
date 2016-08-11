##
##  Author        : Paul Onions
##  Creation date : 4 August 2016
##
##  Copyright 2016 Silicon Infusion Limited
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
## Utilities for querying DVB-S2 frame properties
##

import sys

# Private data, see below for API functions
bb_bytes = [
    None,
    None,
    # DVB-S2 QPSK normal & short
    2001,  # 1/4
     384,
    2676,  # 1/3
     654,
    3216,  # 2/5
     789,
    4026,  # 1/2
     879,
    4836,  # 3/5
    1194,
    5380,  # 2/3
    1329,
    6051,  # 3/4
    1464,
    6456,  # 4/5
    1554,
    6730,  # 5/6
    1644,
    7184,  # 8/9
    1779,
    7274,  # 9/10
    None,
    # DVB-S2 8PSK normal & short
    4836,  # 3/5
    1194,
    5380,  # 2/3
    1329,
    6051,  # 3/4
    1464,
    6730,  # 5/6
    1644,
    7184,  # 8/9
    1779,
    7274,  # 9/10
    None,  
    # DVB-S2 16APSK normal & short
    5380,  # 2/3
    1329,
    6051,  # 3/4
    1464,
    6456,  # 4/5
    1554,
    6730,  # 5/6
    1644,
    7184,  # 8/9
    1779,
    7274,  # 9/10
    None,
    # DVB-S2 32APSK normal & short
    6051,  # 3/4
    1464,
    6456,  # 4/5
    1554,
    6730,  # 5/6
    1644,
    7184,  # 8/9
    1779,
    7274,  # 9/10
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    # DVB-S2X QPSK normal
    2316,  # 13/45
    3621,  # 9/20
    4431,  # 11/20
    # DVB-S2X 8APSK normal
    4476,  # 100/180
    4656,  # 104/180
    # DVB-S2X 8PSK normal
    5151,  # 23/36
    5601,  # 25/36
    5826,  # 13/18
    # DVB-S2X 16APSK normal
    4026,  # 90/180
    4296,  # 96/180
    4476,  # 100/180
    4656,  # 26/45
    4836,  # 3/5
    4836,  # 18/30
    5016,  # 28/45
    5151,  # 23/36
    5376,  # 20/30
    5601,  # 25/36
    5826,  # 13/18
    6276,  # 140/180
    6906,  # 154/180
    # DVB-S2X 32APSK normal
    5380,  # 2/3
    None,
    5736,  # 128/180
    5916,  # 132/180
    6276,  # 140/180
    # DVB-S2X 64APSK normal
    5736,  # 128/180
    5916,  # 132/180
    None,
    6276,  # 7/9
    None,
    6456,  # 4/5
    None,
    6730,  # 5/6
    # DVB-S2X 128APSK normal
    6051,  # 135/180
    6276,  # 140/180
    # DVB-S2X 256APSK normal
    5196,  # 116/180
    5376,  # 20/30
    5556,  # 124/180
    5736,  # 128/180
    5916,  # 22/30
    6051,  # 135/180
    # DVB-S2X QPSK short
     474,  # 11/45
     519,  # 4/15
     609,  # 14/45
     924,  # 7/15
    1059,  # 8/15
    1419,  # 32/45
    # DVB-S2X 8PSK short
     924,  # 7/15
    1059,  # 8/15
    1149,  # 26/45
    1419,  # 32/45
    # DVB-S2X 16APSK short
     924,  # 7/15
    1059,  # 8/15
    1149,  # 26/45
    1194,  # 3/5
    1419,  # 32/45
    # DVB-S2X 32APSK short
    1329,  # 2/3
    1419,  # 32/45
    None,
    None,
    None ]

# API functions
def bbframe_byte_length(plsv):
    return bb_bytes[plsv//2]
