##
##  Author        : Paul Onions
##  Creation date : 8 November 2016
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
##  A python wrapper for the libgse library, for testing purposes only.
##

from ctypes import CDLL, c_ubyte, c_ushort, c_uint, c_size_t, c_void_p, POINTER, byref


#
# Constants
#
gse_max_header_length  = 13
gse_max_trailer_length = 4


#
#  LibgseWrapper exceptions
#
class LibgseWrapperError(Exception): pass


#
# LibgseWrapper class
#
class LibgseWrapper (object):
    '''
        Wrapper for the libgse library.

        Example usage:-
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
    '''
    def __init__(self, num_channels=1, fifo_size=1024, libgse_path="/usr/lib/libgse.so"):
        self.num_channels = num_channels
        self.fifo_size = fifo_size
        self.libgse = CDLL(libgse_path)

        # Initialize libgse interface
        self.libgse.gse_create_vfrag_with_data.argtypes = [POINTER(c_void_p), c_size_t, c_size_t, c_size_t, POINTER(c_ubyte), c_size_t]
        self.libgse.gse_create_vfrag_with_data.restype  = c_ushort
        
        self.libgse.gse_get_vfrag_start.argtypes = [c_void_p]
        self.libgse.gse_get_vfrag_start.restype  = POINTER(c_ubyte)

        self.libgse.gse_get_vfrag_length.argtypes = [c_void_p]
        self.libgse.gse_get_vfrag_length.restype  = c_size_t

        self.libgse.gse_free_vfrag.argtypes = [POINTER(c_void_p)]
        self.libgse.gse_free_vfrag.restype  = c_ushort

        self.libgse.gse_encap_init.argtypes = [c_ubyte, c_size_t, POINTER(c_void_p)]
        self.libgse.gse_encap_init.restype  = c_ushort

        self.libgse.gse_encap_receive_pdu.argtypes = [c_void_p, c_void_p, c_ubyte*6, c_ubyte, c_ushort, c_ubyte]
        self.libgse.gse_encap_receive_pdu.restype  = c_ushort

        self.libgse.gse_encap_get_packet_copy.argtypes = [POINTER(c_void_p), c_void_p, c_size_t, c_ubyte]
        self.libgse.gse_encap_get_packet_copy.restype  = c_ushort

        self.libgse.gse_encap_get_packet_copy.argtypes = [POINTER(c_void_p), c_void_p, c_size_t, c_ubyte]
        self.libgse.gse_encap_get_packet_copy.restype  = c_ushort

        self.libgse.gse_encap_release.argtypes = [c_void_p]
        self.libgse.gse_encap_release.restype  = c_ushort

        self.libgse.gse_deencap_init.argtypes = [c_ubyte, POINTER(c_void_p)]
        self.libgse.gse_deencap_init.restype  = c_ushort

        self.libgse.gse_deencap_packet.argtypes = [c_void_p, c_void_p, POINTER(c_ubyte), c_ubyte*6, POINTER(c_ushort), POINTER(c_void_p), POINTER(c_ushort)]
        self.libgse.gse_deencap_packet.restype  = c_ushort

        self.libgse.gse_deencap_release.argtypes = [c_void_p]
        self.libgse.gse_deencap_release.restype  = c_ushort

        # Allocate C data storage
        self.c_encap_state   = c_void_p()
        self.c_deencap_state = c_void_p()

        self.c_pdu_vfrag = c_void_p()
        self.c_gse_vfrag = c_void_p()
        self.c_data      = (c_ubyte*65536)()
        self.c_label     = (c_ubyte*6)()
        self.c_labeltype = c_ubyte()
        self.c_protocol  = c_ushort()
        self.c_len       = c_ushort()

        # Initialize Rx PDU queues
        self.rx_pdus = [[]]*num_channels

        # Initialize encapsulator and deencapsulator
        status = self.libgse.gse_encap_init(self.num_channels, self.fifo_size, byref(self.c_encap_state))
        if status != 0:
            raise LibgseWrapperError('libgse/gse_encap_init: {}'.format(hex(status)))

        status = self.libgse.gse_deencap_init(self.num_channels, byref(self.c_deencap_state))
        if status != 0:
            self.libgse.gse_encap_release(self.c_encap_state)
            raise LibgseWrapperError('libgse/gse_deencap_init: {}'.format(hex(status)))

    def __del__(self):
        self.libgse.gse_encap_release(self.c_encap_state)
        self.libgse.gse_deencap_release(self.c_deencap_state)

    def encap_push_pdu(self, pdu_bytes, channel=0, label=[1,2,3,4,5,6], protocol=0x0800):
        '''
            Push a PDU into the Tx packet buffer
            The contents of the PDU, pdu_bytes, should be a sequence of bytes.
        '''
        if channel < 0 or channel >= self.num_channels:
            raise LibgseWrapperError('Channel number out of range: {}'.format(channel))
        if len(label) != 6:
            raise LibgseWrapperError('Only 6-byte labels supported: {}'.format(label))

        num_bytes = min(len(pdu_bytes), 65536)
        for n in range(num_bytes):
            self.c_data[n] = pdu_bytes[n]

        for n in range(6):
            self.c_label[n] = label[n]

        self.c_labeltype = c_ubyte(0)

        self.c_protocol = c_ushort(protocol)

        status = self.libgse.gse_create_vfrag_with_data(byref(self.c_pdu_vfrag), num_bytes, gse_max_header_length, gse_max_trailer_length, self.c_data, num_bytes)
        if status != 0:
            raise LibgseWrapperError('libgse/gse_create_vfrag_with_data: {}'.format(hex(status)))

        status = self.libgse.gse_encap_receive_pdu(self.c_pdu_vfrag, self.c_encap_state, self.c_label, self.c_labeltype, self.c_protocol, channel)
        if status != 0:
            raise LibgseWrapperError('libgse/gse_encap_receive_pdu: {}'.format(hex(status)))

    def encap_pop_gse(self, max_bytes=4096, channel=0):
        '''
            Pop a GSE packet no bigger than max_bytes from the Tx packet buffer.
            Returns a list of byte values if the buffer is non-empty,
            otherwise an empty list.
        '''
        if channel < 0 or channel >= self.num_channels:
            raise LibgseWrapperError('Channel number out of range: {}'.format(channel))

        status = self.libgse.gse_encap_get_packet_copy(byref(self.c_gse_vfrag), self.c_encap_state, max_bytes, channel)
        if status == 0x0302:  # buffer empty
            return []
        elif status != 0:
            raise LibgseWrapperError('libgse/gse_encap_get_packet_copy: {}'.format(hex(status)))

        buf = self.libgse.gse_get_vfrag_start(self.c_gse_vfrag)
        lng = self.libgse.gse_get_vfrag_length(self.c_gse_vfrag)

        pkt = [0]*lng
        for n in range(lng):
            pkt[n] = buf[n]

        # remove unnecessary padding bytes added by libgse
        gse_len = (pkt[0] % 16)*256 + pkt[1]
        gse_pkt = pkt[0:gse_len+2]

        status = self.libgse.gse_free_vfrag(self.c_gse_vfrag)
        if status != 0:
            raise LibgseWrapperError('libgse/gse_free_vfrag: {}'.format(hex(status)))

        return gse_pkt

    def decap_push_gse(self, pkt, channel=0):
        '''
            Push a GSE packet (sequence of byte values) into the Rx packet buffer.
        '''
        if channel < 0 or channel >= self.num_channels:
            raise LibgseWrapperError('Channel number out of range: {}'.format(channel))

        num_bytes = min(len(pkt), 65536)
        for n in range(num_bytes):
            self.c_data[n] = pkt[n]

        status = self.libgse.gse_create_vfrag_with_data(self.c_gse_vfrag, num_bytes, 0, 0, self.c_data, num_bytes)
        if status != 0:
            raise LibgseWrapperError('libgse/gse_create_vfrag_with_data: {}'.format(hex(status)))

        status = self.libgse.gse_deencap_packet(self.c_gse_vfrag, self.c_deencap_state, byref(self.c_labeltype), self.c_label, byref(self.c_protocol), byref(self.c_pdu_vfrag), byref(self.c_len))
        if status == 0x0901:  # PDU completed
            buf = self.libgse.gse_get_vfrag_start(self.c_pdu_vfrag)
            lng = self.libgse.gse_get_vfrag_length(self.c_pdu_vfrag)

            label = [0]*6
            for n in range(6):
                label[n] = self.c_label[n]

            protocol = self.c_protocol.value

            pdu_bytes = [0]*lng
            for n in range(lng):
                pdu_bytes[n] = buf[n]

            self.rx_pdus[channel].append([label, protocol, pdu_bytes])
        elif status != 0:
            raise LibgseWrapperError('libgse/gse_deencap_packet: {}'.format(hex(status)))

    def decap_pop_pdu(self, channel=0):
        '''
            Pop a PDU from the Rx packet buffer.
            Returns a list of three items: a 6-element list of label
            byte values, an integer representing the protocol type, and
            another list of byte values representing the contents of the PDU.
            If the buffer is empty (no PDUs available), then returns an empty list.
        '''
        if channel < 0 or channel >= self.num_channels:
            raise LibgseWrapperError('Channel number out of range: {}'.format(channel))

        if len(self.rx_pdus[channel]) > 0:
            return self.rx_pdus[channel].pop()
        else:
            return []

