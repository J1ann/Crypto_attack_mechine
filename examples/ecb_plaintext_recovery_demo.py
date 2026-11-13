#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECB 明文恢复示例（纯 Python，只需 PyCryptodome）
=================================================

场景：服务端把 `用户输入 + 秘密` 用 AES-ECB 加密后返回。ECB 对相同
16 字节块产生相同密文，且块之间互不影响，于是可以"一次喂一个字节"，
把秘密逐字节爆破出来。

步骤（本次只演示恢复，不重复造轮子）：
    1. 构造明文使目标字节落在某个块的最后一格；
    2. 枚举该字节 0..255，找到与前一块密文相同的那个；
    3. 逐字节推进，直到遇到"凑不出"的情况，说明秘密已到末尾。

运行：
    python examples/ecb_plaintext_recovery_demo.py
"""

import os
import secrets
import sys

_HERE = os.path.dirname(os.path.realpath(__file__))
_PARENT = os.path.dirname(_HERE)
_ROOT = _PARENT if os.path.isdir(os.path.join(_PARENT, "attacks")) else _HERE
sys.path.insert(1, _ROOT)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from attacks.ecb import plaintext_recovery

KEY = secrets.token_bytes(16)
SECRET = b"flag{ecb_is_not_semantic_secure}"  # 服务端拼在用户输入后面的秘密


def encrypt_oracle(plaintext: bytes) -> bytes:
    """服务端行为：AES-ECB(user_input + secret)，攻击者只掌握这个函数。"""
    return AES.new(KEY, AES.MODE_ECB).encrypt(pad(bytes(plaintext) + SECRET, AES.block_size))


def main():
    print(f"秘密长度 : {len(SECRET)} 字节")
    print(f"真实秘密 : {SECRET.decode()}")

    recovered = plaintext_recovery.attack(encrypt_oracle)
    print(f"恢复结果 : {recovered.decode()}")

    assert recovered == SECRET, (recovered, SECRET)
    print("\n[+] 攻击成功：无需密钥，仅凭加密预言机就还原了全部明文。")


if __name__ == "__main__":
    main()
