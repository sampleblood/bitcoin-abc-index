#!/usr/bin/env python3
# Copyright (c) 2016-2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Encode and decode BASE58, P2PKH and P2SH addresses."""

from .script import CScript, hash160, hash256
from .util import hex_str_to_bytes

chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
b58len = len(chars)


def byte_to_base58(b, version):
    result = ''
    str = b.hex()
    str = chr(version).encode('latin-1').hex() + str
    checksum = hash256(hex_str_to_bytes(str)).hex()
    str += checksum[:8]
    value = int('0x' + str, 0)
    while value > 0:
        result = chars[value % 58] + result
        value //= 58
    while (str[:2] == '00'):
        result = chars[0] + result
        str = str[2:]
    return result

# TODO: def base58_decode
# base58地址decode成bytes


def decode(v, length=None):
    """ decode v into a string of len bytes
    """
    long_value = 0
    for i, c in enumerate(v[::-1]):
        pos = chars.find(c)
        assert pos != -1
        long_value += pos * (b58len**i)

    result = bytes()
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = bytes((mod,)) + result
        long_value = div
    result = bytes((long_value, )) + result

    nPad = 0
    for c in v:
        if c == chars[0]:
            nPad += 1
            continue
        break

    result = bytes(nPad) + result
    if length is not None and len(result) != length:
        return None

    return result


def keyhash_to_p2pkh(hash, main=False):
    assert (len(hash) == 20)
    version = 0 if main else 111
    return byte_to_base58(hash, version)


def scripthash_to_p2sh(hash, main=False):
    assert (len(hash) == 20)
    version = 5 if main else 196
    return byte_to_base58(hash, version)


def key_to_p2pkh(key, main=False):
    key = check_key(key)
    return keyhash_to_p2pkh(hash160(key), main)


def script_to_p2sh(script, main=False):
    script = check_script(script)
    return scripthash_to_p2sh(hash160(script), main)


def check_key(key):
    if (isinstance(key, str)):
        key = hex_str_to_bytes(key)  # Assuming this is hex string
    if (isinstance(key, bytes) and (len(key) == 33 or len(key) == 65)):
        return key
    assert False


def check_script(script):
    if (isinstance(script, str)):
        script = hex_str_to_bytes(script)  # Assuming this is hex string
    if (isinstance(script, bytes) or isinstance(script, CScript)):
        return script
    assert False
