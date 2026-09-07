# AGPL-3.0 License. Copyright © 2026 Ellen Red


import os
import binascii
from hashlib import sha256
import codecs
import bech32m
import andrea
import ecc
import core


def gen_orig_pri():
    while True:
        orig_pri = int.from_bytes(os.urandom(32), 'big')
        if 1 <= orig_pri <= ecc.constants.n - 1:       
            return orig_pri        
            break
        return orig_pri
    

def tweak():
    while True:
        try:
            orig_pri_int = gen_orig_pri()
        
            # 1. Generate P = orig_pri * G
            public_tuple = andrea.scalar_mult(orig_pri_int, ecc.constants.g)
            
            # Pb_int is just the X coordinate used for hashing, keep as is
            untweak_pubx_int = public_tuple[0]
            untweak_pubx__bytes = core.bytes_from_int(untweak_pubx_int)
            
            # 2. Calculate tweak t
            tweak = core.tagged_hash("TapTweak", untweak_pubx__bytes)
            tweak_int = int.from_bytes(tweak, 'big') 
            
            # 3. Calculate tG = t * G
            tag_generator_tuple = andrea.scalar_mult(tweak_int, ecc.constants.g)            
            
            # Perform Point Addition P + tG
            # If the result is a tuple (x, y), we take the x coordinate.
            tweak_pubx_tuple = andrea.point_add(public_tuple, tag_generator_tuple)
            tweak_pubx_int = tweak_pubx_tuple[0]
            tweak_pubx_bytes = core.bytes_from_int(tweak_pubx_int)
            tweak_pubx_hex = tweak_pubx_bytes.hex() 

            # Tweak Private Key: privkey + tweak
            # This addition happens in the scalar field (modulo order n)
            n = ecc.constants.n # The order of the curve group
            tweak_pri_int = (orig_pri_int + tweak_int) % n
            tweak_pri_bytes = core.bytes_from_int(tweak_pri_int)  
            tweak_pri_hex = tweak_pri_bytes.hex()            
            return tweak_pri_hex, tweak_pubx_hex 
            break        
        
        except Exception as e:            
            return f'Error occurred: {e}'

def iden():
    tweaked_privkey, tweaked_pubkey = tweak()          
    hrp = "tb" 
    wit_ver = 1
    wit_prog = binascii.unhexlify(tweaked_pubkey)
    addr = bech32m.encode(hrp, wit_ver, wit_prog)            
    return addr, tweaked_privkey, tweaked_pubkey


