# 攻击参数手册

由 `python crypto_attack_machine.py docs` 自动生成，请勿手工编辑。

## ACD · 近似公因数

### Multivariate Polynomial Attack

- 入口键：`acd/mp`
- 源码：[`attacks/acd/mp.py`](../attacks/acd/mp.py)
- 依赖 SageMath：是
- 演示用例：`test.test_acd.TestACD.test_mp`

#### `attack(...)`

- 调用：`attacks.acd.mp.attack(...)` → `attack(N, a, rho, t=1, k=1, roots_method='groebner')`
- 说明：Solves the ACD problem using the multivariate polynomial approach.
- 参考：Galbraith D. S. et al., "Algorithms for the Approximate Common Divisor Problem" (Section 5)
- 返回：the secret integer p and a list containing the r values, or None if p could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | N = p * q0 |
| `a` | ✔ | the a samples, with ai = p * qi + ri |
| `rho` | ✔ | the bit length of the r values |
| `t` | `1` | the parameter t (default: 1) |
| `k` | `1` | the parameter k (default: 1) |
| `roots_method` | `'groebner'` | the method to use to find roots (default: "groebner") |

### Orthogonal Based Attack

- 入口键：`acd/ol`
- 源码：[`attacks/acd/ol.py`](../attacks/acd/ol.py)
- 依赖 SageMath：是
- 演示用例：`test.test_acd.TestACD.test_ol`

#### `attack(...)`

- 调用：`attacks.acd.ol.attack(...)` → `attack(x, rho)`
- 说明：Solves the ACD problem using the orthogonal based approach.
- 参考：Galbraith D. S. et al., "Algorithms for the Approximate Common Divisor Problem" (Section 4)
- 返回：the secret integer p and a list containing the r values, or None if p could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `x` | ✔ | the x samples, with xi = p * qi + ri |
| `rho` | ✔ | the bit length of the r values |

### Simultaneous Diophantine Approximation

- 入口键：`acd/sda`
- 源码：[`attacks/acd/sda.py`](../attacks/acd/sda.py)
- 依赖 SageMath：是
- 演示用例：`test.test_acd.TestACD.test_sda`

#### `attack(...)`

- 调用：`attacks.acd.sda.attack(...)` → `attack(x, rho)`
- 说明：Solves the ACD problem using the simultaneous Diophantine approximation approach.
- 参考：Galbraith D. S. et al., "Algorithms for the Approximate Common Divisor Problem" (Section 3)
- 返回：the secret integer p and a list containing the r values, or None if p could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `x` | ✔ | the x samples, with xi = p * qi + ri |
| `rho` | ✔ | the bit length of the r values |

## CBC 分组模式

### Bit Flipping Attack

