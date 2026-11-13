# Crypto Attack Machine

> 把 [crypto-attacks](https://github.com/J1ann/crypto-attacks) 的全部密码学攻击收进一个仓库，
> 并配一个统一的调度器：**一条命令列出、查看并执行任意一个攻击**。

```text
$ python crypto_attack_machine.py list
$ python crypto_attack_machine.py info rsa/boneh_durfee
$ python crypto_attack_machine.py run rsa/wiener_attack --demo
```

**73 个攻击 / 22 个分类**，全部保留原始实现（RSA、格攻击、分组模式、ECC、LCG、LWE、背包、Shamir……），
外加一个零依赖的 Python 调度器 `crypto_attack_machine.py`。

> ⚠️ **免责声明**
> 本仓库仅供**教学、CTF 竞赛与授权安全研究**使用。所有代码都是公开论文中密码分析方法的实现，
> 请勿用于攻击你未获授权的系统或数据。使用者需自行承担因不当使用产生的一切后果。

---

## 目录

- [这是什么](#这是什么)
- [环境准备](#环境准备)
- [快速开始](#快速开始)
- [调度器用法](#调度器用法)
- [攻击总览](#攻击总览)
- [目录结构](#目录结构)
- [新增一个攻击](#新增一个攻击)
- [关于 `m` / `t` 参数](#关于-m--t-参数)
- [测试](#测试)
- [许可与致谢](#许可与致谢)

---

## 这是什么

| 部分 | 说明 |
| --- | --- |
| `attacks/` | 73 个攻击实现，按密码系统分目录（直接来自上游项目，保持原样） |
| `shared/` | 共享工具：格约减、小根求解、CRT、椭圆曲线生成、`PartialInteger` 等 |
| `test/` | 73 个攻击对应的单元测试，同时充当**可复现的演示用例** |
| `crypto_attack_machine.py` | 调度器：自动扫描攻击 → 分类展示 → 选一个跑起来 |
| `docs/` | 自动生成的攻击清单与参数手册 |

调度器做的事很简单但很省事：

- **自动发现**：扫描 `attacks/**/*.py`，解析函数签名、docstring 参数说明、论文引用和单元测试，
  不需要维护任何手工注册表（新增文件即自动出现在列表里）。
- **三种执行方式**：内置演示用例 / 自定义 JSON 参数 / 你自己的 PoC 脚本。
- **自动切换解释器**：调度器本身纯标准库（普通 `python3` 即可），真正执行时自动调用 `sage -python`。
- **可被脚本消费**：`list --json` 输出结构化清单，便于二次开发或接入其他工具。

## 环境准备

### 1. SageMath（必需）

绝大多数攻击依赖 `sage.all`（LLL、多项式环、椭圆曲线、`Qp` 等），所以必须装 SageMath。

```bash
# 检查是否已安装
sage -python --version     # 期望 >= Python 3.9

# 官方安装包 / 包管理器
#   macOS:   brew install --cask sage
#   Ubuntu:  sudo apt install sagemath
#   Windows: https://www.sagemath.org/download-windows.html （或使用 WSL2 安装 Linux 版）
#   其他:    https://www.sagemath.org/download.html
#   也可以直接用 Docker: docker run -it --rm -v "$PWD":/work sagemath/sagemath:latest
```

Windows 上的原生安装版会把 `sage.bat` 放在 `C:\Program Files\SageMath <版本>\runtime\bin\`，
若不在 `PATH` 中，用 `--sage` 指定即可：

```bash
python crypto_attack_machine.py doctor --sage "C:/Program Files/SageMath 10.4/runtime/bin/sage.bat"
```

### 2. PyCryptodome（分组模式攻击需要）

```bash
sage -pip install pycryptodome
```

### 3. 验证环境

```bash
python crypto_attack_machine.py doctor
```

输出会告诉你：调度器 Python 版本、SageMath 位置、`sage -python` 版本、PyCryptodome 是否可用、攻击总数。

## 快速开始

```bash
git clone https://github.com/J1ann/Crypto_attack_mechine.git
cd Crypto_attack_mechine

# 1) 看有什么
python crypto_attack_machine.py list

# 2) 跑一个内置演示（真实参数，来自 test/ 用例）
python crypto_attack_machine.py run rsa/wiener_attack --demo

# 3) 换成你自己的参数
python crypto_attack_machine.py run rsa/wiener_attack --params '{"N": 90581, "e": 17993}'

# 4) 不知道参数长什么样？先看说明，再生成模板
python crypto_attack_machine.py info rsa/boneh_durfee
python crypto_attack_machine.py run rsa/boneh_durfee --template > poc.py
```

想看全部命令：

```bash
python crypto_attack_machine.py --help
```

## 调度器用法

### `list` —— 列出全部攻击

```bash
python crypto_attack_machine.py list            # 按分类列出，标记是否有内置演示
python crypto_attack_machine.py list -v         # 附带一句话说明
python crypto_attack_machine.py list --json     # 结构化输出，供脚本消费
```

`✓ demo` 表示该攻击有可跑通的单元测试用例，`[N 入口]` 表示该文件里有多个公开函数
（例如 `factorization/branch_and_prune` 有 `factorize_pq` / `factorize_pqd` / `factorize_pqddpdq`）。

### `search` / `info` —— 查参数

```bash
python crypto_attack_machine.py search lattice
python crypto_attack_machine.py info rsa/boneh_durfee
```

`info` 会给出：源码路径、是否依赖 Sage、对应测试、每个入口函数的签名、每个参数的含义（必填/默认值）、
论文出处、返回值说明，以及可直接复制的示例命令。

### `run` —— 执行攻击

三种模式，任选其一：

| 模式 | 命令 | 适用场景 |
| --- | --- | --- |
| 内置演示 | `run <key> --demo` | 想确认它能跑通、看输出长什么样（**默认行为**） |
| 自定义参数 | `run <key> --params '{...}'` 或 `--params-file p.json` | 参数是整数/字符串/字节 |
| 自定义脚本 | `run <key> --script my_poc.py` | 参数是预言机、矩阵、椭圆曲线点等复杂对象 |

```bash
# 内置演示：直接复用 test/ 下的真实用例
python crypto_attack_machine.py run rsa/known_d --demo

# 自定义参数：JSON 键名即函数形参名
python crypto_attack_machine.py run rsa/common_modulus \
  --params '{"n": 123456789, "e1": 3, "c1": 111, "e2": 65537, "c2": 222}'

# 参数太长就放文件
python crypto_attack_machine.py run rsa/partial_key_exposure --params-file params.json

# 多入口模块指定函数
python crypto_attack_machine.py run factorization/branch_and_prune \
  --entry factorize_pqd --params '{"N": 0, "e": 0, "p": 0, "q": 0, "d": 0}'

# 想把自动生成的运行脚本留下来复现
python crypto_attack_machine.py run rsa/wiener_attack --params '{...}' --keep
```

#### 参数编码约定

JSON 只有数字/字符串/数组/对象，而攻击参数里有字节串、大整数、Sage 对象。用以下前缀表达：

| 写法 | 转换结果 | 例子 |
| --- | --- | --- |
| `123` / `"123"` | 整数 | `{"N": 90581}` |
| `"hex:00ff10"` | `bytes` | `{"iv": "hex:00000000000000000000000000000000"}` |
| `"bytes:hello"` | `bytes`（UTF-8） | `{"p": "bytes:admin=0"}` |
| `"b64:AAECAw=="` | `bytes`（Base64） | 二进制密文 |
| `"@json:[1,2,3]"` | 解析内层 JSON | 嵌套结构 |
| `"@eval:Matrix(ZZ, [[1,2],[3,4]])"` | 在 Sage 环境中 `eval` | 矩阵、曲线点、`PartialInteger(...)` |

`@eval:` 是逃生舱口：它会生成 `from sage.all import *` 的脚本再 eval，所以可以直接写
`"@eval:EllipticCurve(GF(101), [1, 1])(3, 6)"` 这类表达式。

#### 运行结果

成功时调度器会打印耗时与返回值；攻击返回 `None`（表示没打出来）时退出码为 `1`，
方便在脚本里判断：

```bash
python crypto_attack_machine.py run rsa/wiener_attack --params-file p.json
if [ $? -eq 0 ]; then
    echo "打穿了"
else
    echo "没打出来：参数不对，或需要调大 m/t"
fi
```

### `interactive` —— 交互式菜单

不带任何子命令直接运行，或显式使用：

```bash
python crypto_attack_machine.py interactive
```

```text
==================================================================
  Crypto Attack Machine · 交互模式
==================================================================
   1. ACD · 近似公因数                    3 个
   2. CBC 分组模式                        3 个
  ...
  21. RSA                               21 个
  22. Shamir 秘密共享                    2 个
   0. 退出

选择分类编号（或直接输入攻击键、关键词搜索）>
```

选中攻击后可：跑演示 / 输入 JSON 参数 / 打印并保存调用模板 / 查看参数说明。

### `test` —— 跑测试套件

```bash
python crypto_attack_machine.py test                       # 全部用例（几分钟）
python crypto_attack_machine.py test rsa/wiener_attack     # 单个攻击对应的用例
```

### `docs` —— 重新生成文档

```bash
python crypto_attack_machine.py docs            # 生成 docs/ATTACKS.md 与 docs/ATTACK_PARAMETERS.md
python crypto_attack_machine.py docs --readme   # 同时刷新本 README 的「攻击总览」区块
```

### 退出码

| 码 | 含义 |
| --- | --- |
| `0` | 成功 |
| `1` | 攻击跑完了但返回 `None`（未成功），或测试失败 |
| `2` | 用法/环境错误（参数缺失、JSON 非法、找不到 Sage 等） |
| `130` | 用户中断（Ctrl+C） |

## 攻击总览

<!-- BEGIN AUTO-GENERATED ATTACKS -->

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


<!-- END AUTO-GENERATED ATTACKS -->

每个入口的完整参数说明见 [`docs/ATTACK_PARAMETERS.md`](docs/ATTACK_PARAMETERS.md)，
按分类汇总的表格见 [`docs/ATTACKS.md`](docs/ATTACKS.md)。

## 目录结构

```text
Crypto_attack_mechine/
├── crypto_attack_machine.py     # 调度器（唯一入口，纯标准库）
├── attacks/                     # 73 个攻击实现，按密码系统分类
│   ├── rsa/                     #   21 个：Wiener、Boneh-Durfee、Håstad、Manger、Bleichenbacher…
│   ├── factorization/           #   12 个：Fermat、Coppersmith、ROCA、Shor 模拟、隐式分解…
│   ├── ecc/                     #    6 个：Smart、MOV、Frey-Rück、ECDSA nonce 重用…
│   ├── cbc/ ctr/ ecb/ ige/ …    #    分组模式攻击
│   ├── acd/ hnp/ lcg/ lwe/ …    #    数论与格方向
│   └── …
├── shared/                      # 共享工具：lattice、small_roots、polynomial、ecc、crt…
├── test/                        # 单元测试（同时是演示用例来源）
├── examples/                    # 可直接运行的示例 PoC
├── docs/
│   ├── ATTACKS.md               # 自动生成：攻击清单表
│   ├── ATTACK_PARAMETERS.md     # 自动生成：逐参数手册
│   └── UPSTREAM_README.md       # 上游项目原始 README（含 46 条参考文献）
├── requirements.txt
├── LICENSE                      # Apache-2.0（本仓库新增部分）
├── LICENSE-UPSTREAM             # MIT（attacks/ shared/ test/ 原始许可）
└── NOTICE                       # 归属声明
```

## 新增一个攻击

调度器不需要注册，**放进 `attacks/` 就行**：

1. 新建 `attacks/<分类>/<名字>.py`，实现一个顶层函数（推荐叫 `attack`）：

   ```python
   from sage.all import ZZ


   def attack(N, e):
       """
       Recovers the prime factors if the private exponent is too small.
       :param N: the modulus
       :param e: the public exponent
       :return: a tuple containing the prime factors, or None if not found
       """
       ...
   ```

2. 在 `test/` 里加一个名为 `test_<名字>` 的用例（可选，但这样 `run <key> --demo` 才能用）。

3. 已可运行：

   ```bash
   python crypto_attack_machine.py list | grep <名字>
   python crypto_attack_machine.py run <分类>/<名字> --demo
   ```

`docstring` 里写 `:param xxx: 说明`、`:return:`、`More information: 论文出处`，
`info` 命令会自动把这些整理成参数表。

## 关于 `m` / `t` 参数

格攻击（Boneh-Durfee、Coppersmith、隐式分解、HNP、ACD 等）都靠 `m` 和 `t` 调整格的大小：
格越大，LLL 越慢，但成功概率越高；太小则可能白算一场。上游给的两种用法：

```python
# 1) 从小到大试，直到打出来
m = 1
while True:
    res = attack(..., m=m)
    if res is not None:
        break
    m += 1

# 2) 用已知答案的样例调出合适的 m，再直接调用
attack(..., m=3)
```

调度器里对应的做法：

```bash
python crypto_attack_machine.py run rsa/boneh_durfee --demo        # 先看内置用例里 m 取多少能过
python crypto_attack_machine.py run rsa/boneh_durfee --params '{..., "m": 3}'
python crypto_attack_machine.py run rsa/boneh_durfee --params '{...}' --timeout 600
```

## 测试

```bash
sage -python -m unittest discover -s test -t . -v    # 全部
sage -python -m unittest -v test.test_rsa            # 单个模块
python crypto_attack_machine.py test rsa/wiener_attack
```

全部用例通常几分钟内跑完，具体取决于机器性能与格攻击的规模。

## 许可与致谢

本仓库是两部分拼起来的，许可证也相应分成两块：

| 范围 | 来源 | 许可 |
| --- | --- | --- |
| `attacks/`、`shared/`、`test/` | [J1ann/crypto-attacks](https://github.com/J1ann/crypto-attacks)，作者 Joachim Vandersmissen，原样拷贝 | **MIT**，见 [`LICENSE-UPSTREAM`](LICENSE-UPSTREAM) |
| `crypto_attack_machine.py`、`examples/`、`docs/`、`README.md` | 本仓库新增 | **Apache-2.0**，见 [`LICENSE`](LICENSE) |

完整归属声明见 [`NOTICE`](NOTICE)。上游 README（含每个攻击对应的论文清单，46 条参考文献）
保留在 [`docs/UPSTREAM_README.md`](docs/UPSTREAM_README.md)，便于溯源。

如果这份代码帮到了你，请也给上游项目点个 star。

