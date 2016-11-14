##
##  Author        : Paul Onions
##  Creation date : 14 November 2016
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
##  Test example for the libgse wrapper.
##
##  Invoke at a shell prompt with:-
##    python libgse_wrapper_test.py
##

from libgse_wrapper import LibgseWrapper


# create encapsulator/decapsulator
gse = LibgseWrapper()

# create PDU
pdu_label = [0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45]
pdu_protocol = 0x1234
pdu_bytes = [0xA5]*60

# encapsulate into very small GSE packets
gse.encap_push_pdu(pdu_bytes, label=pdu_label, protocol=pdu_protocol)
gse_pkt1 = gse.encap_pop_gse(max_bytes=50)
gse_pkt2 = gse.encap_pop_gse(max_bytes=50)

# decapsulate back into PDU
gse.decap_push_gse(gse_pkt1)
gse.decap_push_gse(gse_pkt2)
pdu = gse.decap_pop_pdu()
rx_pdu_label = pdu[0]
rx_pdu_protocol = pdu[1]
rx_pdu_bytes = pdu[2]
