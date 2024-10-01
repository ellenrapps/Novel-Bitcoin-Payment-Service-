# AGPL-3.0 License. Copyright © 2024 Ellen Red. All rights reserved.


import os
import binascii
from hashlib import sha256
import codecs
import bech32m
import andrea
import ecc
import core


def pri_orig():
    while True:
        orig_pri = int.from_bytes(os.urandom(32), 'big')
        if 1 <= orig_pri <= ecc.constants.n - 1:        
            return orig_pri        
            break

# Reference: https://bitcoin.stackexchange.com/questions/116384/what-are-the-steps-to-convert-a-private-key-to-a-taproot-address/116391#116391
def tweak():
    while True:
        try:
            orig_pri_int = pri_orig()            
            # Tweak
            public_tuple = andrea.scalar_mult(orig_pri_int, ecc.constants.g) #  P = privkey * G
            untweak_pubx_int = public_tuple[0]
            untweak_pubx__bytes = core.bytes_from_int(untweak_pubx_int) # Let Pb be the serialization of P in x-only form: that's just the 32-byte big endian encoding of its X coordinate
            pre_tweak_bytes = sha256("TapTweak".encode()).digest()
            tweak_bytes = sha256(pre_tweak_bytes + pre_tweak_bytes + untweak_pubx__bytes).digest() # Compute the tweak t = SHA256(SHA256("TapTweak") || SHA256("TapTweak") || Pb), interpreted as 32-byte big endian encoded integer
            tweak_int = int.from_bytes(tweak_bytes)
            # Tweak Pri -> Compute private key as privkey + t
            tweak_pri_int = orig_pri_int + tweak_int
            tweak_pri_bytes = core.bytes_from_int(tweak_pri_int)
            tweak_pri_hex = tweak_pri_bytes.hex()
            tweak_pri_ascii = bytes(tweak_pri_hex, encoding="ascii")
            tweak_pri_codec = codecs.encode(tweak_pri_ascii, 'hex')
            # Tweak Pubx -> Compute the tweaked public key Q = P + (t * G)
            tag_generator_tuple = andrea.scalar_mult(tweak_int, ecc.constants.g)
            tag_generatorx_int = tag_generator_tuple[0]
            tweak_pubx_int = untweak_pubx_int + tag_generatorx_int
            tweak_pubx_bytes = core.bytes_from_int(tweak_pubx_int) # Loop corrects the overflow
            tweak_pubx_hex = tweak_pubx_bytes.hex()
            return tweak_pri_hex, tweak_pri_codec, tweak_pubx_hex
            break        
        except:
            pass


def iden():
    tweak_pri_hex, tweak_pri_codec, tweak_pubx_hex = tweak()          
    hrp = "tb" 
    wit_ver = 1
    wit_prog = binascii.unhexlify(tweak_pubx_hex)
    addr = bech32m.encode(hrp, wit_ver, wit_prog)            
    return addr, tweak_pri_hex, tweak_pri_codec, tweak_pubx_hex



