#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CBC 比特翻转示例（纯 Python，只需 PyCryptodome）
================================================

场景：应用把 `user=guest&amount=100` 加密成 AES-CBC 密文后传给客户端，
客户端回传时服务端直接解密并信任明文。攻击者不需要密钥，只要知道
其中一段明文，就能翻转它。

原理：CBC 解密时 P[i] = D(C[i]) XOR C[i-1]，所以改动前一个密文块
（第一块改 IV）的对应字节，就能精确控制当前块的明文字节。

运行：
    python examples/cbc_bit_flipping_demo.py
或：
    python crypto_attack_machine.py run cbc/bit_flipping --script examples/cbc_bit_flipping_demo.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.realpath(__file__))
_PARENT = os.path.dirname(_HERE)
_ROOT = _PARENT if os.path.isdir(os.path.join(_PARENT, "attacks")) else os.path.dirname(_HERE)
sys.path.insert(1, _ROOT)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from attacks.cbc import bit_flipping

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")  # 服务端密钥，攻击者并不知道
IV = bytes(16)
MESSAGE = b"user=guest&amount=100"


def encrypt(iv, plaintext):
    return AES.new(KEY, AES.MODE_CBC, bytes(iv)).encrypt(pad(plaintext, AES.block_size))


def decrypt(iv, ciphertext):
    return unpad(AES.new(KEY, AES.MODE_CBC, bytes(iv)).decrypt(bytes(ciphertext)), AES.block_size)


def main():
    ciphertext = encrypt(IV, MESSAGE)
    print(f"原始明文 : {MESSAGE.decode()}")
    print(f"IV       : {IV.hex()}")
    print(f"密文     : {ciphertext.hex()}")

    # 我们想把 "guest" 改成 "admin"，两者等长（5 字节）
    original = b"guest"
    forged = b"admin"
    position = MESSAGE.index(original)

    iv_, c_ = bit_flipping.attack(IV, ciphertext, position, original, forged)
    tampered = decrypt(iv_, c_)

    print(f"\n翻转位置 : {position}  ({original.decode()} -> {forged.decode()})")
    print(f"伪造 IV  : {bytes(iv_).hex()}")
    print(f"伪造密文 : {bytes(c_).hex()}")
    print(f"服务端解密出 : {tampered.decode()}")

    assert tampered == b"user=admin&amount=100", tampered
    print("\n[+] 攻击成功：明文被改成了 user=admin，且未触发任何解密错误。")


if __name__ == "__main__":
    main()
