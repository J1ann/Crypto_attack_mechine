# 攻击总览

> 本文件由 `python crypto_attack_machine.py docs` 自动生成，请勿手工编辑。

共 **73** 个攻击，覆盖 **22** 个分类。

### ACD · 近似公因数（3）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Multivariate Polynomial Attack](attacks/acd/mp.py) | `acd/mp` | `attack(N, a, rho, t=1, k=1, roots_method='groebner')` | ✅ |
| [Orthogonal Based Attack](attacks/acd/ol.py) | `acd/ol` | `attack(x, rho)` | ✅ |
| [Simultaneous Diophantine Approximation](attacks/acd/sda.py) | `acd/sda` | `attack(x, rho)` | ✅ |

### CBC 分组模式（3）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Bit Flipping Attack](attacks/cbc/bit_flipping.py) | `cbc/bit_flipping` | `attack(iv, c, pos, p, p_)` | ✅ |
| [IV Recovery](attacks/cbc/iv_recovery.py) | `cbc/iv_recovery` | `attack(decrypt_oracle)` | ✅ |
| [Padding Oracle Attack](attacks/cbc/padding_oracle.py) | `cbc/padding_oracle` | `attack(padding_oracle, iv, c)` | ✅ |

### CBC + CBC-MAC（3）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Key Reuse (Encrypt-and-MAC)](attacks/cbc_and_cbc_mac/eam_key_reuse.py) | `cbc_and_cbc_mac/eam_key_reuse` | `attack(decrypt_oracle, iv, c, t)` | ✅ |
| [Key Reuse (Encrypt-then-MAC)](attacks/cbc_and_cbc_mac/etm_key_reuse.py) | `cbc_and_cbc_mac/etm_key_reuse` | `attack(encrypt_oracle, decrypt_oracle, iv, c, t)` | ✅ |
| [Key Reuse (MAC-then-Encrypt)](attacks/cbc_and_cbc_mac/mte_key_reuse.py) | `cbc_and_cbc_mac/mte_key_reuse` | `attack(decrypt_oracle, iv, c, encrypted_zeroes)` | ✅ |

### CBC-MAC（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Length Extension Attack](attacks/cbc_mac/length_extension.py) | `cbc_mac/length_extension` | `attack(m1, t1, m2, t2)` | ✅ |

### CTR 分组模式（3）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Bit Flipping Attack](attacks/ctr/bit_flipping.py) | `ctr/bit_flipping` | `attack(c, pos, p, p_)` | ✅ |
| [CRIME Attack](attacks/ctr/crime.py) | `ctr/crime` | `attack(encrypt_oracle, known_prefix, padding_byte)` | ✅ |
| [Separator Oracle Attack](attacks/ctr/separator_oracle.py) | `ctr/separator_oracle` | `attack(separator_oracle, separator_byte, c)` | ✅ |

### ECB 分组模式（3）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Plaintext Recovery](attacks/ecb/plaintext_recovery.py) | `ecb/plaintext_recovery` | `attack(encrypt_oracle, unused_byte=0)` | ✅ |
| [Plaintext Recovery (Harder)](attacks/ecb/plaintext_recovery_harder.py) | `ecb/plaintext_recovery_harder` | `attack(encrypt_oracle, unused_byte=0)` | ✅ |
| [Plaintext Recovery (Hardest)](attacks/ecb/plaintext_recovery_hardest.py) | `ecb/plaintext_recovery_hardest` | `attack(encrypt_oracle, unused_byte=0)` | ✅ |

