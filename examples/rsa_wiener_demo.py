#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wiener 攻击示例（需要 SageMath）
================================

当 RSA 的私钥指数 d 过小（d < N^0.25 / 3）时，e/N 的连分数展开中会出现
k/d 的收敛项，从而可以直接恢复 d 并分解 N。

这里用 Boneh 教材里的经典小例子：
    N = 90581 = 239 * 379,  e = 17993,  d = 5

运行：
    sage -python examples/rsa_wiener_demo.py
或：
    python crypto_attack_machine.py run rsa/wiener_attack --script examples/rsa_wiener_demo.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.realpath(__file__))
_PARENT = os.path.dirname(_HERE)
_ROOT = _PARENT if os.path.isdir(os.path.join(_PARENT, "attacks")) else _HERE
sys.path.insert(1, _ROOT)

from sage.all import ZZ  # noqa: F401  确认当前解释器是 Sage 的 python

from attacks.rsa import wiener_attack

N = 90581
e = 17993


def main():
    print(f"N = {N}")
    print(f"e = {e}")
    print("真实 d = 5（远小于 N^0.25 ≈ 17.3，满足 Wiener 攻击条件）\n")

    result = wiener_attack.attack(N, e)
    if result is None:
        raise SystemExit("攻击失败：参数不满足条件")

    p, q, d = result
    print(f"恢复出 p = {p}")
    print(f"恢复出 q = {q}")
    print(f"恢复出 d = {d}")

    assert p * q == N
    assert pow(pow(2, e, N), d, N) == 2

    plaintext = 12345  # 任意小于 N 的消息
    ciphertext = pow(plaintext, e, N)
    assert pow(ciphertext, d, N) == plaintext

    print(f"\n[+] 攻击成功：用恢复的 d 解开了示例密文 {ciphertext} -> {plaintext}")


if __name__ == "__main__":
    main()