- 入口键：`cbc/bit_flipping`
- 源码：[`attacks/cbc/bit_flipping.py`](../attacks/cbc/bit_flipping.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc.TestCBC.test_bit_flipping`

#### `attack(...)`

- 调用：`attacks.cbc.bit_flipping.attack(...)` → `attack(iv, c, pos, p, p_)`
- 说明：Replaces the original plaintext with a new plaintext at a position in the ciphertext.
- 返回：a tuple containing the modified initialization vector and the modified ciphertext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `iv` | ✔ | the initialization vector |
| `c` | ✔ | the ciphertext |
| `pos` | ✔ | the position to modify at |
| `p` | ✔ | the original plaintext |
| `p_` | ✔ | the new plaintext |

### IV Recovery

- 入口键：`cbc/iv_recovery`
- 源码：[`attacks/cbc/iv_recovery.py`](../attacks/cbc/iv_recovery.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc.TestCBC.test_iv_recovery`

#### `attack(...)`

- 调用：`attacks.cbc.iv_recovery.attack(...)` → `attack(decrypt_oracle)`
- 说明：Recovers the initialization vector using a chosen-ciphertext attack.
- 返回：the initialization vector

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `decrypt_oracle` | ✔ | the decryption oracle to decrypt ciphertexts |

### Padding Oracle Attack

- 入口键：`cbc/padding_oracle`
- 源码：[`attacks/cbc/padding_oracle.py`](../attacks/cbc/padding_oracle.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc.TestCBC.test_padding_oracle`

#### `attack(...)`

- 调用：`attacks.cbc.padding_oracle.attack(...)` → `attack(padding_oracle, iv, c)`
- 说明：Recovers the plaintext using the padding oracle attack.
- 返回：the (padded) plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `padding_oracle` | ✔ | the padding oracle, returns True if the padding is correct, False otherwise |
| `iv` | ✔ | the initialization vector |
| `c` | ✔ | the ciphertext |

## CBC + CBC-MAC

### Key Reuse (Encrypt-and-MAC)

- 入口键：`cbc_and_cbc_mac/eam_key_reuse`
- 源码：[`attacks/cbc_and_cbc_mac/eam_key_reuse.py`](../attacks/cbc_and_cbc_mac/eam_key_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc_and_cbc_mac.TestCBCAndCBCMAC.test_eam_key_reuse`

#### `attack(...)`

- 调用：`attacks.cbc_and_cbc_mac.eam_key_reuse.attack(...)` → `attack(decrypt_oracle, iv, c, t)`
- 说明：Uses a chosen-ciphertext attack to decrypt the ciphertext.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `decrypt_oracle` | ✔ | the decryption oracle |
| `iv` | ✔ | the initialization vector |
| `c` | ✔ | the ciphertext |
| `t` | ✔ | the tag corresponding to the ciphertext |

### Key Reuse (Encrypt-then-MAC)

- 入口键：`cbc_and_cbc_mac/etm_key_reuse`
- 源码：[`attacks/cbc_and_cbc_mac/etm_key_reuse.py`](../attacks/cbc_and_cbc_mac/etm_key_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc_and_cbc_mac.TestCBCAndCBCMAC.test_etm_key_reuse`

#### `attack(...)`

- 调用：`attacks.cbc_and_cbc_mac.etm_key_reuse.attack(...)` → `attack(encrypt_oracle, decrypt_oracle, iv, c, t)`
- 说明：Uses a chosen-ciphertext attack to decrypt the ciphertext.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `encrypt_oracle` | ✔ | the encryption oracle |
| `decrypt_oracle` | ✔ | the decryption oracle |
| `iv` | ✔ | the initialization vector |
| `c` | ✔ | the ciphertext |
| `t` | ✔ | the tag corresponding to the ciphertext |

### Key Reuse (MAC-then-Encrypt)

- 入口键：`cbc_and_cbc_mac/mte_key_reuse`
- 源码：[`attacks/cbc_and_cbc_mac/mte_key_reuse.py`](../attacks/cbc_and_cbc_mac/mte_key_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc_and_cbc_mac.TestCBCAndCBCMAC.test_mte_key_reuse`

#### `attack(...)`

- 调用：`attacks.cbc_and_cbc_mac.mte_key_reuse.attack(...)` → `attack(decrypt_oracle, iv, c, encrypted_zeroes)`
- 说明：Uses a chosen-ciphertext attack to decrypt the ciphertext.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `decrypt_oracle` | ✔ | the decryption oracle |
| `iv` | ✔ | the initialization vector |
| `c` | ✔ | the ciphertext |
| `encrypted_zeroes` | ✔ | a full zero block encrypted using the key |

## CBC-MAC

### Length Extension Attack

- 入口键：`cbc_mac/length_extension`
- 源码：[`attacks/cbc_mac/length_extension.py`](../attacks/cbc_mac/length_extension.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc_mac.TestCBCMAC.test_length_extension`

#### `attack(...)`

- 调用：`attacks.cbc_mac.length_extension.attack(...)` → `attack(m1, t1, m2, t2)`
- 说明：Uses a length extension attack to forge a message and tag pair for CBC-MAC.
- 返回：a tuple containing a valid message and tag for CBC-MAC

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `m1` | ✔ | the first message |
| `t1` | ✔ | the tag of the first message |
| `m2` | ✔ | the second message |
| `t2` | ✔ | the tag of the second message |

## CTR 分组模式

### Bit Flipping Attack

- 入口键：`ctr/bit_flipping`
- 源码：[`attacks/ctr/bit_flipping.py`](../attacks/ctr/bit_flipping.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc.TestCBC.test_bit_flipping`

#### `attack(...)`

- 调用：`attacks.ctr.bit_flipping.attack(...)` → `attack(c, pos, p, p_)`
- 说明：Replaces the original plaintext with a new plaintext at a position in the ciphertext.
- 返回：the modified ciphertext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `c` | ✔ | the ciphertext |
| `pos` | ✔ | the position to modify at |
| `p` | ✔ | the original plaintext |
| `p_` | ✔ | the new plaintext |

### CRIME Attack

- 入口键：`ctr/crime`
- 源码：[`attacks/ctr/crime.py`](../attacks/ctr/crime.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ctr.TestCTR.test_crime`

#### `attack(...)`

- 调用：`attacks.ctr.crime.attack(...)` → `attack(encrypt_oracle, known_prefix, padding_byte)`
- 说明：Recovers a secret using the CRIME attack (CTR version).
- 返回：the secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `encrypt_oracle` | ✔ | the encryption oracle |
| `known_prefix` | ✔ | a known prefix of the secret to recover |
| `padding_byte` | ✔ | a byte which is never used in the plaintext |

### Separator Oracle Attack

- 入口键：`ctr/separator_oracle`
- 源码：[`attacks/ctr/separator_oracle.py`](../attacks/ctr/separator_oracle.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ctr.TestCTR.test_separator_oracle`

#### `attack(...)`

- 调用：`attacks.ctr.separator_oracle.attack(...)` → `attack(separator_oracle, separator_byte, c)`
- 说明：Recovers the plaintext using the separator oracle attack.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `separator_oracle` | ✔ | the separator oracle, returns True if the separators are correct, False otherwise |
| `separator_byte` | ✔ | the separator which is used in the separator oracle |
| `c` | ✔ | the ciphertext |

## ECB 分组模式

### Plaintext Recovery

- 入口键：`ecb/plaintext_recovery`
- 源码：[`attacks/ecb/plaintext_recovery.py`](../attacks/ecb/plaintext_recovery.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ecb.TestECB.test_plaintext_recovery`

#### `attack(...)`

- 调用：`attacks.ecb.plaintext_recovery.attack(...)` → `attack(encrypt_oracle, unused_byte=0)`
- 说明：Recovers a secret which is appended to a plaintext and encrypted using ECB.
- 返回：the secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `encrypt_oracle` | ✔ | the encryption oracle |
| `unused_byte` | `0` | a byte that's never used in the secret |

### Plaintext Recovery (Harder)

- 入口键：`ecb/plaintext_recovery_harder`
- 源码：[`attacks/ecb/plaintext_recovery_harder.py`](../attacks/ecb/plaintext_recovery_harder.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ecb.TestECB.test_plaintext_recovery_harder`

#### `attack(...)`

- 调用：`attacks.ecb.plaintext_recovery_harder.attack(...)` → `attack(encrypt_oracle, unused_byte=0)`
- 说明：Recovers a secret which is appended to a plaintext and encrypted using ECB.
- 返回：the secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `encrypt_oracle` | ✔ | the encryption oracle |
| `unused_byte` | `0` | a byte that's never used in the secret or random prefix |

### Plaintext Recovery (Hardest)

- 入口键：`ecb/plaintext_recovery_hardest`
- 源码：[`attacks/ecb/plaintext_recovery_hardest.py`](../attacks/ecb/plaintext_recovery_hardest.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ecb.TestECB.test_plaintext_recovery_hardest`

#### `attack(...)`

- 调用：`attacks.ecb.plaintext_recovery_hardest.attack(...)` → `attack(encrypt_oracle, unused_byte=0)`
- 说明：Recovers a secret which is appended to a plaintext and encrypted using ECB.
- 返回：the secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `encrypt_oracle` | ✔ | the encryption oracle |
| `unused_byte` | `0` | a byte that's never used in the secret or random prefix |

## ECC · 椭圆曲线

### ECDSA Nonce Reuse

- 入口键：`ecc/ecdsa_nonce_reuse`
- 源码：[`attacks/ecc/ecdsa_nonce_reuse.py`](../attacks/ecc/ecdsa_nonce_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ecc.TestECC.test_ecdsa_nonce_reuse`

#### `attack(...)`

- 调用：`attacks.ecc.ecdsa_nonce_reuse.attack(...)` → `attack(n, m1, r1, s1, m2, r2, s2)`
- 说明：Recovers the nonce and private key from two messages signed using the same nonce.
- 返回：generates tuples containing the possible nonce and private key

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the order of the elliptic curve |
| `m1` | ✔ | the first message |
| `r1` | ✔ | the signature of the first message |
| `s1` | ✔ | the signature of the first message |
| `m2` | ✔ | the second message |
| `r2` | ✔ | the signature of the second message |
| `s2` | ✔ | the signature of the second message |

### Frey-Rück Attack

- 入口键：`ecc/frey_ruck_attack`
- 源码：[`attacks/ecc/frey_ruck_attack.py`](../attacks/ecc/frey_ruck_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_ecc.TestECC.test_frey_ruck_attack`

#### `attack(...)`

- 调用：`attacks.ecc.frey_ruck_attack.attack(...)` → `attack(P, R, max_k=6, max_tries=10)`
- 说明：Solves the discrete logarithm problem using the Frey-Ruck attack.
- 参考：Harasawa R. et al., "Comparing the MOV and FR Reductions in Elliptic Curve Cryptography" (Section 3)
- 返回：l such that l * P == R, or None if l was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `P` | ✔ | the base point |
| `R` | ✔ | the point multiplication result |
| `max_k` | `6` | the maximum value of embedding degree to try (default: 6) |
| `max_tries` | `10` | the maximum amount of times to try to find l (default: 10) |

### MOV Attack

- 入口键：`ecc/mov_attack`
- 源码：[`attacks/ecc/mov_attack.py`](../attacks/ecc/mov_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_ecc.TestECC.test_mov_attack`

#### `attack(...)`

- 调用：`attacks.ecc.mov_attack.attack(...)` → `attack(P, R, max_k=6, max_tries=10)`
- 说明：Solves the discrete logarithm problem using the MOV attack.
- 参考：Harasawa R. et al., "Comparing the MOV and FR Reductions in Elliptic Curve Cryptography" (Section 2)
- 返回：l such that l * P == R, or None if l was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `P` | ✔ | the base point |
| `R` | ✔ | the point multiplication result |
| `max_k` | `6` | the maximum value of embedding degree to try (default: 6) |
| `max_tries` | `10` | the maximum amount of times to try to find l (default: 10) |

### Parameter Recovery

- 入口键：`ecc/parameter_recovery`
- 源码：[`attacks/ecc/parameter_recovery.py`](../attacks/ecc/parameter_recovery.py)
- 依赖 SageMath：否
- 演示用例：`test.test_ecc.TestECC.test_parameter_recovery`

#### `attack(...)`

- 调用：`attacks.ecc.parameter_recovery.attack(...)` → `attack(p, x1, y1, x2, y2)`
- 说明：Recovers the a and b parameters from an elliptic curve when two points are known.
- 返回：a tuple containing the a and b parameters of the elliptic curve

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime of the curve base ring |
| `x1` | ✔ | the x coordinate of the first point |
| `y1` | ✔ | the y coordinate of the first point |
| `x2` | ✔ | the x coordinate of the second point |
| `y2` | ✔ | the y coordinate of the second point |

### Singular Curve Attack

- 入口键：`ecc/singular_curve`
- 源码：[`attacks/ecc/singular_curve.py`](../attacks/ecc/singular_curve.py)
- 依赖 SageMath：是
- 演示用例：`test.test_ecc.TestECC.test_singular_curve`

#### `attack(...)`

- 调用：`attacks.ecc.singular_curve.attack(...)` → `attack(p, a2, a4, a6, Gx, Gy, Px, Py)`
- 说明：Solves the discrete logarithm problem on a singular curve (y^2 = x^3 + a2 * x^2 + a4 * x + a6).
- 返回：l such that l * G == P

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime of the curve base ring |
| `a2` | ✔ | the a2 parameter of the curve |
| `a4` | ✔ | the a4 parameter of the curve |
| `a6` | ✔ | the a6 parameter of the curve |
| `Gx` | ✔ | the base point x value |
| `Gy` | ✔ | the base point y value |
| `Px` | ✔ | the point multiplication result x value |
| `Py` | ✔ | the point multiplication result y value |

### Smart's Attack

- 入口键：`ecc/smart_attack`
- 源码：[`attacks/ecc/smart_attack.py`](../attacks/ecc/smart_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_ecc.TestECC.test_smart_attack`

#### `attack(...)`

- 调用：`attacks.ecc.smart_attack.attack(...)` → `attack(G, P)`
- 说明：Solves the discrete logarithm problem using Smart's attack.
- 参考：Smart N. P., "The discrete logarithm problem on elliptic curves of trace one"
- 返回：l such that l * G == P

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `G` | ✔ | the base point |
| `P` | ✔ | the point multiplication result |

## ElGamal 加密

### Nonce Reuse Attack

- 入口键：`elgamal_encryption/nonce_reuse`
- 源码：[`attacks/elgamal_encryption/nonce_reuse.py`](../attacks/elgamal_encryption/nonce_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_elgamal_encryption.TestElgamalEncryption.test_nonce_reuse`

#### `attack(...)`

- 调用：`attacks.elgamal_encryption.nonce_reuse.attack(...)` → `attack(p, m1, c1, d1, c2, d2)`
- 说明：Recovers a secret plaintext encrypted using the same nonce as a previous, known plaintext.
- 返回：the secret plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime used in the ElGamal scheme |
| `m1` | ✔ | the known plaintext |
| `c1` | ✔ | the ciphertext of the known plaintext |
| `d1` | ✔ | the ciphertext of the known plaintext |
| `c2` | ✔ | the ciphertext of the secret plaintext |
| `d2` | ✔ | the ciphertext of the secret plaintext |

### Unsafe Generator Attack

- 入口键：`elgamal_encryption/unsafe_generator`
- 源码：[`attacks/elgamal_encryption/unsafe_generator.py`](../attacks/elgamal_encryption/unsafe_generator.py)
- 依赖 SageMath：是
- 演示用例：`test.test_elgamal_encryption.TestElgamalEncryption.test_unsafe_generator`

#### `attack(...)`

- 调用：`attacks.elgamal_encryption.unsafe_generator.attack(...)` → `attack(p, h, c1, c2)`
- 说明：Returns the Legendre symbol of the message encrypted using an unsafe generator.
- 返回：the Legendre symbol

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime used in the ElGamal scheme |
| `h` | ✔ | the public key |
| `c1` | ✔ | the ciphertext |
| `c2` | ✔ | the ciphertext |

## ElGamal 签名

### Nonce Reuse Attack

- 入口键：`elgamal_signature/nonce_reuse`
- 源码：[`attacks/elgamal_signature/nonce_reuse.py`](../attacks/elgamal_signature/nonce_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_elgamal_encryption.TestElgamalEncryption.test_nonce_reuse`

#### `attack(...)`

- 调用：`attacks.elgamal_signature.nonce_reuse.attack(...)` → `attack(p, m1, r1, s1, m2, r2, s2)`
- 说明：Recovers the nonce and private key from two messages signed using the same nonce.
- 返回：generates tuples containing the possible nonce and private key

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime used in the ElGamal scheme |
| `m1` | ✔ | the first message |
| `r1` | ✔ | the signature of the first message |
| `s1` | ✔ | the signature of the first message |
| `m2` | ✔ | the second message |
| `r2` | ✔ | the signature of the second message |
| `s2` | ✔ | the signature of the second message |

## 整数分解

### Base Conversion Attack

- 入口键：`factorization/base_conversion`
- 源码：[`attacks/factorization/base_conversion.py`](../attacks/factorization/base_conversion.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_base_conversion`

#### `factorize(...)`

- 调用：`attacks.factorization.base_conversion.factorize(...)` → `factorize(N, coefficient_threshold=32)`
- 说明：Recovers the prime factors from a modulus by converting it to different bases.
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `coefficient_threshold` | `32` | the threshold of coefficients below which we will try to factor a base k polynomial |

#### `factorize_base_2x(...)`

- 调用：`attacks.factorization.base_conversion.factorize_base_2x(...)` → `factorize_base_2x(N)`
- 说明：Recovers the prime factors from a modulus by converting it to different bases of the form 2^x.
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |

### Branch And Prune Attack

- 入口键：`factorization/branch_and_prune`
- 源码：[`attacks/factorization/branch_and_prune.py`](../attacks/factorization/branch_and_prune.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_branch_and_prune`

#### `factorize_pq(...)`

- 调用：`attacks.factorization.branch_and_prune.factorize_pq(...)` → `factorize_pq(N, p, q)`
- 说明：Factorizes n when some bits of p and q are known.
- 参考：Heninger N., Shacham H., "Reconstructing RSA Private Keys from Random Key Bits"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `p` | ✔ | partial p (PartialInteger) |
| `q` | ✔ | partial q (PartialInteger) |

#### `factorize_pqd(...)`

- 调用：`attacks.factorization.branch_and_prune.factorize_pqd(...)` → `factorize_pqd(N, e, p, q, d)`
- 说明：Factorizes n when some bits of p, q, and d are known.
- 参考：Heninger N., Shacham H., "Reconstructing RSA Private Keys from Random Key Bits"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `p` | ✔ | partial p (PartialInteger) |
| `q` | ✔ | partial q (PartialInteger) |
| `d` | ✔ | partial d (PartialInteger) |

#### `factorize_pqddpdq(...)`

- 调用：`attacks.factorization.branch_and_prune.factorize_pqddpdq(...)` → `factorize_pqddpdq(N, e, p, q, d, dp, dq)`
- 说明：Factorizes n when some bits of p, q, d, dp, and dq are known.
- 参考：Heninger N., Shacham H., "Reconstructing RSA Private Keys from Random Key Bits"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `p` | ✔ | partial p (PartialInteger) |
| `q` | ✔ | partial q (PartialInteger) |
| `d` | ✔ | partial d (PartialInteger) |
| `dp` | ✔ | partial dp (PartialInteger) |
| `dq` | ✔ | partial dq (PartialInteger) |

### Complex Multiplication Attack

- 入口键：`factorization/complex_multiplication`
- 源码：[`attacks/factorization/complex_multiplication.py`](../attacks/factorization/complex_multiplication.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_complex_multiplication`

#### `factorize(...)`

- 调用：`attacks.factorization.complex_multiplication.factorize(...)` → `factorize(N, D)`
- 说明：Recovers the prime factors from a modulus using Cheng's elliptic curve complex multiplication method.
- 参考：Sedlacek V. et al., "I want to break square-free: The 4p - 1 factorization method and its RSA backdoor viability"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `D` | ✔ | the discriminant to use to generate the Hilbert polynomial |

### Coppersmith Attack

- 入口键：`factorization/coppersmith`
- 源码：[`attacks/factorization/coppersmith.py`](../attacks/factorization/coppersmith.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_coppersmith`

#### `factorize_p(...)`

- 调用：`attacks.factorization.coppersmith.factorize_p(...)` → `factorize_p(N, partial_p, beta=0.5, epsilon=0.125, m=None, t=None)`
- 说明：Recover the prime factors from a modulus using Coppersmith's method and bits of one prime factor p are known.
- 参考：Herrmann M., May A., "Solving Linear Equations Modulo Divisors: On Factoring Given Any Bits" (Section 3 and 4)
- 返回：a tuple containing the prime factors, or None if the factors could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `partial_p` | ✔ | the partial prime factor p (PartialInteger) |
| `beta` | `0.5` | the parameter beta (default: 0.5) |
| `epsilon` | `0.125` | the parameter epsilon (default: 0.125) |
| `m` | `None` | the number of normal shifts to use (default: automatically computed using beta and epsilon) |
| `t` | `None` | the number of additional shifts to use (default: automatically computed using beta and epsilon) |

#### `factorize_pq(...)`

- 调用：`attacks.factorization.coppersmith.factorize_pq(...)` → `factorize_pq(N, partial_p, partial_q, k=None)`
- 说明：Recover the prime factors from a modulus using Coppersmith's method and bits of both prime factors p and q are known.
- 返回：a tuple containing the prime factors, or None if the factors could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `partial_p` | ✔ | the partial prime factor p (PartialInteger) |
| `partial_q` | ✔ | the partial prime factor q (PartialInteger) |
| `k` | `None` | the number of shifts to use for Coron's method, must be set if the total number of unknown components is two (default: None) |

### Fermat Attack

- 入口键：`factorization/fermat`
- 源码：[`attacks/factorization/fermat.py`](../attacks/factorization/fermat.py)
- 依赖 SageMath：否
- 演示用例：`test.test_factorization.TestFactorization.test_fermat`

#### `factorize(...)`

- 调用：`attacks.factorization.fermat.factorize(...)` → `factorize(N)`
- 说明：Recovers the prime factors from a modulus using Fermat's factorization method.
- 返回：a tuple containing the prime factors, or None if the factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |

### Ghafar-Ariffin-Asbullah Attack

- 入口键：`factorization/gaa`
- 源码：[`attacks/factorization/gaa.py`](../attacks/factorization/gaa.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_gaa`

#### `factorize(...)`

- 调用：`attacks.factorization.gaa.factorize(...)` → `factorize(N, rp, rq)`
- 说明：Recovers the prime factors from a modulus using the Ghafar-Ariffin-Asbullah attack.
- 参考：Ghafar AHA. et al., "A New LSB Attack on Special-Structured RSA Primes"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `rp` | ✔ | the value rp |
| `rq` | ✔ | the value rq |

### Implicit Attack

- 入口键：`factorization/implicit`
- 源码：[`attacks/factorization/implicit.py`](../attacks/factorization/implicit.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_implicit`

#### `factorize_msb(...)`

- 调用：`attacks.factorization.implicit.factorize_msb(...)` → `factorize_msb(N, n, t)`
- 说明：Factorizes the moduli when some most significant bits are equal among multiples of a prime factor.
- 参考：Nitaj A., Ariffin MRK., "Implicit factorization of unbalanced RSA moduli" (Section 4)
- 返回：a list containing a tuple of the factors of each modulus, or None if the factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the moduli |
| `n` | ✔ | the bit length of the moduli |
| `t` | ✔ | the number of shared most significant bits |

#### `factorize_lsb(...)`

- 调用：`attacks.factorization.implicit.factorize_lsb(...)` → `factorize_lsb(N, n, t)`
- 说明：Factorizes the moduli when some least significant bits are equal among multiples of a prime factor.
- 参考：Nitaj A., Ariffin MRK., "Implicit factorization of unbalanced RSA moduli" (Section 6)
- 返回：a list containing a tuple of the factors of each modulus, or None if the factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the moduli |
| `n` | ✔ | the bit length of the moduli |
| `t` | ✔ | the number of shared least significant bits |

### Known phi Attack

- 入口键：`factorization/known_phi`
- 源码：[`attacks/factorization/known_phi.py`](../attacks/factorization/known_phi.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_known_phi`

#### `factorize(...)`

- 调用：`attacks.factorization.known_phi.factorize(...)` → `factorize(N, phi)`
- 说明：Recovers the prime factors from a modulus if Euler's totient is known.
- 返回：a tuple containing the prime factors, or None if the factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `phi` | ✔ | Euler's totient, the order of the multiplicative group modulo N |

#### `factorize_multi_prime(...)`

- 调用：`attacks.factorization.known_phi.factorize_multi_prime(...)` → `factorize_multi_prime(N, phi)`
- 说明：Recovers the prime factors from a modulus if Euler's totient is known.
- 参考：Hinek M. J., Low M. K., Teske E., "On Some Attacks on Multi-prime RSA" (Section 3)
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `phi` | ✔ | Euler's totient, the order of the multiplicative group modulo N |

### ROCA Attack

- 入口键：`factorization/roca`
- 源码：[`attacks/factorization/roca.py`](../attacks/factorization/roca.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_roca`

#### `compute_max_M_(...)`

- 调用：`attacks.factorization.roca.compute_max_M_(...)` → `compute_max_M_(M, ord_)`

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `M` | ✔ |  |
| `ord_` | ✔ |  |

#### `factorize(...)`

- 调用：`attacks.factorization.roca.factorize(...)` → `factorize(N, M, m, t, g=65537)`
- 说明：Recovers the prime factors from a modulus using the ROCA method.
- 参考：Nemec M. et al., "The Return of Coppersmith’s Attack: Practical Factorization of Widely Used RSA Moduli"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `M` | ✔ | the primorial used to generate the primes |
| `m` | ✔ | the m parameter for Coppersmith's method |
| `t` | ✔ | the t parameter for Coppersmith's method |
| `g` | `65537` | the generator value (default: 65537) |

### Shor's Algorithm (Classical Simulation)

- 入口键：`factorization/shor`
- 源码：[`attacks/factorization/shor.py`](../attacks/factorization/shor.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_shor`

#### `factorize(...)`

- 调用：`attacks.factorization.shor.factorize(...)` → `factorize(N, a, s)`
- 说明：Recovers the prime factors from a modulus if the order of a mod n is known.
- 参考：M. Johnston A., "Shor's Algorithm and Factoring: Don't Throw Away the Odd Orders"
- 返回：a tuple containing the prime factors, or None if the factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `a` | ✔ | the base |
| `s` | ✔ | the order of a |

### Twin Primes Attack

- 入口键：`factorization/twin_primes`
- 源码：[`attacks/factorization/twin_primes.py`](../attacks/factorization/twin_primes.py)
- 依赖 SageMath：否
- 演示用例：`test.test_factorization.TestFactorization.test_twin_primes`

#### `factorize(...)`

- 调用：`attacks.factorization.twin_primes.factorize(...)` → `factorize(N)`
- 说明：Recovers the prime factors from a modulus if the factors are twin primes.
- 返回：a tuple containing the prime factors, or None if there is no factorization

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |

### Unbalanced Attack

- 入口键：`factorization/unbalanced`
- 源码：[`attacks/factorization/unbalanced.py`](../attacks/factorization/unbalanced.py)
- 依赖 SageMath：是
- 演示用例：`test.test_factorization.TestFactorization.test_unbalanced`

#### `factorize(...)`

- 调用：`attacks.factorization.unbalanced.factorize(...)` → `factorize(N, partial_p, Q, m=1, t=None, check_bounds=True)`
- 说明：Recovers the prime factors from a modulus if the modulus is unbalanced and bits are known.
- 参考：Brier E. et al., "Factoring Unbalanced Moduli with Known Bits" (Section 4)
- 返回：a tuple containing the prime factors, or None if the factors could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus: N = p * q > q ** 3 |
| `partial_p` | ✔ | the partial prime factor p (PartialInteger) |
| `Q` | ✔ | the bit length of q |
| `m` | `1` | the m value to use for the small roots method (default: 1) |
| `t` | `None` | the t value to use for the small roots method (default: automatically computed using m) |
| `check_bounds` | `True` | perform bounds check (default: True) |

## GCM

### Forbidden Attack

- 入口键：`gcm/forbidden_attack`
- 源码：[`attacks/gcm/forbidden_attack.py`](../attacks/gcm/forbidden_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_gcm.TestGCM.test_forbidden_attack`

#### `recover_possible_auth_keys(...)`

- 调用：`attacks.gcm.forbidden_attack.recover_possible_auth_keys(...)` → `recover_possible_auth_keys(a1, c1, t1, a2, c2, t2)`
- 说明：Recovers possible authentication keys from two messages encrypted with the same authentication key.
- 参考：Joux A., "Authentication Failures in NIST version of GCM"
- 返回：a generator generating possible authentication keys (gf2e element)

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `a1` | ✔ | the associated data of the first message (bytes) |
| `c1` | ✔ | the ciphertext of the first message (bytes) |
| `t1` | ✔ | the authentication tag of the first message (bytes) |
| `a2` | ✔ | the associated data of the second message (bytes) |
| `c2` | ✔ | the ciphertext of the second message (bytes) |
| `t2` | ✔ | the authentication tag of the second message (bytes) |

#### `forge_tag(...)`

- 调用：`attacks.gcm.forbidden_attack.forge_tag(...)` → `forge_tag(h, a, c, t, target_a, target_c)`
- 说明：Forges an authentication tag for a target message given a message with a known tag.
- 参考：Joux A., "Authentication Failures in NIST version of GCM"
- 返回：the forged authentication tag (bytes)

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `h` | ✔ | the authentication key to use (gf2e element) |
| `a` | ✔ | the associated data of the message with the known tag (bytes) |
| `c` | ✔ | the ciphertext of the message with the known tag (bytes) |
| `t` | ✔ | the known authentication tag (bytes) |
| `target_a` | ✔ | the target associated data (bytes) |
| `target_c` | ✔ | the target ciphertext (bytes) |

## HNP · 隐藏数问题

### Extended HNP

- 入口键：`hnp/extended_hnp`
- 源码：[`attacks/hnp/extended_hnp.py`](../attacks/hnp/extended_hnp.py)
- 依赖 SageMath：是
- 演示用例：`test.test_hnp.TestHNP.test_extended_hnp`

#### `attack(...)`

- 调用：`attacks.hnp.extended_hnp.attack(...)` → `attack(x_, N, pi, nu, a, p, u, b, delta=None)`
- 说明：Solves the extended hidden number problem (definition 6 in the source paper).
- 参考：Hlavac M., Rosa T., "Extended Hidden Number Problem and Its Cryptanalytic Applications" (Section 4)
- 返回：a generator generating possible values of x

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `x_` | ✔ | the known bits of x |
| `N` | ✔ | the modulus |
| `pi` | ✔ | the pi values |
| `nu` | ✔ | the nu values |
| `a` | ✔ | the alpha values |
| `p` | ✔ | the rho values |
| `u` | ✔ | the mu values |
| `b` | ✔ | the beta values |
| `delta` | `None` | the delta value (default: automatically computed) |

#### `dsa_known_bits(...)`

- 调用：`attacks.hnp.extended_hnp.dsa_known_bits(...)` → `dsa_known_bits(N, h, r, s, x, k)`
- 说明：Recovers the (EC)DSA private key if any nonce bits are known.
- 返回：a generator generating possible private keys

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `h` | ✔ | a list containing the hashed messages |
| `r` | ✔ | a list containing the r values |
| `s` | ✔ | a list containing the s values |
| `x` | ✔ | the partial private key (PartialInteger, can be fully unknown) |
| `k` | ✔ | a list containing the partial nonces (PartialIntegers) |

### Lattice Attack

- 入口键：`hnp/lattice_attack`
- 源码：[`attacks/hnp/lattice_attack.py`](../attacks/hnp/lattice_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_hnp.TestHNP.test_lattice_attack`

#### `attack(...)`

- 调用：`attacks.hnp.lattice_attack.attack(...)` → `attack(a, b, m, X)`
- 说明：Solves the hidden number problem using an attack based on the shortest vector problem.
- 返回：a generator generating tuples containing a list of xi values and a list of yj values

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `a` | ✔ | the aij values |
| `b` | ✔ | the bi values |
| `m` | ✔ | the modulus |
| `X` | ✔ | a bound on the xi values |

#### `dsa_known_msb(...)`

- 调用：`attacks.hnp.lattice_attack.dsa_known_msb(...)` → `dsa_known_msb(n, h, r, s, k)`
- 说明：Recovers the (EC)DSA private key and nonces if the most significant nonce bits are known.
- 返回：a generator generating tuples containing the possible private key and a list of nonces

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the modulus |
| `h` | ✔ | a list containing the hashed messages |
| `r` | ✔ | a list containing the r values |
| `s` | ✔ | a list containing the s values |
| `k` | ✔ | a list containing the partial nonces (PartialIntegers) |

#### `dsa_known_lsb(...)`

- 调用：`attacks.hnp.lattice_attack.dsa_known_lsb(...)` → `dsa_known_lsb(n, h, r, s, k)`
- 说明：Recovers the (EC)DSA private key and nonces if the least significant nonce bits are known.
- 返回：a generator generating tuples containing the possible private key and a list of nonces

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the modulus |
| `h` | ✔ | a list containing the hashed messages |
| `r` | ✔ | a list containing the r values |
| `s` | ✔ | a list containing the s values |
| `k` | ✔ | a list containing the partial nonces (PartialIntegers) |

#### `dsa_known_middle(...)`

- 调用：`attacks.hnp.lattice_attack.dsa_known_middle(...)` → `dsa_known_middle(n, h1, r1, s1, k1, h2, r2, s2, k2)`
- 说明：Recovers the (EC)DSA private key and nonces if the middle nonce bits are known.
- 参考：De Micheli G., Heninger N., "Recovering cryptographic keys from partial information, by example" (Section 5.2.3)
- 返回：a tuple containing the private key, the nonce of the first signature, and the nonce of the second signature

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the modulus |
| `h1` | ✔ | the first hashed message |
| `r1` | ✔ | the first r value |
| `s1` | ✔ | the first s value |
| `k1` | ✔ | the first partial nonce (PartialInteger) |
| `h2` | ✔ | the second hashed message |
| `r2` | ✔ | the second r value |
| `s2` | ✔ | the second s value |
| `k2` | ✔ | the second partial nonce (PartialInteger) |

## IGE 分组模式

### Padding Oracle Attack

- 入口键：`ige/padding_oracle`
- 源码：[`attacks/ige/padding_oracle.py`](../attacks/ige/padding_oracle.py)
- 依赖 SageMath：否
- 演示用例：`test.test_cbc.TestCBC.test_padding_oracle`

#### `attack(...)`

- 调用：`attacks.ige.padding_oracle.attack(...)` → `attack(padding_oracle, p0, c0, c)`
- 说明：Recovers the plaintext using the padding oracle attack.
- 返回：the (padded) plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `padding_oracle` | ✔ | the padding oracle, returns True if the padding is correct, False otherwise |
| `p0` | ✔ | the initial plaintext block |
| `c0` | ✔ | the initial ciphertext block |
| `c` | ✔ | the ciphertext |

## 背包密码

### Low Density Attack

- 入口键：`knapsack/low_density`
- 源码：[`attacks/knapsack/low_density.py`](../attacks/knapsack/low_density.py)
- 依赖 SageMath：是
- 演示用例：`test.test_knapsack.TestKnapsack.test_low_density`

#### `attack(...)`

- 调用：`attacks.knapsack.low_density.attack(...)` → `attack(a, s)`
- 说明：Tries to find e_i values such that sum(e_i * a_i) = s.
- 参考：Coster M. J. et al., "Improved low-density subset sum algorithms"
- 返回：the e_i values, or None if the e_i values were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `a` | ✔ | the a_i values |
| `s` | ✔ | the s value |

## LCG · 线性同余

### Parameter Recovery

- 入口键：`lcg/parameter_recovery`
- 源码：[`attacks/lcg/parameter_recovery.py`](../attacks/lcg/parameter_recovery.py)
- 依赖 SageMath：是
- 演示用例：`test.test_ecc.TestECC.test_parameter_recovery`

#### `attack(...)`

- 调用：`attacks.lcg.parameter_recovery.attack(...)` → `attack(y, m=None, a=None, c=None)`
- 说明：Recovers the parameters from a linear congruential generator.
- 返回：a tuple containing the modulus, multiplier, and the increment

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `y` | ✔ | the sequential output values obtained from the LCG |
| `m` | `None` | the modulus of the LCG (can be None) |
| `a` | `None` | the multiplier of the LCG (can be None) |
| `c` | `None` | the increment of the LCG (can be None) |

### Truncated Parameter Recovery

- 入口键：`lcg/truncated_parameter_recovery`
- 源码：[`attacks/lcg/truncated_parameter_recovery.py`](../attacks/lcg/truncated_parameter_recovery.py)
- 依赖 SageMath：是
- 演示用例：`test.test_lcg.TestLCG.test_truncated_parameter_recovery`

#### `attack(...)`

- 调用：`attacks.lcg.truncated_parameter_recovery.attack(...)` → `attack(y, k, s, m=None, a=None, check_modulus=None)`
- 说明：Recovers possible parameters and states from a truncated linear congruential generator.
- 参考：Contini S., Shparlinski I. E., "On Stern's Attack Against Secret Truncated Linear Congruential Generators" If no modulus is provided, attempts to recover a modulus from the outputs. If no multiplier is provided, attempts to recover a multiplier from the outputs. Also recovers an increment from the outputs. The resulting parameters may not match the original parameters, but the generated sequence should be the same up to some small error.
- 返回：a generator generating possible parameters (tuples of modulus, multiplier, increment, and seed) of the truncated LCG

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `y` | ✔ | the sequential output values obtained from the truncated LCG (the states truncated to s most significant bits) |
| `k` | ✔ | the bit length of the states |
| `s` | ✔ | the bit length of the outputs |
| `m` | `None` | the modulus of the LCG (can be None) |
| `a` | `None` | the multiplier of the LCG (can be None) |
| `check_modulus` | `None` | a function which checks if a possible value can be the modulus (default: compare the bit length with k) |

### Truncated State Recovery

- 入口键：`lcg/truncated_state_recovery`
- 源码：[`attacks/lcg/truncated_state_recovery.py`](../attacks/lcg/truncated_state_recovery.py)
- 依赖 SageMath：是
- 演示用例：`test.test_lcg.TestLCG.test_truncated_state_recovery`

#### `attack(...)`

- 调用：`attacks.lcg.truncated_state_recovery.attack(...)` → `attack(y, k, s, m, a, c)`
- 说明：Recovers the states associated with the outputs from a truncated linear congruential generator.
- 参考：Frieze, A. et al., "Reconstructing Truncated Integer Variables Satisfying Linear Congruences"
- 返回：a list containing the states associated with the provided outputs

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `y` | ✔ | the sequential output values obtained from the truncated LCG (the states truncated to s most significant bits) |
| `k` | ✔ | the bit length of the states |
| `s` | ✔ | the bit length of the outputs |
| `m` | ✔ | the modulus of the LCG |
| `a` | ✔ | the multiplier of the LCG |
| `c` | ✔ | the increment of the LCG |

## LWE

### Arora-Ge Attack

- 入口键：`lwe/arora_ge`
- 源码：[`attacks/lwe/arora_ge.py`](../attacks/lwe/arora_ge.py)
- 依赖 SageMath：是
- 演示用例：`test.test_lwe.TestLWE.test_arora_ge`

#### `attack(...)`

- 调用：`attacks.lwe.arora_ge.attack(...)` → `attack(q, A, b, E, S=None)`
- 说明：Recovers the secret key s from the LWE samples A and b.
- 参考："The Learning with Errors Problem: Algorithms" (Section 1)
- 返回：a list representing the secret key s

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `q` | ✔ | the modulus |
| `A` | ✔ | the matrix A, represented as a list of lists |
| `b` | ✔ | the vector b, represented as a list |
| `E` | ✔ | the possible error values |
| `S` | `None` | the possible values of the entries in s (default: None) |

## Mersenne Twister

### State Recovery Attack

- 入口键：`mersenne_twister/state_recovery`
- 源码：[`attacks/mersenne_twister/state_recovery.py`](../attacks/mersenne_twister/state_recovery.py)
- 依赖 SageMath：否
- 演示用例：`test.test_mersenne_twister.TestMersenneTwister.test_state_recovery`

#### `attack(...)`

- 调用：`attacks.mersenne_twister.state_recovery.attack(...)` → `attack(y, w, n, m, r, a, b, c, s, t, u, d, l)`
- 说明：Recovers the state from a Mersenne Twister instance using n outputs.
- 返回：a cloned Mersenne Twister instance

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `y` | ✔ | the outputs (must be of length n) |
| `w` | ✔ | the parameter w |
| `n` | ✔ | the parameter n |
| `m` | ✔ | the parameter m |
| `r` | ✔ | the parameter r |
| `a` | ✔ | the parameter a |
| `b` | ✔ | the parameter b |
| `c` | ✔ | the parameter c |
| `s` | ✔ | the parameter s |
| `t` | ✔ | the parameter t |
| `u` | ✔ | the parameter u |
| `d` | ✔ | the parameter d |
| `l` | ✔ | the parameter l |

#### `attack_mt19937(...)`

- 调用：`attacks.mersenne_twister.state_recovery.attack_mt19937(...)` → `attack_mt19937(y)`
- 说明：Recovers the state from an MT19937 instance using 624 outputs.
- 返回：a cloned MT19937 instance

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `y` | ✔ | the outputs |

#### `attack_mt19937_64(...)`

- 调用：`attacks.mersenne_twister.state_recovery.attack_mt19937_64(...)` → `attack_mt19937_64(y)`
- 说明：Recovers the state from an MT19937-64 instance using 312 outputs.
- 返回：a cloned MT19937-64 instance

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `y` | ✔ | the outputs |

## OTP · 一次性密码本

### Key Reuse Attack

- 入口键：`otp/key_reuse`
- 源码：[`attacks/otp/key_reuse.py`](../attacks/otp/key_reuse.py)
- 依赖 SageMath：否
- 演示用例：`test.test_otp.TestOTP.test_key_reuse`

#### `attack(...)`

- 调用：`attacks.otp.key_reuse.attack(...)` → `attack(c, char_frequencies, char_floor, key_size=None)`
- 说明：Breaks the one-time pad when the key is reused in a single plaintext or multiple plaintexts.
- 返回：the best guess for the key

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `c` | ✔ | the list of ciphertexts |
| `char_frequencies` | ✔ | a dict of (char, frequency) items for the plaintext language |
| `char_floor` | ✔ | the value to assign to a character if it is not found in char_frequencies |
| `key_size` | `None` | the size of the key in bytes (default: None): if no key size is given, this method attempts to discover it using the Hamming distance |

## 伪素数

### Miller-Rabin Pseudoprimes

- 入口键：`pseudoprimes/miller_rabin`
- 源码：[`attacks/pseudoprimes/miller_rabin.py`](../attacks/pseudoprimes/miller_rabin.py)
- 依赖 SageMath：是
- 演示用例：`test.test_pseudoprimes.TestPseudoprimes.test_miller_rabin`

#### `generate_pseudoprime(...)`

- 调用：`attacks.pseudoprimes.miller_rabin.generate_pseudoprime(...)` → `generate_pseudoprime(A, k2=None, k3=None, min_bit_length=0)`
- 说明：Generates a pseudoprime of the form p1 * p2 * p3 which passes the Miller-Rabin primality test for the provided bases.
- 参考：R. Albrecht M. et al., "Prime and Prejudice: Primality Testing Under Adversarial Conditions"
- 返回：a tuple containing the pseudoprime n, as well as its 3 prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `A` | ✔ | the bases |
| `k2` | `None` | the k2 value (default: next_prime(A[-1])) |
| `k3` | `None` | the k3 value (default: next_prime(k2)) |
| `min_bit_length` | `0` | the minimum bit length of the generated pseudoprime (default: 0) |

## RC4

### Fluhrer-Mantin-Shamir Attack

- 入口键：`rc4/fms`
- 源码：[`attacks/rc4/fms.py`](../attacks/rc4/fms.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rc4.TestRC4.test_fms`

#### `attack(...)`

- 调用：`attacks.rc4.fms.attack(...)` → `attack(encrypt_oracle, key_len)`
- 说明：Recovers the hidden part of an RC4 key using the Fluhrer-Mantin-Shamir attack.
- 返回：the hidden part of the key

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `encrypt_oracle` | ✔ | the padding oracle, returns the encryption of a plaintext under a hidden key concatenated with the iv |
| `key_len` | ✔ | the length of the hidden part of the key |

## RSA

### Bleichenbacher Attack

- 入口键：`rsa/bleichenbacher`
- 源码：[`attacks/rsa/bleichenbacher.py`](../attacks/rsa/bleichenbacher.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rsa.TestRSA.test_bleichenbacher`

#### `attack(...)`

- 调用：`attacks.rsa.bleichenbacher.attack(...)` → `attack(padding_oracle, n, e, c)`
- 说明：Recovers the plaintext using Bleichenbacher's attack.
- 参考：Bleichenbacher D., "Chosen Ciphertext Attacks Against Protocols Based on the RSA Encryption Standard PKCS #1"
- 返回：the plaintext (integer)

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `padding_oracle` | ✔ | the padding oracle taking integers, returns True if the PKCS #1 v1.5 padding is correct, False otherwise |
| `n` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `c` | ✔ | the ciphertext (integer) |

### Bleichenbacher Signature Forgery Attack

- 入口键：`rsa/bleichenbacher_signature_forgery`
- 源码：[`attacks/rsa/bleichenbacher_signature_forgery.py`](../attacks/rsa/bleichenbacher_signature_forgery.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rsa.TestRSA.test_bleichenbacher_signature_forgery`

#### `attack(...)`

- 调用：`attacks.rsa.bleichenbacher_signature_forgery.attack(...)` → `attack(suffix, suffix_bit_length)`
- 说明：Returns a number s for which s^3 ends with the provided suffix.
- 返回：the number s

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `suffix` | ✔ | the suffix |
| `suffix_bit_length` | ✔ | the bit length of the suffix |

### Boneh-Durfee Attack

- 入口键：`rsa/boneh_durfee`
- 源码：[`attacks/rsa/boneh_durfee.py`](../attacks/rsa/boneh_durfee.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_boneh_durfee`

#### `attack(...)`

- 调用：`attacks.rsa.boneh_durfee.attack(...)` → `attack(N, e, factor_bit_length, partial_p=None, delta=0.25, m=1, t=None)`
- 说明：Recovers the prime factors if the private exponent is too small.
- 参考：Boneh D., Durfee G., "Cryptanalysis of RSA with Private Key d Less than N^0.292"
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `factor_bit_length` | ✔ | the bit length of the prime factors |
| `partial_p` | `None` | the partial prime factor p (PartialInteger) (default: None) |
| `delta` | `0.25` | a predicted bound on the private exponent (d < N^delta) (default: 0.25) |
| `m` | `1` | the m value to use for the small roots method (default: 1) |
| `t` | `None` | the t value to use for the small roots method (default: automatically computed using m) |

#### `attack_multi_prime(...)`

- 调用：`attacks.rsa.boneh_durfee.attack_multi_prime(...)` → `attack_multi_prime(N, e, factor_bit_length, factors, delta=0.25, m=1, t=None)`
- 说明：Recovers the prime factors if the private exponent is too small.
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `factor_bit_length` | ✔ | the bit length of the prime factors |
| `factors` | ✔ | the number of prime factors in the modulus |
| `delta` | `0.25` | a predicted bound on the private exponent (d < n^delta) (default: 0.25) |
| `m` | `1` | the m value to use for the small roots method (default: 1) |
| `t` | `None` | the t value to use for the small roots method (default: automatically computed using m) |

### Cherkaoui Semmouni Attack

- 入口键：`rsa/cherkaoui_semmouni`
- 源码：[`attacks/rsa/cherkaoui_semmouni.py`](../attacks/rsa/cherkaoui_semmouni.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_cherkaoui_semmouni`

#### `attack(...)`

- 调用：`attacks.rsa.cherkaoui_semmouni.attack(...)` → `attack(N, e, beta, delta, m=1, t=None, check_bounds=True)`

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ |  |
| `e` | ✔ |  |
| `beta` | ✔ |  |
| `delta` | ✔ |  |
| `m` | `1` |  |
| `t` | `None` |  |
| `check_bounds` | `True` |  |

### Common Modulus Attack

- 入口键：`rsa/common_modulus`
- 源码：[`attacks/rsa/common_modulus.py`](../attacks/rsa/common_modulus.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_common_modulus`

#### `attack(...)`

- 调用：`attacks.rsa.common_modulus.attack(...)` → `attack(n, e1, c1, e2, c2)`
- 说明：Recovers the plaintext from two ciphertexts, encrypted using the same modulus and different public exponents.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the common modulus |
| `e1` | ✔ | the first public exponent |
| `c1` | ✔ | the ciphertext of the first encryption |
| `e2` | ✔ | the second public exponent |
| `c2` | ✔ | the ciphertext of the second encryption |

### CRT Fault Attack

- 入口键：`rsa/crt_fault_attack`
- 源码：[`attacks/rsa/crt_fault_attack.py`](../attacks/rsa/crt_fault_attack.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rsa.TestRSA.test_crt_fault_attack`

#### `attack(...)`

- 调用：`attacks.rsa.crt_fault_attack.attack(...)` → `attack(n, e, sign)`
- 说明：Recovers the prime factors from a modulus using a faulty RSA-CRT signing function.
- 返回：a tuple containing the prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `sign` | ✔ | the faulty RSA-CRT signing function |

### Extended Wiener Attack

- 入口键：`rsa/extended_wiener_attack`
- 源码：[`attacks/rsa/extended_wiener_attack.py`](../attacks/rsa/extended_wiener_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_extended_wiener_attack`

#### `attack(...)`

- 调用：`attacks.rsa.extended_wiener_attack.attack(...)` → `attack(n, e, max_s=20000, max_r=100, max_t=100)`
- 说明：Recovers the prime factors if the private exponent is too small.
- 参考：Dujella A., "Continued fractions and RSA with small secret exponent"
- 返回：a tuple containing the prime factors and the private exponent, or None if the private exponent was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `n` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `max_s` | `20000` | the amount of s values to try (default: 20000) |
| `max_r` | `100` | the amount of r values to try for each s value (default: 100) |
| `max_t` | `100` | the amount of t values to try for each s value (default: 100) |

### Håstad Attack

- 入口键：`rsa/hastad_attack`
- 源码：[`attacks/rsa/hastad_attack.py`](../attacks/rsa/hastad_attack.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rsa.TestRSA.test_hastad_attack`

#### `attack(...)`

- 调用：`attacks.rsa.hastad_attack.attack(...)` → `attack(N, e, c)`
- 说明：Recovers the plaintext from e ciphertexts, encrypted using different moduli and the same public exponent.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the moduli |
| `e` | ✔ | the public exponent |
| `c` | ✔ | the ciphertexts |

### Known CRT Exponents Attack

- 入口键：`rsa/known_crt_exponents`
- 源码：[`attacks/rsa/known_crt_exponents.py`](../attacks/rsa/known_crt_exponents.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_known_crt_exponents`

#### `attack(...)`

- 调用：`attacks.rsa.known_crt_exponents.attack(...)` → `attack(e_start, e_end, N=None, dp=None, dq=None, p_bit_length=None, q_bit_length=None)`
- 说明：Generates possible prime factors for a modulus, if d_p and/or d_q are known.
- 参考：Campagna M., Sethi A., "Key Recovery Method for CRT Implementation of RSA"
- 返回：a generator generating tuples containing possible prime factors

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `e_start` | ✔ | the start value of the public exponent (inclusive) |
| `e_end` | ✔ | the end value of the public exponent (exclusive) |
| `N` | `None` | the modulus, will be used to check the factors if not None (default: None) |
| `dp` | `None` | the d exponent for p, will be used to generate possible factors for p if not None (default: None) |
| `dq` | `None` | the d exponent for q, will be used to generate possible factors for q if not None (default: None) |
| `p_bit_length` | `None` | the bit length of p, will be used to check possible factors for p if not None (default: None) |
| `q_bit_length` | `None` | the bit length of q, will be used to check possible factors for q if not None (default: None) |

### Known D Attack

- 入口键：`rsa/known_d`
- 源码：[`attacks/rsa/known_d.py`](../attacks/rsa/known_d.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rsa.TestRSA.test_known_d`

#### `attack(...)`

- 调用：`attacks.rsa.known_d.attack(...)` → `attack(N, e, d)`
- 说明：Recovers the prime factors from a modulus if the public exponent and private exponent are known.
- 返回：a tuple containing the prime factors, or None if the factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `d` | ✔ | the private exponent |

### Low Public Exponent Attack

- 入口键：`rsa/low_exponent`
- 源码：[`attacks/rsa/low_exponent.py`](../attacks/rsa/low_exponent.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_low_exponent`

#### `attack(...)`

- 调用：`attacks.rsa.low_exponent.attack(...)` → `attack(e, c)`
- 说明：Recovers the plaintext from a ciphertext, encrypted using a very small public exponent (e.g. e = 3).
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `e` | ✔ | the public exponent |
| `c` | ✔ | the ciphertext |

### LSB Oracle Attack

- 入口键：`rsa/lsb_oracle`
- 源码：[`attacks/rsa/lsb_oracle.py`](../attacks/rsa/lsb_oracle.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_lsb_oracle`

#### `attack(...)`

- 调用：`attacks.rsa.lsb_oracle.attack(...)` → `attack(N, e, c, oracle)`
- 说明：Recovers the plaintext from the ciphertext using the LSB oracle (parity oracle) attack.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `c` | ✔ | the encrypted message |
| `oracle` | ✔ | a function which returns the last bit of a plaintext for a given ciphertext |

### Manger Attack

- 入口键：`rsa/manger`
- 源码：[`attacks/rsa/manger.py`](../attacks/rsa/manger.py)
- 依赖 SageMath：否
- 演示用例：`test.test_rsa.TestRSA.test_manger`

#### `attack(...)`

- 调用：`attacks.rsa.manger.attack(...)` → `attack(padding_oracle, n, e, c)`
- 说明：Recovers the plaintext using Manger's attack.
- 参考：Manger J., "A Chosen Ciphertext Attack on RSA Optimal Asymmetric Encryption Padding (OAEP) as Standardized in PKCS #1 v2.0"
- 返回：the plaintext (integer)

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `padding_oracle` | ✔ | the padding oracle taking integers, returns True if the PKCS #1 OAEP padding length is correct, False otherwise |
| `n` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `c` | ✔ | the ciphertext (integer) |

### Nitaj CRT-RSA Attack

- 入口键：`rsa/nitaj_crt_rsa`
- 源码：[`attacks/rsa/nitaj_crt_rsa.py`](../attacks/rsa/nitaj_crt_rsa.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_nitaj_crt_rsa`

#### `attack(...)`

- 调用：`attacks.rsa.nitaj_crt_rsa.attack(...)` → `attack(N, e, delta, m, t, check_bounds=True)`
- 说明：Recovers the prime factors if one of the CRT-RSA private exponents is too small.
- 参考：Nitaj A., "A new attack on RSA and CRT-RSA" (Section 4)
- 返回：a tuple containing the prime factors, or None if the factors could not be found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `delta` | ✔ | the parameter delta such that dp <= N^delta |
| `m` | ✔ | the parameter m for small roots |
| `t` | ✔ | the parameter t for small roots |
| `check_bounds` | `True` | perform bounds check (default: True) |

### Non-Coprime Exponent Attack

- 入口键：`rsa/non_coprime_exponent`
- 源码：[`attacks/rsa/non_coprime_exponent.py`](../attacks/rsa/non_coprime_exponent.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_non_coprime_exponent`

#### `attack(...)`

- 调用：`attacks.rsa.non_coprime_exponent.attack(...)` → `attack(N, e, phi, c)`
- 说明：Computes possible plaintexts when e is not coprime with Euler's totient.
- 参考：Shumow D., "Incorrectly Generated RSA Keys: How To Recover Lost Plaintexts"
- 返回：a generator generating possible plaintexts for c

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `phi` | ✔ | Euler's totient for the modulus |
| `c` | ✔ | the ciphertext |

### Partial Key Exposure Attack

- 入口键：`rsa/partial_key_exposure`
- 源码：[`attacks/rsa/partial_key_exposure.py`](../attacks/rsa/partial_key_exposure.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_partial_key_exposure`

#### `attack(...)`

- 调用：`attacks.rsa.partial_key_exposure.attack(...)` → `attack(N, e, partial_d, factor_e=True, m=1, t=None)`
- 说明：Recovers the prime factors of a modulus and the private exponent if part of the private exponent is known.
- 参考：Ernst M. et al., "Partial Key Exposure Attacks on RSA Up to Full Size Exponents"
- 返回：a tuple containing the prime factors and the private exponent, or None if the private exponent was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `partial_d` | ✔ | the partial private exponent d (PartialInteger) |
| `factor_e` | `True` | whether we should attempt to factor e (for BDF) if it is not prime (default: True) |
| `m` | `1` | the m value to use for the small roots method (default: 1) |
| `t` | `None` | the t value to use for the small roots method (default: automatically computed using m) |

### Related Message Attack

- 入口键：`rsa/related_message`
- 源码：[`attacks/rsa/related_message.py`](../attacks/rsa/related_message.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_related_message`

#### `attack(...)`

- 调用：`attacks.rsa.related_message.attack(...)` → `attack(N, e, c1, c2, f1, f2)`
- 说明：Recovers the shared secret if p1 and p2 are affinely related and encrypted with the same modulus and exponent.
- 返回：the shared secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `c1` | ✔ | the ciphertext of the first encryption |
| `c2` | ✔ | the ciphertext of the second encryption |
| `f1` | ✔ | the first function to apply to the shared secret |
| `f2` | ✔ | the second function to apply to the shared secret |

#### `attack_xor(...)`

- 调用：`attacks.rsa.related_message.attack_xor(...)` → `attack_xor(N, e, c1, c2, x)`
- 说明：Recovers the shared secret if p1 = p2 ^ x and encrypted with the same modulus and exponent.
- 返回：a generator generating possible values of the shared secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `c1` | ✔ | the ciphertext of the first encryption |
| `c2` | ✔ | the ciphertext of the second encryption |
| `x` | ✔ | the XOR difference |

### Stereotyped Message Attack

- 入口键：`rsa/stereotyped_message`
- 源码：[`attacks/rsa/stereotyped_message.py`](../attacks/rsa/stereotyped_message.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_stereotyped_message`

#### `attack(...)`

- 调用：`attacks.rsa.stereotyped_message.attack(...)` → `attack(N, e, c, partial_m, m=1, t=0)`
- 说明：Recovers the plaintext from the ciphertext if some bits of the plaintext are known, using Coppersmith's method.
- 返回：the plaintext

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent (should be "small": 3, 5, or 7 work best) |
| `c` | ✔ | the encrypted message |
| `partial_m` | ✔ | the partial plaintext message (PartialInteger) |
| `m` | `1` | the m value to use for the small roots method (default: 1) |
| `t` | `0` | the t value to use for the small roots method (default: 0) |

### Wiener's Attack

- 入口键：`rsa/wiener_attack`
- 源码：[`attacks/rsa/wiener_attack.py`](../attacks/rsa/wiener_attack.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_wiener_attack`

#### `attack(...)`

- 调用：`attacks.rsa.wiener_attack.attack(...)` → `attack(N, e)`
- 说明：Recovers the prime factors of a modulus and the private exponent if the private exponent is too small.
- 返回：a tuple containing the prime factors and the private exponent, or None if the private exponent was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |

### Wiener Attack (Common Prime RSA)

- 入口键：`rsa/wiener_attack_common_prime`
- 源码：[`attacks/rsa/wiener_attack_common_prime.py`](../attacks/rsa/wiener_attack_common_prime.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_wiener_attack_common_prime`

#### `attack(...)`

- 调用：`attacks.rsa.wiener_attack_common_prime.attack(...)` → `attack(N, e, delta=0.25, m=1, t=None, check_bounds=True)`
- 说明：Recovers the prime factors of a modulus and the private exponent if the private exponent is too small (Common Prime RSA version).
- 参考：Jochemsz E., May A., "A Strategy for Finding Roots of Multivariate Polynomials with New Applications in Attacking RSA Variants" (Section 5)
- 返回：a tuple containing the prime factors and the private exponent, or None if the private exponent was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `delta` | `0.25` | a predicted bound on the private exponent (d < N^delta) (default: 0.25) |
| `m` | `1` | the m value to use for the small roots method (default: 1) |
| `t` | `None` | the t value to use for the small roots method (default: automatically computed using m) |
| `check_bounds` | `True` | perform bounds check (default: True) |

### Wiener Attack (Lattice Variant)

- 入口键：`rsa/wiener_attack_lattice`
- 源码：[`attacks/rsa/wiener_attack_lattice.py`](../attacks/rsa/wiener_attack_lattice.py)
- 依赖 SageMath：是
- 演示用例：`test.test_rsa.TestRSA.test_wiener_attack_lattice`

#### `attack(...)`

- 调用：`attacks.rsa.wiener_attack_lattice.attack(...)` → `attack(N, e)`
- 说明：Recovers the prime factors of a modulus and the private exponent if the private exponent is too small.
- 参考：Nguyen P. Q., "Public-Key Cryptanalysis"
- 返回：a tuple containing the prime factors and the private exponent, or None if the private exponent was not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |

#### `attack_multiple_exponents_1(...)`

- 调用：`attacks.rsa.wiener_attack_lattice.attack_multiple_exponents_1(...)` → `attack_multiple_exponents_1(N, e, alpha)`
- 说明：Recovers the prime factors of a modulus given multiple public exponents with small corresponding private exponents.
- 参考：Howgrave-Graham N., Seifert J., "Extending Wiener’s Attack in the Presence of Many Decrypting Exponents"
- 返回：a tuple containing the prime factors, or None if the prime factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `alpha` | ✔ | the bound on the private exponents (i.e. d < N^alpha) |

#### `attack_multiple_exponents_2(...)`

- 调用：`attacks.rsa.wiener_attack_lattice.attack_multiple_exponents_2(...)` → `attack_multiple_exponents_2(N, e, d_bit_length, m=1)`
- 说明：Recovers the prime factors of a modulus given multiple public exponents with small corresponding private exponents.
- 参考：Aono Y., "Minkowski sum based lattice construction for multivariate simultaneous Coppersmith’s technique and applications to RSA" (Section 4)
- 返回：a tuple containing the prime factors, or None if the prime factors were not found

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `N` | ✔ | the modulus |
| `e` | ✔ | the public exponent |
| `d_bit_length` | ✔ | the bit length of the private exponents |
| `m` | `1` | the m value to use for the small roots method (default: 1) |

## Shamir 秘密共享

### Deterministic Coefficients Attack

- 入口键：`shamir_secret_sharing/deterministic_coefficients`
- 源码：[`attacks/shamir_secret_sharing/deterministic_coefficients.py`](../attacks/shamir_secret_sharing/deterministic_coefficients.py)
- 依赖 SageMath：否
- 演示用例：`test.test_shamir_secret_sharing.TestShamirSecretSharing.test_deterministic_coefficients`

#### `attack(...)`

- 调用：`attacks.shamir_secret_sharing.deterministic_coefficients.attack(...)` → `attack(p, k, a1, f, x, y)`
- 说明：Recovers the shared secret if the coefficients are generated deterministically, and a single share is given.
- 返回：the shared secret

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime used for Shamir's secret sharing |
| `k` | ✔ | the amount of shares needed to unlock the secret |
| `a1` | ✔ | the first coefficient of the polynomial |
| `f` | ✔ | a function which takes a coefficient and returns the next coefficient in the polynomial |
| `x` | ✔ | the x coordinate of the given share |
| `y` | ✔ | the y coordinate of the given share |

### Share Forgery Attack

- 入口键：`shamir_secret_sharing/share_forgery`
- 源码：[`attacks/shamir_secret_sharing/share_forgery.py`](../attacks/shamir_secret_sharing/share_forgery.py)
- 依赖 SageMath：否
- 演示用例：`test.test_shamir_secret_sharing.TestShamirSecretSharing.test_share_forgery`

#### `attack(...)`

- 调用：`attacks.shamir_secret_sharing.share_forgery.attack(...)` → `attack(p, s, s_, x, y, xs)`
- 说明：Forges a share to recombine into a new shared secret, s', if a single share and the x coordinates of the other participants are given.
- 返回：the forged share

| 参数 | 必填 | 说明 |
| --- | :---: | --- |
| `p` | ✔ | the prime used for Shamir's secret sharing |
| `s` | ✔ | the original shared secret |
| `s_` | ✔ | the target shared secret, s' |
| `x` | ✔ | the x coordinate of the given share |
| `y` | ✔ | the y coordinate of the given share |
| `xs` | ✔ | the x coordinates of the other participants (excluding the x coordinate of the given share) |