### ECC · 椭圆曲线（6）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [ECDSA Nonce Reuse](attacks/ecc/ecdsa_nonce_reuse.py) | `ecc/ecdsa_nonce_reuse` | `attack(n, m1, r1, s1, m2, r2, s2)` | ✅ |
| [Frey-Rück Attack](attacks/ecc/frey_ruck_attack.py) | `ecc/frey_ruck_attack` | `attack(P, R, max_k=6, max_tries=10)` | ✅ |
| [MOV Attack](attacks/ecc/mov_attack.py) | `ecc/mov_attack` | `attack(P, R, max_k=6, max_tries=10)` | ✅ |
| [Parameter Recovery](attacks/ecc/parameter_recovery.py) | `ecc/parameter_recovery` | `attack(p, x1, y1, x2, y2)` | ✅ |
| [Singular Curve Attack](attacks/ecc/singular_curve.py) | `ecc/singular_curve` | `attack(p, a2, a4, a6, Gx, Gy, Px, Py)` | ✅ |
| [Smart's Attack](attacks/ecc/smart_attack.py) | `ecc/smart_attack` | `attack(G, P)` | ✅ |

### ElGamal 加密（2）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Nonce Reuse Attack](attacks/elgamal_encryption/nonce_reuse.py) | `elgamal_encryption/nonce_reuse` | `attack(p, m1, c1, d1, c2, d2)` | ✅ |
| [Unsafe Generator Attack](attacks/elgamal_encryption/unsafe_generator.py) | `elgamal_encryption/unsafe_generator` | `attack(p, h, c1, c2)` | ✅ |

### ElGamal 签名（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Nonce Reuse Attack](attacks/elgamal_signature/nonce_reuse.py) | `elgamal_signature/nonce_reuse` | `attack(p, m1, r1, s1, m2, r2, s2)` | ✅ |

### 整数分解（12）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Base Conversion Attack (+1)](attacks/factorization/base_conversion.py) | `factorization/base_conversion` | `factorize(N, coefficient_threshold=32)` | ✅ |
| [Branch And Prune Attack (+2)](attacks/factorization/branch_and_prune.py) | `factorization/branch_and_prune` | `factorize_pq(N, p, q)` | ✅ |
| [Complex Multiplication Attack](attacks/factorization/complex_multiplication.py) | `factorization/complex_multiplication` | `factorize(N, D)` | ✅ |
| [Coppersmith Attack (+1)](attacks/factorization/coppersmith.py) | `factorization/coppersmith` | `factorize_p(N, partial_p, beta=0.5, epsilon=0.125, m=None, t=None)` | ✅ |
| [Fermat Attack](attacks/factorization/fermat.py) | `factorization/fermat` | `factorize(N)` | ✅ |
| [Ghafar-Ariffin-Asbullah Attack](attacks/factorization/gaa.py) | `factorization/gaa` | `factorize(N, rp, rq)` | ✅ |
| [Implicit Attack (+1)](attacks/factorization/implicit.py) | `factorization/implicit` | `factorize_msb(N, n, t)` | ✅ |
| [Known phi Attack (+1)](attacks/factorization/known_phi.py) | `factorization/known_phi` | `factorize(N, phi)` | ✅ |
| [ROCA Attack (+1)](attacks/factorization/roca.py) | `factorization/roca` | `compute_max_M_(M, ord_)` | ✅ |
| [Shor's Algorithm (Classical Simulation)](attacks/factorization/shor.py) | `factorization/shor` | `factorize(N, a, s)` | ✅ |
| [Twin Primes Attack](attacks/factorization/twin_primes.py) | `factorization/twin_primes` | `factorize(N)` | ✅ |
| [Unbalanced Attack](attacks/factorization/unbalanced.py) | `factorization/unbalanced` | `factorize(N, partial_p, Q, m=1, t=None, check_bounds=True)` | ✅ |

### GCM（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Forbidden Attack (+1)](attacks/gcm/forbidden_attack.py) | `gcm/forbidden_attack` | `recover_possible_auth_keys(a1, c1, t1, a2, c2, t2)` | ✅ |

### HNP · 隐藏数问题（2）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Extended HNP (+1)](attacks/hnp/extended_hnp.py) | `hnp/extended_hnp` | `attack(x_, N, pi, nu, a, p, u, b, delta=None)` | ✅ |
| [Lattice Attack (+3)](attacks/hnp/lattice_attack.py) | `hnp/lattice_attack` | `attack(a, b, m, X)` | ✅ |

### IGE 分组模式（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Padding Oracle Attack](attacks/ige/padding_oracle.py) | `ige/padding_oracle` | `attack(padding_oracle, p0, c0, c)` | ✅ |

### 背包密码（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Low Density Attack](attacks/knapsack/low_density.py) | `knapsack/low_density` | `attack(a, s)` | ✅ |

### LCG · 线性同余（3）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Parameter Recovery](attacks/lcg/parameter_recovery.py) | `lcg/parameter_recovery` | `attack(y, m=None, a=None, c=None)` | ✅ |
| [Truncated Parameter Recovery](attacks/lcg/truncated_parameter_recovery.py) | `lcg/truncated_parameter_recovery` | `attack(y, k, s, m=None, a=None, check_modulus=None)` | ✅ |
| [Truncated State Recovery](attacks/lcg/truncated_state_recovery.py) | `lcg/truncated_state_recovery` | `attack(y, k, s, m, a, c)` | ✅ |

### LWE（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Arora-Ge Attack](attacks/lwe/arora_ge.py) | `lwe/arora_ge` | `attack(q, A, b, E, S=None)` | ✅ |

### Mersenne Twister（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [State Recovery Attack (+2)](attacks/mersenne_twister/state_recovery.py) | `mersenne_twister/state_recovery` | `attack(y, w, n, m, r, a, b, c, s, t, u, d, l)` | ✅ |

### OTP · 一次性密码本（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Key Reuse Attack](attacks/otp/key_reuse.py) | `otp/key_reuse` | `attack(c, char_frequencies, char_floor, key_size=None)` | ✅ |

### 伪素数（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Miller-Rabin Pseudoprimes](attacks/pseudoprimes/miller_rabin.py) | `pseudoprimes/miller_rabin` | `generate_pseudoprime(A, k2=None, k3=None, min_bit_length=0)` | ✅ |

### RC4（1）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Fluhrer-Mantin-Shamir Attack](attacks/rc4/fms.py) | `rc4/fms` | `attack(encrypt_oracle, key_len)` | ✅ |

### RSA（21）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Bleichenbacher Attack](attacks/rsa/bleichenbacher.py) | `rsa/bleichenbacher` | `attack(padding_oracle, n, e, c)` | ✅ |
| [Bleichenbacher Signature Forgery Attack](attacks/rsa/bleichenbacher_signature_forgery.py) | `rsa/bleichenbacher_signature_forgery` | `attack(suffix, suffix_bit_length)` | ✅ |
| [Boneh-Durfee Attack (+1)](attacks/rsa/boneh_durfee.py) | `rsa/boneh_durfee` | `attack(N, e, factor_bit_length, partial_p=None, delta=0.25, m=1, t=…` | ✅ |
| [Cherkaoui Semmouni Attack](attacks/rsa/cherkaoui_semmouni.py) | `rsa/cherkaoui_semmouni` | `attack(N, e, beta, delta, m=1, t=None, check_bounds=True)` | ✅ |
| [Common Modulus Attack](attacks/rsa/common_modulus.py) | `rsa/common_modulus` | `attack(n, e1, c1, e2, c2)` | ✅ |
| [CRT Fault Attack](attacks/rsa/crt_fault_attack.py) | `rsa/crt_fault_attack` | `attack(n, e, sign)` | ✅ |
| [Extended Wiener Attack](attacks/rsa/extended_wiener_attack.py) | `rsa/extended_wiener_attack` | `attack(n, e, max_s=20000, max_r=100, max_t=100)` | ✅ |
| [Håstad Attack](attacks/rsa/hastad_attack.py) | `rsa/hastad_attack` | `attack(N, e, c)` | ✅ |
| [Known CRT Exponents Attack](attacks/rsa/known_crt_exponents.py) | `rsa/known_crt_exponents` | `attack(e_start, e_end, N=None, dp=None, dq=None, p_bit_length=None,…` | ✅ |
| [Known D Attack](attacks/rsa/known_d.py) | `rsa/known_d` | `attack(N, e, d)` | ✅ |
| [Low Public Exponent Attack](attacks/rsa/low_exponent.py) | `rsa/low_exponent` | `attack(e, c)` | ✅ |
| [LSB Oracle Attack](attacks/rsa/lsb_oracle.py) | `rsa/lsb_oracle` | `attack(N, e, c, oracle)` | ✅ |
| [Manger Attack](attacks/rsa/manger.py) | `rsa/manger` | `attack(padding_oracle, n, e, c)` | ✅ |
| [Nitaj CRT-RSA Attack](attacks/rsa/nitaj_crt_rsa.py) | `rsa/nitaj_crt_rsa` | `attack(N, e, delta, m, t, check_bounds=True)` | ✅ |
| [Non-Coprime Exponent Attack](attacks/rsa/non_coprime_exponent.py) | `rsa/non_coprime_exponent` | `attack(N, e, phi, c)` | ✅ |
| [Partial Key Exposure Attack](attacks/rsa/partial_key_exposure.py) | `rsa/partial_key_exposure` | `attack(N, e, partial_d, factor_e=True, m=1, t=None)` | ✅ |
| [Related Message Attack (+1)](attacks/rsa/related_message.py) | `rsa/related_message` | `attack(N, e, c1, c2, f1, f2)` | ✅ |
| [Stereotyped Message Attack](attacks/rsa/stereotyped_message.py) | `rsa/stereotyped_message` | `attack(N, e, c, partial_m, m=1, t=0)` | ✅ |
| [Wiener's Attack](attacks/rsa/wiener_attack.py) | `rsa/wiener_attack` | `attack(N, e)` | ✅ |
| [Wiener Attack (Common Prime RSA)](attacks/rsa/wiener_attack_common_prime.py) | `rsa/wiener_attack_common_prime` | `attack(N, e, delta=0.25, m=1, t=None, check_bounds=True)` | ✅ |
| [Wiener Attack (Lattice Variant) (+2)](attacks/rsa/wiener_attack_lattice.py) | `rsa/wiener_attack_lattice` | `attack(N, e)` | ✅ |

### Shamir 秘密共享（2）

| 攻击 | 入口键 | 参数签名 | 演示 |
| --- | --- | --- | :---: |
| [Deterministic Coefficients Attack](attacks/shamir_secret_sharing/deterministic_coefficients.py) | `shamir_secret_sharing/deterministic_coefficients` | `attack(p, k, a1, f, x, y)` | ✅ |
| [Share Forgery Attack](attacks/shamir_secret_sharing/share_forgery.py) | `shamir_secret_sharing/share_forgery` | `attack(p, s, s_, x, y, xs)` | ✅ |

