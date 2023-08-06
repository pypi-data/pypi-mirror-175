import ctypes
import os
import logging
from logging.config import fileConfig
from time import sleep

# Setup logger
log_file_path = os.path.join(os.path.abspath('./'), 'logging.conf')
fileConfig(log_file_path)
logger = logging.getLogger('signer')

def setup_se_interface():
    _lib = ctypes.CDLL(os.path.dirname(__file__)+"/libse_interface.so")

    _lib.wrap_block2go_select.argtypes = [ ctypes.POINTER(ctypes.c_uint8),
                                           ctypes.POINTER(ctypes.c_char_p)]
    _lib.wrap_gen_key.argtypes = [  ctypes.POINTER(ctypes.c_uint8) ]
    
    _lib.wrap_get_pub_key.argtypes = [ ctypes.c_uint8, 
                                       ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
                                       ctypes.POINTER(ctypes.c_uint8)] 
                                       
    _lib.wrap_sign.argtypes = [ ctypes.c_uint8, 
                                ctypes.POINTER(ctypes.c_uint8),
                                ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
                                ctypes.POINTER(ctypes.c_uint16) ]
    
    return _lib

def init():
    global se_interface
    se_interface = setup_se_interface()
    ret = se_interface.se_interface_init()
    if(ret):
        raise Exception(f"Signer init error {ret}")
    
    return ret
    

def block2go_select():
    
    id_nr = (ctypes.c_uint8 * 11)()
    version = (ctypes.c_char_p)()
    
    ret = se_interface.wrap_block2go_select(id_nr, version)
    if(ret):
        raise Exception(f"Signer select error {ret}")
    
    return ret

def block2go_gen_key():
    c_key_index = (ctypes.c_uint8 * 1)()
    ret = se_interface.wrap_gen_key(c_key_index)
    if(ret):
        print("genkeys error\n")
    
    return c_key_index[0]

def block2go_get_pub_key(key_index):
    c_key_index = ctypes.c_uint8()
    c_key_index.value = key_index
    c_public_key = ctypes.POINTER(ctypes.c_uint8)()
    c_public_key_len = ctypes.c_uint8()
   
    ret = se_interface.wrap_get_pub_key(c_key_index, c_public_key, c_public_key_len)

    if(ret):
        print("get public key error\n")
        
    return c_public_key[0:c_public_key_len.value]
    
def block2go_sign(key_index, msg):
    logger.debug("Signing message")
    c_key_index = ctypes.c_uint8()
    c_key_index.value = key_index
    c_msg = (ctypes.c_uint8) * 32
    c_msg = c_msg(*msg)
    c_sig = ctypes.POINTER(ctypes.c_uint8)()
    c_sig_len = ctypes.c_uint16()
    ret = se_interface.wrap_sign(key_index, c_msg, c_sig, c_sig_len)
    
    if(ret):
        raise Exception(f'Sign error {ret}')
    else:
        der_sig = c_sig[0:c_sig_len.value]
        rlen_index = 3 # 4th byte
        rlen = der_sig[rlen_index]
        r_index = rlen_index + 1
        r = der_sig[r_index:r_index+rlen]
        if rlen == 33:
            r = r[1:]
        slen_index = r_index+rlen+1
        slen = der_sig[slen_index]
        s_index = slen_index+1
        s= der_sig[s_index:s_index+slen]
        return r+s

    
