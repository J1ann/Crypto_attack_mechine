#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto Attack Machine —— 密码学攻击统一调度器
==============================================

把 `attacks/` 目录下的所有攻击集中到一个可交互 / 可脚本化的入口：

    python crypto_attack_machine.py list                # 列出全部攻击
    python crypto_attack_machine.py info rsa/boneh_durfee
    python crypto_attack_machine.py run rsa/wiener_attack --demo
    python crypto_attack_machine.py run cbc/bit_flipping --params '{"iv":"hex:00"*16 ...}'
    python crypto_attack_machine.py interactive         # 交互式菜单

本脚本只依赖标准库，可以放心用系统的普通 python3 运行；
真正执行攻击时会自动切换到 SageMath 的 python（`sage -python`），
因为绝大多数攻击依赖 `sage.all`（格约减、多项式环、椭圆曲线等）。

退出码约定：
    0  成功
    1  攻击执行了但没有得到结果（返回 None）或测试失败
    2  用法 / 环境错误
    130 用户中断
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
ATTACKS_DIR = ROOT / "attacks"
TEST_DIR = ROOT / "test"
DOCS_DIR = ROOT / "docs"
README_PATH = ROOT / "README.md"

BEGIN_MARK = "<!-- BEGIN AUTO-GENERATED ATTACKS -->"
END_MARK = "<!-- END AUTO-GENERATED ATTACKS -->"

# --------------------------------------------------------------------------- #
# 元数据：分类展示名称与顺序（与上游 README 保持一致）
# --------------------------------------------------------------------------- #

CATEGORY_ORDER: List[str] = [
    "acd",
    "cbc",
    "cbc_and_cbc_mac",
    "cbc_mac",
    "ctr",
    "ecb",
    "ecc",
    "elgamal_encryption",
    "elgamal_signature",
    "factorization",
    "gcm",
    "hnp",
    "ige",
    "knapsack",
    "lcg",
    "lwe",
    "mersenne_twister",
    "otp",
    "pseudoprimes",
    "rc4",
    "rsa",
    "shamir_secret_sharing",
]

CATEGORY_LABELS: Dict[str, str] = {
    "acd": "ACD · 近似公因数",
    "cbc": "CBC 分组模式",
    "cbc_and_cbc_mac": "CBC + CBC-MAC",
    "cbc_mac": "CBC-MAC",
    "ctr": "CTR 分组模式",
    "ecb": "ECB 分组模式",
    "ecc": "ECC · 椭圆曲线",
    "elgamal_encryption": "ElGamal 加密",
    "elgamal_signature": "ElGamal 签名",
    "factorization": "整数分解",
    "gcm": "GCM",
    "hnp": "HNP · 隐藏数问题",
    "ige": "IGE 分组模式",
    "knapsack": "背包密码",
    "lcg": "LCG · 线性同余",
    "lwe": "LWE",
    "mersenne_twister": "Mersenne Twister",
    "otp": "OTP · 一次性密码本",
    "pseudoprimes": "伪素数",
    "rc4": "RC4",
    "rsa": "RSA",
    "shamir_secret_sharing": "Shamir 秘密共享",
}

# 文件名 -> 展示标题的特殊情况
TITLE_OVERRIDES: Dict[str, str] = {
    "mp": "Multivariate Polynomial Attack",
    "ol": "Orthogonal Based Attack",
    "sda": "Simultaneous Diophantine Approximation",
    "gaa": "Ghafar-Ariffin-Asbullah Attack",
    "shor": "Shor's Algorithm (Classical Simulation)",
    "roca": "ROCA Attack",
    "fms": "Fluhrer-Mantin-Shamir Attack",
    "eam_key_reuse": "Key Reuse (Encrypt-and-MAC)",
    "etm_key_reuse": "Key Reuse (Encrypt-then-MAC)",
    "mte_key_reuse": "Key Reuse (MAC-then-Encrypt)",
    "arora_ge": "Arora-Ge Attack",
    "miller_rabin": "Miller-Rabin Pseudoprimes",
    "wiener_attack_common_prime": "Wiener Attack (Common Prime RSA)",
    "wiener_attack_lattice": "Wiener Attack (Lattice Variant)",
    "crt_fault_attack": "CRT Fault Attack",
    "plaintext_recovery_harder": "Plaintext Recovery (Harder)",
    "plaintext_recovery_hardest": "Plaintext Recovery (Hardest)",
    "mov_attack": "MOV Attack",
    "frey_ruck_attack": "Frey-Ruck Attack",
    "smart_attack": "Smart's Attack",
    "ecdsa_nonce_reuse": "ECDSA Nonce Reuse",
    "extended_hnp": "Extended HNP",
    "bkw": "BKW Attack",
    "boneh_durfee": "Boneh-Durfee Attack",
    "non_coprime_exponent": "Non-Coprime Exponent Attack",
    "nitaj_crt_rsa": "Nitaj CRT-RSA Attack",
    "wiener_attack": "Wiener's Attack",
    "frey_ruck_attack": "Frey-Rück Attack",
    "known_crt_exponents": "Known CRT Exponents Attack",
    "low_exponent": "Low Public Exponent Attack",
    "lsb_oracle": "LSB Oracle Attack",
    "state_recovery": "State Recovery Attack",
}

ABBREVIATIONS = {
    "rsa": "RSA",
    "cbc": "CBC",
    "mac": "MAC",
    "ecb": "ECB",
    "ctr": "CTR",
    "ige": "IGE",
    "acd": "ACD",
    "ecc": "ECC",
    "ecdsa": "ECDSA",
    "gcm": "GCM",
    "hnp": "HNP",
    "lcg": "LCG",
    "lwe": "LWE",
    "otp": "OTP",
    "rc4": "RC4",
    "crt": "CRT",
    "iv": "IV",
    "lsb": "LSB",
    "mov": "MOV",
    "dp": "dp",
    "dq": "dq",
    "phi": "phi",
    "wiener": "Wiener",
    "hastad": "Håstad",
    "nitaj": "Nitaj",
    "cherkaoui": "Cherkaoui",
    "semmouni": "Semmouni",
    "bleichenbacher": "Bleichenbacher",
    "coppersmith": "Coppersmith",
    "jochemsz": "Jochemsz",
    "howgrave": "Howgrave",
    "graham": "Graham",
    "herrmann": "Herrmann",
    "blomer": "Blömer",
    "aono": "Aono",
    "ernst": "Ernst",
    "coron": "Coron",
    "fouotsa": "Fouotsa",
    "arora": "Arora",
    "ge": "Ge",
    "fermat": "Fermat",
    "roca": "ROCA",
    "shor": "Shor",
    "fms": "FMS",
    "khadir": "Khadir",
    "manger": "Manger",
    "boneh": "Boneh",
    "durfee": "Durfee",
    "smart": "Smart",
    "frey": "Frey",
    "ruck": "Ruck",
    "mt19937": "MT19937",
    "crime": "CRIME",
}


# --------------------------------------------------------------------------- #
# 数据模型
# --------------------------------------------------------------------------- #


@dataclass
class Param:
    name: str
    default: Optional[str]
    doc: str

    @property
    def required(self) -> bool:
        return self.default is None


@dataclass
class Entry:
    """模块中的一个可调用入口（多数是 attack，少数是 factorize_pq / forge_tag 等）。"""

    name: str
    params: List[Param] = field(default_factory=list)
    summary: str = ""
    returns: str = ""
    reference: str = ""

    @property
    def required_params(self) -> List[Param]:
        return [p for p in self.params if p.required]

    @property
    def signature(self) -> str:
        parts = [p.name if p.required else f"{p.name}={p.default}" for p in self.params]
        return f"{self.name}({', '.join(parts)})"


@dataclass
class Attack:
    category: str
    name: str
    path: Path  # 相对仓库根目录
    module: str
    title: str
    entries: List[Entry] = field(default_factory=list)
    module_summary: str = ""
    test_id: Optional[str] = None
    needs_sage: bool = True

    @property
    def key(self) -> str:
        return f"{self.category}/{self.name}"

    @property
    def primary(self) -> Entry:
        return self.entries[0]

    @property
    def summary(self) -> str:
        return self.primary.summary or self.module_summary

    @property
    def params(self) -> List[Param]:
        return self.primary.params

    @property
    def required_params(self) -> List[Param]:
        return self.primary.required_params

    @property
    def signature(self) -> str:
        return self.primary.signature

    def entry(self, name: Optional[str]) -> Entry:
        if not name:
            return self.primary
        for e in self.entries:
            if e.name == name:
                return e
        available = ", ".join(e.name for e in self.entries)
        raise SystemExit(f"[cam] {self.key} 没有入口 '{name}'，可用入口: {available}")


# --------------------------------------------------------------------------- #
# 注册表：静态扫描 attacks/ 目录，无需手工维护
# --------------------------------------------------------------------------- #


def _parse_docstring(doc: str) -> Tuple[str, str, str, Dict[str, str]]:
    """从 attack() 的 docstring 中提取摘要、返回值、参考文献与参数说明。"""
    if not doc:
        return "", "", "", {}

    lines = [line.rstrip() for line in doc.expandtabs().splitlines()]
    summary_lines: List[str] = []
    returns = ""
    reference = ""
    params: Dict[str, str] = {}

    current_param: Optional[str] = None
    current_field: Optional[str] = None

    for raw in lines:
        line = raw.strip()
        if not line:
            current_field = None
            current_param = None
            continue

        m = re.match(r":param\s+(\w+)\s*:\s*(.*)", line)
        if m:
            current_param, current_field = m.group(1), "param"
            params[current_param] = m.group(2).strip()
            continue

        m = re.match(r":return\s*:\s*(.*)", line)
        if m:
            current_field = "return"
            returns = m.group(1).strip()
            continue

        if line.lower().startswith("more information"):
            current_field = "ref"
            reference = line.split(":", 1)[1].strip() if ":" in line else line
            continue

        if current_field == "param" and current_param:
            params[current_param] = (params[current_param] + " " + line).strip()
        elif current_field == "return":
            returns = (returns + " " + line).strip()
        elif current_field == "ref":
            reference = (reference + " " + line).strip()
        elif not summary_lines:
            summary_lines.append(line)

    summary = " ".join(summary_lines).strip()
    return summary, returns, reference, params


def _needs_sage(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "sage" or alias.name.startswith("sage."):
                    return True
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "sage" or node.module.startswith("sage."):
                return True
    return False


def _title_for(name: str) -> str:
    if name in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[name]
    words = []
    for token in name.split("_"):
        words.append(ABBREVIATIONS.get(token, token.capitalize()))
    title = " ".join(words)
    if "attack" not in title.lower() and "recovery" not in title.lower():
        title += " Attack"
    return title


_TEST_INDEX: Optional[Dict[str, str]] = None


def _test_index() -> Dict[str, str]:
    """扫描 test/test_*.py，建立 attack 名称 -> unittest 点分路径的索引。"""
    global _TEST_INDEX
    if _TEST_INDEX is not None:
        return _TEST_INDEX

    index: Dict[str, str] = {}
    if not TEST_DIR.is_dir():
        _TEST_INDEX = index
        return index

    for test_file in sorted(TEST_DIR.glob("test_*.py")):
        try:
            tree = ast.parse(test_file.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        module_id = f"test.{test_file.stem}"
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                    index.setdefault(item.name[5:], f"{module_id}.{node.name}.{item.name}")
    _TEST_INDEX = index
    return index


def _entry_from_function(fn: ast.FunctionDef) -> Entry:
    summary, returns, reference, param_docs = _parse_docstring(ast.get_docstring(fn) or "")

    args = fn.args
    positional = list(args.args)
    defaults: List[Optional[str]] = [None] * (len(positional) - len(args.defaults)) + [
        ast.unparse(d) for d in args.defaults
    ]

    params: List[Param] = []
    for arg, default in zip(positional, defaults):
        if arg.arg in ("self", "cls"):
            continue
        params.append(Param(name=arg.arg, default=default, doc=param_docs.get(arg.arg, "")))

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        params.append(
            Param(
                name=arg.arg,
                default=None if default is None else ast.unparse(default),
                doc=param_docs.get(arg.arg, ""),
            )
        )

    return Entry(name=fn.name, params=params, summary=summary, returns=returns, reference=reference)


def load_registry() -> List[Attack]:
    """扫描 attacks/**/*.py 构建攻击注册表。"""
    attacks: List[Attack] = []
    if not ATTACKS_DIR.is_dir():
        raise SystemExit(f"[cam] 未找到攻击目录: {ATTACKS_DIR}")

    tests = _test_index()

    for path in sorted(ATTACKS_DIR.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError) as exc:  # pragma: no cover
            print(f"[cam] 跳过无法解析的文件 {path}: {exc}", file=sys.stderr)
            continue

        # 公开的顶层函数都视为攻击入口；attack 优先，其余按文件内顺序排列
        entries = [
            _entry_from_function(node)
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        ]
        if not entries:
            continue
        entries.sort(key=lambda e: 0 if e.name == "attack" else 1)

        rel = path.relative_to(ROOT)
        attacks.append(
            Attack(
                category=path.parent.name,
                name=path.stem,
                path=rel,
                module=".".join(rel.with_suffix("").parts),
                title=_title_for(path.stem),
                entries=entries,
                module_summary=(ast.get_docstring(tree) or "").strip().splitlines()[0]
                if ast.get_docstring(tree)
                else "",
                test_id=tests.get(path.stem),
                needs_sage=_needs_sage(tree),
            )
        )

    order = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    attacks.sort(key=lambda a: (order.get(a.category, len(order)), a.category, a.name))
    return attacks


def find_attack(attacks: Sequence[Attack], query: str) -> Attack:
    """按 `分类/名称`、`分类.名称`、`名称` 或唯一子串定位攻击。"""
    q = query.strip().replace("\\", "/").replace(".", "/").lower()
    for a in attacks:
        if a.key.lower() == q:
            return a
    for a in attacks:
        if a.name.lower() == q.split("/")[-1] and q.count("/") <= 1:
            same = [b for b in attacks if b.name.lower() == a.name.lower()]
            if len(same) == 1:
                return a
    matches = [a for a in attacks if q in a.key.lower() or q in a.title.lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"[cam] 没有找到匹配 '{query}' 的攻击，试试 `list` 或 `search {query}`")
    listing = "\n".join(f"  - {a.key}  ({a.title})" for a in matches)
    raise SystemExit(f"[cam] '{query}' 匹配到多个攻击，请写得更精确：\n{listing}")


# --------------------------------------------------------------------------- #
# 输出辅助
# --------------------------------------------------------------------------- #


def _c(text: str, code: str, enabled: bool = True) -> str:
    if not enabled or not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(text: str) -> str:
    return _c(text, "1")


def dim(text: str) -> str:
    return _c(text, "2")


def green(text: str) -> str:
    return _c(text, "32")


def yellow(text: str) -> str:
    return _c(text, "33")


def red(text: str) -> str:
    return _c(text, "31")


def cyan(text: str) -> str:
    return _c(text, "36")


def truncate(text: str, width: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: max(0, width - 1)] + "…"


def group_by_category(attacks: Iterable[Attack]) -> Dict[str, List[Attack]]:
    grouped: Dict[str, List[Attack]] = {}
    for a in attacks:
        grouped.setdefault(a.category, []).append(a)
    return grouped


def category_label(category: str) -> str:
    return CATEGORY_LABELS.get(category, category.replace("_", " ").title())


# --------------------------------------------------------------------------- #
# 环境探测：找到可用的 SageMath python
# --------------------------------------------------------------------------- #


def _sage_candidates() -> List[Path]:
    candidates: List[Path] = []

    for exe in ("sage", "sage.bat", "sage.exe"):
        found = shutil.which(exe)
        if found:
            candidates.append(Path(found))

    env_sage = os.environ.get("SAGE")
    if env_sage:
        candidates.append(Path(env_sage))
    env_root = os.environ.get("SAGE_ROOT")
    if env_root:
        candidates.append(Path(env_root) / "bin" / "sage")

    patterns = []
    if sys.platform.startswith("win"):
        patterns = [
            "C:/Program Files/SageMath*/runtime/bin/sage*",
            "C:/Program Files (x86)/SageMath*/runtime/bin/sage*",
            "C:/SageMath/runtime/bin/sage*",
            "D:/SageMath/runtime/bin/sage*",
            "D:/Program Files/SageMath*/runtime/bin/sage*",
        ]
    elif sys.platform == "darwin":
        patterns = ["/Applications/SageMath*/sage", "/usr/local/bin/sage", "/opt/homebrew/bin/sage"]
    else:
        patterns = ["/usr/bin/sage", "/usr/local/bin/sage", "/opt/sagemath*/sage"]

    import glob

    for pattern in patterns:
        for hit in glob.glob(pattern):
            candidates.append(Path(hit))

    seen = set()
    unique = []
    for c in candidates:
        if c.exists() and c.name.lower().startswith("sage") and str(c) not in seen:
            seen.add(str(c))
            unique.append(c)
    return unique


def find_sage(explicit: Optional[str] = None) -> Optional[Path]:
    if explicit:
        path = Path(explicit)
        if not path.exists():
            raise SystemExit(f"[cam] 指定的 SageMath 路径不存在: {explicit}")
        return path
    found = _sage_candidates()
    return found[0] if found else None


def sage_command(sage: Path) -> List[str]:
    """把 sage 可执行文件包装成 `sage -python ...` 的形式。"""
    if sage.suffix.lower() in (".bat", ".cmd"):
        base = ["cmd", "/c", str(sage)]
    else:
        base = [str(sage)]
    return base + ["-python"]


def build_interpreter(args: argparse.Namespace, needs_sage: bool) -> Tuple[List[str], str]:
    """返回执行攻击所需的解释器前缀与人类可读描述。"""
    if getattr(args, "python", None):
        return [args.python], f"Python ({args.python})"
    sage = find_sage(getattr(args, "sage", None))
    if sage is not None:
        return sage_command(sage), f"SageMath ({sage})"
    if needs_sage:
        print(
            yellow(
                "[cam] 警告：未检测到 SageMath，改用当前 Python 执行。"
                "依赖 sage.all 的攻击会因此失败，请安装 SageMath 或用 --sage 指定路径。"
            ),
            file=sys.stderr,
        )
    return [sys.executable], f"Python ({sys.executable})"


def subprocess_env() -> Dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing if existing else "")
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_command(cmd: Sequence[str], title: str, timeout: Optional[int]) -> int:
    """执行子进程，实时透传输出，返回退出码。"""
    print(dim("$ " + " ".join(str(c) for c in cmd)))
    started = time.time()
    try:
        proc = subprocess.run(list(cmd), cwd=str(ROOT), env=subprocess_env(), timeout=timeout)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        print(red(f"[cam] {title} 超时（>{timeout}s 未完成），已终止。可用 --timeout 放宽或调小 m/t。"))
        return 1
    except FileNotFoundError:
        print(red(f"[cam] 找不到可执行文件: {cmd[0]}"))
        return 2
    except KeyboardInterrupt:
        return 130
    print(dim(f"[cam] {title} 结束，用时 {time.time() - started:.2f}s，退出码 {code}"))
    return code


# --------------------------------------------------------------------------- #
# 执行：三种运行方式
# --------------------------------------------------------------------------- #


def run_demo(attack: Attack, args: argparse.Namespace) -> int:
    if not attack.test_id:
        print(red(f"[cam] {attack.key} 没有内置测试用例。"))
        print("      可改用 `--params` 传参运行，或用 `--template` 打印调用模板。")
        return 2
    cmd, label = build_interpreter(args, attack.needs_sage)
    print(cyan(f"[cam] 运行内置演示（真实参数，来自 {attack.test_id}）"))
    print(cyan(f"[cam] 解释器：{label}"))
    return run_command(cmd + ["-m", "unittest", "-v", attack.test_id], f"demo {attack.key}", args.timeout)


DECODE_HELPERS = r'''
def _decode(value):
    """把 JSON 里的标记字符串转换成 Python / Sage 对象。"""
    if isinstance(value, str):
        if value.startswith("@eval:"):
            return eval(value[len("@eval:"):], EVAL_NS)  # noqa: S307 - 用户显式要求
        if value.startswith("hex:"):
            return bytes.fromhex(value[4:].replace(" ", ""))
        if value.startswith("b64:"):
            import base64
            return base64.b64decode(value[4:])
        if value.startswith("bytes:"):
            return value[len("bytes:"):].encode("utf-8")
        if value.startswith("@json:"):
            import json as _json
            return _json.loads(value[len("@json:"):])
        return value
    if isinstance(value, list):
        return [_decode(item) for item in value]
    if isinstance(value, dict):
        return {k: _decode(v) for k, v in value.items()}
    return value
'''


def build_param_script(attack: Attack, entry: Entry, params: Dict[str, object]) -> str:
    lines = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        f"# 由 crypto_attack_machine.py 自动生成的运行脚本：{attack.key} :: {entry.name}",
        "import sys",
        "from pprint import pprint",
        f"sys.path.insert(0, {str(ROOT)!r})",
        "",
    ]
    if attack.needs_sage:
        lines += [
            "try:",
            "    from sage.all import *  # noqa: F401,F403 - 供 @eval: 使用",
            "except ImportError:",
            "    pass",
        ]
    lines += [
        f"import {attack.module} as _attack_module",
        "",
        "EVAL_NS = dict(globals())",
        DECODE_HELPERS.strip(),
        "",
        f"ENTRY = getattr(_attack_module, {entry.name!r})",
        f"RAW_PARAMS = {json.dumps(params, ensure_ascii=False)}",
        "_params = {key: _decode(value) for key, value in RAW_PARAMS.items()}",
        "",
        "import inspect",
        "_sig = inspect.signature(ENTRY)",
        "_unknown = sorted(set(_params) - set(_sig.parameters))",
        "if _unknown:",
        "    print('[cam] 未知参数: ' + ', '.join(_unknown), file=sys.stderr)",
        "    print('[cam] 可用参数: ' + ', '.join(_sig.parameters), file=sys.stderr)",
        "    sys.exit(2)",
        "_missing = [n for n, p in _sig.parameters.items()",
        "            if p.default is inspect._empty and n not in _params]",
        "if _missing:",
        "    print('[cam] 缺少必填参数: ' + ', '.join(_missing), file=sys.stderr)",
        "    sys.exit(2)",
        "",
        "import time",
        "print('[cam] 调用 ' + %r)" % f"{attack.module}.{entry.name}(**params)",
        "_started = time.time()",
        "result = ENTRY(**_params)",
        "_elapsed = time.time() - _started",
        "print()",
        "print('-' * 70)",
        f"print('[cam] attack  : {attack.key} :: {entry.name}')",
        "print(f'[cam] elapsed : {_elapsed:.3f}s')",
        "if result is None:",
        "    print('[cam] result  : None  ->  攻击没有成功（参数或 m/t 需要调整）')",
        "    print('-' * 70)",
        "    sys.exit(1)",
        "print('[cam] result  :')",
        "pprint(result)",
        "print('-' * 70)",
        "",
    ]
    return "\n".join(lines)


def run_with_params(
    attack: Attack, entry: Entry, params: Dict[str, object], args: argparse.Namespace
) -> int:
    unknown = {p.name for p in entry.params}
    extra = sorted(set(params) - unknown)
    if extra:
        print(yellow(f"[cam] 提示：{attack.key}::{entry.name} 没有这些参数，仍会传递给攻击函数：{', '.join(extra)}"))
    missing = [p.name for p in entry.required_params if p.name not in params]
    if missing:
        print(red(f"[cam] 缺少必填参数: {', '.join(missing)}"))
        print(f"      查看参数说明：python crypto_attack_machine.py info {attack.key}")
        return 2

    code = build_param_script(attack, entry, params)
    cmd, label = build_interpreter(args, attack.needs_sage)
    print(cyan(f"[cam] 解释器：{label}"))

    if args.keep:
        run_dir = ROOT / "runs"
        run_dir.mkdir(exist_ok=True)
        script_path = run_dir / f"run_{attack.category}_{attack.name}_{int(time.time())}.py"
        script_path.write_text(code, encoding="utf-8")
        print(dim(f"[cam] 运行脚本已保存: {script_path}"))
        try:
            return run_command(cmd + [str(script_path)], f"run {attack.key}", args.timeout)
        finally:
            pass

    tmp = tempfile.NamedTemporaryFile(
        "w", suffix=".py", prefix=f"cam_{attack.name}_", delete=False, encoding="utf-8"
    )
    try:
        tmp.write(code)
        tmp.close()
        return run_command(cmd + [tmp.name], f"run {attack.key}", args.timeout)
    finally:
        os.unlink(tmp.name)


def run_script(attack: Attack, script: Path, args: argparse.Namespace) -> int:
    if not script.exists():
        print(red(f"[cam] 脚本不存在: {script}"))
        return 2
    cmd, label = build_interpreter(args, attack.needs_sage)
    print(cyan(f"[cam] 解释器：{label}"))
    return run_command(cmd + [str(script.resolve())], f"script {script.name}", args.timeout)


def _placeholder_value(param: Param) -> Tuple[Optional[str], List[str]]:
    """为参数生成占位值；返回 (赋值表达式, 需要的 stub 代码)，表达式为 None 表示已由 stub 定义。"""
    doc = (param.doc or "").lower()
    if "oracle" in doc or "oracle" in param.name:
        hint = f"  # {param.doc}" if param.doc else ""
        stub = [
            f"def {param.name}(*args, **kwargs):{hint}",
            f'    """TODO: 接上你自己的 {param.name}（真实服务或本地实现）。"""',
            "    raise NotImplementedError",
            "",
        ]
        return None, stub
    if "bytes" in doc or "bytearray" in doc:
        return 'b""', []
    if "bit_length" in param.name or "bit length" in doc:
        return "1024", []
    if "matrix" in doc:
        return "0  # TODO: 填入矩阵", []
    if "point" in doc:
        return "0  # TODO: 填入椭圆曲线上的点", []
    return "0", []


def render_template(attack: Attack, entry: Entry) -> str:
    out: List[str] = [
        "#!/usr/bin/env python3",
        "# -*- coding: utf-8 -*-",
        f"# {attack.title} —— {attack.key} :: {entry.name}",
        f"# 运行： python crypto_attack_machine.py run {attack.key} --script <本文件>",
        "# 或直接： sage -python <本文件>.py",
        "import os",
        "import sys",
        "",
        "# 自动定位仓库根目录（本文件放在 examples/ 时可直接运行）",
        "_HERE = os.path.dirname(os.path.realpath(__file__))",
        "_PARENT = os.path.dirname(_HERE)",
        f'_ROOT = _PARENT if os.path.isdir(os.path.join(_PARENT, "attacks")) else {str(ROOT)!r}',
        "sys.path.insert(1, _ROOT)",
        "",
    ]
    if attack.needs_sage:
        out += ["from sage.all import *  # noqa: F401,F403", ""]
    out += [f"from attacks.{attack.category} import {attack.name}", ""]
    if entry.summary:
        for chunk in _wrap_comment(entry.summary, 92):
            out.append(f"# {chunk}")
    if entry.reference:
        for chunk in _wrap_comment(f"参考: {entry.reference}", 92):
            out.append(f"# {chunk}")
    out.append("")

    stubs: List[str] = []
    assignments: List[str] = []
    for p in entry.params:
        if not p.required:
            doc = f"  # {p.doc}" if p.doc else ""
            assignments.append(f"# {p.name} = {p.default}{doc}   # 可选，按需取消注释")
            continue
        value, stub = _placeholder_value(p)
        stubs.extend(stub)
        if value is not None:
            doc = f"  # {p.doc}" if p.doc else ""
            assignments.append(f"{p.name} = {value}{doc}")

    out.extend(stubs)
    out.extend(assignments)

    call_args = ", ".join(f"{p.name}={p.name}" for p in entry.params if p.required)
    out += ["", f"result = {attack.name}.{entry.name}({call_args})"]
    if entry.returns:
        out.append(f"# 期望返回: {truncate(entry.returns, 100)}")
    out += ["print(result)", ""]
    return "\n".join(out)


def _wrap_comment(text: str, width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines or [""]


# --------------------------------------------------------------------------- #
# 命令实现
# --------------------------------------------------------------------------- #


def cmd_list(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    grouped = group_by_category(attacks)
    total_demo = sum(1 for a in attacks if a.test_id)

    if args.json:
        payload = [
            {
                "key": a.key,
                "title": a.title,
                "module": a.module,
                "entry": a.primary.name,
                "signature": a.signature,
                "summary": a.summary,
                "entries": [
                    {
                        "name": e.name,
                        "signature": e.signature,
                        "summary": e.summary,
                        "params": [
                            {"name": p.name, "required": p.required, "doc": p.doc} for p in e.params
                        ],
                        "returns": e.returns,
                    }
                    for e in a.entries
                ],
                "returns": a.primary.returns,
                "reference": a.primary.reference,
                "test": a.test_id,
                "needs_sage": a.needs_sage,
            }
            for a in attacks
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(bold(f"\nCrypto Attack Machine · 共 {len(attacks)} 个攻击，{len(grouped)} 个分类"))
    print(dim(f"{total_demo} 个攻击带内置演示用例（--demo 可直接跑通）\n"))

    width = max((len(a.key) for a in attacks), default=20) + 2
    for category, items in grouped.items():
        print(bold(cyan(f"■ {category_label(category)}  ({len(items)})")))
        for a in items:
            flag = green("✓ demo") if a.test_id else dim("· 仅参数")
            multi = dim(f" [{len(a.entries)} 入口]") if len(a.entries) > 1 else ""
            print(f"  {a.key:<{width}} {a.title:<42} {flag}{multi}")
            if args.verbose and a.summary:
                print(f"  {'':<{width}} {dim(truncate(a.summary, 96))}")
        print()
    print(dim("用法: run <key> --demo | --params '<json>' | --script <file>     详情: info <key>"))
    return 0


def cmd_search(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    needle = args.keyword.lower()
    hits = [
        a
        for a in attacks
        if needle in a.key.lower()
        or needle in a.title.lower()
        or needle in a.summary.lower()
        or needle in " ".join(p.name for p in a.params).lower()
    ]
    if not hits:
        print(yellow(f"没有找到与 '{args.keyword}' 相关的攻击。"))
        return 1
    print(bold(f"\n找到 {len(hits)} 个匹配 '{args.keyword}' 的攻击：\n"))
    for a in hits:
        flag = green("[demo]") if a.test_id else dim("[params]")
        print(f"  {a.key:<34} {flag} {a.title}")
        print(f"  {'':<34} {dim(truncate(a.summary, 88))}")
    print()
    return 0


def cmd_info(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    attack = find_attack(attacks, args.key)
    entry = attack.entry(getattr(args, "entry", None))

    print()
    print(bold(f"{attack.title}"))
    print(f"  key       : {cyan(attack.key)}")
    print(f"  文件      : {attack.path.as_posix()}")
    print(f"  模块      : {attack.module}")
    print(f"  依赖 Sage : {'是' if attack.needs_sage else '否（纯 Python）'}")
    print(f"  演示用例  : {attack.test_id or dim('无')}")
    if len(attack.entries) > 1:
        names = ", ".join(e.name for e in attack.entries)
        print(f"  入口      : {names}  （默认 {entry.name}，可用 --entry 切换）")
    print()

    for idx, item in enumerate(attack.entries):
        if len(attack.entries) > 1:
            tag = green(" 默认") if idx == 0 else ""
            print(bold(f"  ▸ {item.name}(...){tag}"))
        else:
            print(bold(f"  ▸ {item.name}(...)"))
        if item.summary:
            for chunk in _wrap_comment(item.summary, 84):
                print(f"    {chunk}")
        if item.reference:
            print(f"    {dim('参考: ' + truncate(item.reference, 96))}")
        print()
        if not item.params:
            print(dim("    该入口无参数"))
        for p in item.params:
            state = red("必填") if p.required else dim(f"可选={p.default}")
            print(f"    {p.name:<18} {state:<20} {truncate(p.doc, 78)}")
        if item.returns:
            print(f"    {dim('返回: ' + truncate(item.returns, 96))}")
        print()

    print(bold("  示例"))
    print(dim(f"    python crypto_attack_machine.py run {attack.key} --demo"))
    print(dim(f"    python crypto_attack_machine.py run {attack.key} --template"))
    required = [p.name for p in entry.required_params]
    if required:
        sample = json.dumps({name: 0 for name in required}, ensure_ascii=False)
        print(dim(f"    python crypto_attack_machine.py run {attack.key} --params '{sample}'"))
    print()
    return 0


def cmd_doctor(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    print(bold("\n环境自检"))
    print(f"  仓库根目录 : {ROOT}")
    print(f"  调度器 Python: {sys.version.split()[0]} ({sys.executable})")

    sage = find_sage(getattr(args, "sage", None))
    if sage is None:
        print(yellow("  SageMath   : 未找到。绝大多数攻击依赖 sage.all，请安装 SageMath 9.2+ (Python 3.9+)"))
        print(dim("               下载: https://www.sagemath.org/download.html"))
        print(dim("               或用 --sage 指定 sage 可执行文件路径"))
    else:
        print(green(f"  SageMath   : {sage}"))
        try:
            out = subprocess.run(
                sage_command(sage) + ["--version"],
                capture_output=True,
                text=True,
                timeout=120,
                env=subprocess_env(),
            )
            version = (out.stdout or out.stderr).strip().splitlines()
            print(f"  sage -python: {version[0] if version else '未知'}")
        except Exception as exc:  # pragma: no cover
            print(yellow(f"  无法执行 sage -python --version: {exc}"))

        try:
            check = subprocess.run(
                sage_command(sage)
                + ["-c", "import Crypto; print('pycryptodome', Crypto.__version__)"],
                capture_output=True,
                text=True,
                timeout=180,
                env=subprocess_env(),
            )
            line = (check.stdout or check.stderr).strip().splitlines()
            if check.returncode == 0:
                print(green(f"  PyCryptodome: {line[-1] if line else '已安装'}"))
            else:
                print(yellow("  PyCryptodome: 未安装（部分分组模式攻击需要）"))
                print(dim("               sage -pip install pycryptodome"))
        except Exception as exc:  # pragma: no cover
            print(yellow(f"  无法检测 PyCryptodome: {exc}"))

    print(f"  攻击总数   : {len(attacks)}（{len(group_by_category(attacks))} 个分类）")
    with_demo = sum(1 for a in attacks if a.test_id)
    print(f"  演示可用   : {with_demo} 个")
    print()
    return 0


def cmd_run(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    attack = find_attack(attacks, args.key)
    entry = attack.entry(args.entry)

    if args.template:
        print(render_template(attack, entry))
        return 0

    if args.script:
        return run_script(attack, Path(args.script), args)

    if args.params or args.params_file:
        raw = args.params
        if args.params_file:
            try:
                raw = Path(args.params_file).read_text(encoding="utf-8")
            except OSError as exc:
                print(red(f"[cam] 无法读取参数文件: {exc}"))
                return 2
        try:
            params = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(red(f"[cam] 参数不是合法 JSON: {exc}"))
            print(dim("      例：--params '{\"N\": 12345, \"e\": 65537}'"))
            return 2
        if not isinstance(params, dict):
            print(red("[cam] 参数必须是 JSON 对象（键值对）"))
            return 2
        return run_with_params(attack, entry, params, args)

    # 默认：跑内置演示
    if args.entry and args.entry != attack.primary.name:
        print(yellow(f"[cam] 注意：演示用例对应的是 {attack.primary.name}，--entry 仅在 --params 模式下生效"))
    return run_demo(attack, args)


def cmd_test(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    cmd, label = build_interpreter(args, needs_sage=True)
    print(cyan(f"[cam] 解释器：{label}"))
    if args.pattern:
        target = args.pattern
        if target in {a.key for a in attacks}:
            target = find_attack(attacks, target).test_id or target
        cmd = cmd + ["-m", "unittest", "-v", target]
    else:
        cmd = cmd + ["-m", "unittest", "discover", "-s", "test", "-t", ".", "-v"]
    print(dim("[cam] 提示：全部用例几分钟左右；单个攻击建议用 run <key> --demo"))
    return run_command(cmd, "test suite", args.timeout)


def _markdown_inventory(attacks: Sequence[Attack]) -> str:
    lines: List[str] = []
    grouped = group_by_category(attacks)
    lines.append(f"共 **{len(attacks)}** 个攻击，覆盖 **{len(grouped)}** 个分类。")
    lines.append("")
    for category, items in grouped.items():
        lines.append(f"### {category_label(category)}（{len(items)}）")
        lines.append("")
        lines.append("| 攻击 | 入口键 | 参数签名 | 演示 |")
        lines.append("| --- | --- | --- | :---: |")
        for a in items:
            sig = a.signature.replace("|", "\\|")
            if len(sig) > 68:
                sig = sig[:67] + "…"
            label = a.title + (f" (+{len(a.entries) - 1})" if len(a.entries) > 1 else "")
            lines.append(
                f"| [{label}]({a.path.as_posix()}) | `{a.key}` | `{sig}` | {'✅' if a.test_id else '—'} |"
            )
        lines.append("")
    return "\n".join(lines)


def _markdown_details(attacks: Sequence[Attack]) -> str:
    lines: List[str] = ["# 攻击参数手册", "", "由 `python crypto_attack_machine.py docs` 自动生成，请勿手工编辑。", ""]
    grouped = group_by_category(attacks)
    for category, items in grouped.items():
        lines.append(f"## {category_label(category)}")
        lines.append("")
        for a in items:
            lines.append(f"### {a.title}")
            lines.append("")
            lines.append(f"- 入口键：`{a.key}`")
            lines.append(f"- 源码：[`{a.path.as_posix()}`](../{a.path.as_posix()})")
            lines.append(f"- 依赖 SageMath：{'是' if a.needs_sage else '否'}")
            if a.test_id:
                lines.append(f"- 演示用例：`{a.test_id}`")
            lines.append("")
            for e in a.entries:
                lines.append(f"#### `{e.name}(...)`")
                lines.append("")
                lines.append(f"- 调用：`{a.module}.{e.name}(...)` → `{e.signature}`")
                if e.summary:
                    lines.append(f"- 说明：{e.summary}")
                if e.reference:
                    lines.append(f"- 参考：{e.reference}")
                if e.returns:
                    lines.append(f"- 返回：{e.returns}")
                if e.params:
                    lines.append("")
                    lines.append("| 参数 | 必填 | 说明 |")
                    lines.append("| --- | :---: | --- |")
                    for p in e.params:
                        req = "✔" if p.required else f"`{p.default}`"
                        doc = (p.doc or "").replace("|", "\\|")
                        lines.append(f"| `{p.name}` | {req} | {doc} |")
                lines.append("")
    return "\n".join(lines)


def cmd_docs(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    DOCS_DIR.mkdir(exist_ok=True)
    inventory = _markdown_inventory(attacks)
    details = _markdown_details(attacks)

    inv_path = DOCS_DIR / "ATTACKS.md"
    inv_path.write_text(
        "# 攻击总览\n\n"
        "> 本文件由 `python crypto_attack_machine.py docs` 自动生成，请勿手工编辑。\n\n" + inventory + "\n",
        encoding="utf-8",
    )
    det_path = DOCS_DIR / "ATTACK_PARAMETERS.md"
    det_path.write_text(details + "\n", encoding="utf-8")
    print(green(f"[cam] 已生成 {inv_path.relative_to(ROOT)}"))
    print(green(f"[cam] 已生成 {det_path.relative_to(ROOT)}"))

    if args.readme:
        if not README_PATH.exists():
            print(red("[cam] 找不到 README.md，跳过 README 注入"))
            return 0
        text = README_PATH.read_text(encoding="utf-8")
        if BEGIN_MARK not in text or END_MARK not in text:
            print(red("[cam] README.md 中缺少自动生成标记，跳过注入"))
            print(dim(f"      需要包含 {BEGIN_MARK} 与 {END_MARK}"))
            return 0
        head, rest = text.split(BEGIN_MARK, 1)
        _, tail = rest.split(END_MARK, 1)
        new_text = f"{head}{BEGIN_MARK}\n\n{inventory}\n\n{END_MARK}{tail}"
        README_PATH.write_text(new_text, encoding="utf-8")
        print(green("[cam] 已刷新 README.md 中的攻击清单"))
    return 0


# --------------------------------------------------------------------------- #
# 交互模式
# --------------------------------------------------------------------------- #


def _prompt(text: str) -> str:
    try:
        return input(text)
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(130)


def cmd_interactive(attacks: Sequence[Attack], args: argparse.Namespace) -> int:
    grouped = group_by_category(attacks)
    categories = list(grouped)
    while True:
        print()
        print(bold("=" * 66))
        print(bold("  Crypto Attack Machine · 交互模式"))
        print(bold("=" * 66))
        for i, category in enumerate(categories, 1):
            print(f"  {i:>2}. {category_label(category):<34} {dim(f'{len(grouped[category])} 个')}")
        print(f"   0. {dim('退出')}")
        choice = _prompt("\n选择分类编号（或直接输入攻击键、关键词搜索）> ").strip()
        if choice in ("0", "q", "quit", "exit"):
            return 0
        if not choice:
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            items = grouped[categories[int(choice) - 1]]
        else:
            try:
                attack = find_attack(attacks, choice)
            except SystemExit as exc:
                print(exc)
                continue
            _attack_menu(attack, args)
            continue

        while True:
            print()
            print(bold(f"  {category_label(categories[int(choice) - 1])}"))
            width = max(len(a.key) for a in items) + 2
            for i, a in enumerate(items, 1):
                flag = green("✓") if a.test_id else dim("·")
                print(f"  {i:>2}. {flag} {a.key:<{width}} {a.title}")
            sel = _prompt("\n选择攻击编号（0 返回）> ").strip()
            if sel in ("0", "b", "back", ""):
                break
            if not sel.isdigit() or not (1 <= int(sel) <= len(items)):
                print(yellow("  无效编号"))
                continue
            if not _attack_menu(items[int(sel) - 1], args):
                return 0


def _attack_menu(attack: Attack, args: argparse.Namespace) -> bool:
    """单个攻击的操作菜单。返回 False 表示用户要求退出程序。"""
    while True:
        print()
        print(bold(f"▸ {attack.title}  ({attack.key})"))
        if attack.summary:
            print(dim(f"  {truncate(attack.summary, 100)}"))
        print(f"  参数: {attack.signature}")
        if len(attack.entries) > 1:
            print(f"  入口: {', '.join(e.name for e in attack.entries)}")
        print(f"  依赖 Sage: {'是' if attack.needs_sage else '否'}")
        print()
        print("  1. 运行内置演示（真实参数）")
        print("  2. 自定义参数运行（JSON）")
        print("  3. 打印调用模板 / 生成脚本")
        print("  4. 查看完整参数说明")
        print("  0. 返回")
        sel = _prompt("\n选择操作 > ").strip()
        if sel in ("0", "b", ""):
            return True
        if sel == "1":
            run_demo(attack, args)
        elif sel == "2":
            entry = attack.primary
            if len(attack.entries) > 1:
                names = ", ".join(e.name for e in attack.entries)
                picked = _prompt(f"入口函数（{names}，回车默认 {entry.name}）> ").strip()
                if picked:
                    try:
                        entry = attack.entry(picked)
                    except SystemExit as exc:
                        print(red(f"  {exc}"))
                        continue
            print(dim(f"  参数: {entry.signature}"))
            raw = _prompt("输入 JSON 参数（如 {\"N\": 123, \"e\": 65537}）> ").strip()
            if not raw:
                continue
            try:
                params = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(red(f"  JSON 解析失败: {exc}"))
                continue
            if isinstance(params, dict):
                run_with_params(attack, entry, params, args)
            else:
                print(red("  需要 JSON 对象"))
        elif sel == "3":
            entry = attack.primary
            if len(attack.entries) > 1:
                names = ", ".join(e.name for e in attack.entries)
                picked = _prompt(f"入口函数（{names}，回车默认 {entry.name}）> ").strip()
                if picked:
                    try:
                        entry = attack.entry(picked)
                    except SystemExit as exc:
                        print(red(f"  {exc}"))
                        continue
            template = render_template(attack, entry)
            print()
            print(template)
            save = _prompt("保存为 examples/ 下的脚本？(y/N) > ").strip().lower()
            if save == "y":
                target_dir = ROOT / "examples"
                target_dir.mkdir(exist_ok=True)
                suffix = "" if entry.name == attack.primary.name else f"_{entry.name}"
                target = target_dir / f"{attack.category}_{attack.name}{suffix}.py"
                target.write_text(template, encoding="utf-8")
                print(green(f"  已保存: {target.relative_to(ROOT)}"))
                print(dim(f"  运行: python crypto_attack_machine.py run {attack.key} --script {target}"))
        elif sel == "4":
            ns = argparse.Namespace(key=attack.key)
            cmd_info([attack], ns)
        else:
            print(yellow("  无效选择"))


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crypto_attack_machine.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Crypto Attack Machine —— 统一调度 crypto-attacks 中的全部密码学攻击。",
        epilog=(
            "示例:\n"
            "  python crypto_attack_machine.py list\n"
            "  python crypto_attack_machine.py info rsa/boneh_durfee\n"
            "  python crypto_attack_machine.py run rsa/wiener_attack --demo\n"
            "  python crypto_attack_machine.py run rsa/wiener_attack --params '{\"N\": 0, \"e\": 0}'\n"
            "  python crypto_attack_machine.py run rsa/boneh_durfee --script examples/boneh_durfee_demo.py\n"
            "  python crypto_attack_machine.py run cbc/bit_flipping --template > poc.py\n"
            "  python crypto_attack_machine.py interactive\n"
            "  python crypto_attack_machine.py doctor\n"
            "  python crypto_attack_machine.py test rsa/wiener_attack\n"
        ),
    )
    parser.add_argument("--sage", help="SageMath 的 sage 可执行文件路径（自动探测失败时使用）")
    parser.add_argument("--python", help="直接指定解释器，覆盖 SageMath 检测")
    parser.add_argument("--timeout", type=int, default=None, help="单个任务超时秒数（默认不限制）")

    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="列出全部攻击")
    p_list.add_argument("-v", "--verbose", action="store_true", help="附带一句话说明")
    p_list.add_argument("--json", action="store_true", help="输出 JSON（便于脚本消费）")

    p_search = sub.add_parser("search", help="按关键词搜索攻击")
    p_search.add_argument("keyword")

    p_info = sub.add_parser("info", help="查看某个攻击的参数与说明")
    p_info.add_argument("key")
    p_info.add_argument("--entry", help="查看指定入口函数（默认第一个）")

    p_run = sub.add_parser("run", help="运行某个攻击")
    p_run.add_argument("key", help="攻击入口键，如 rsa/wiener_attack")
    p_run.add_argument("--entry", help="指定入口函数（默认 attack，多入口模块可用）")
    p_run.add_argument("--demo", action="store_true", help="运行内置演示用例（默认行为）")
    p_run.add_argument("--params", help="JSON 字符串形式的攻击参数")
    p_run.add_argument("--params-file", help="从 JSON 文件读取攻击参数")
    p_run.add_argument("--script", help="运行自定义 PoC 脚本")
    p_run.add_argument("--template", action="store_true", help="只打印调用模板，不执行")
    p_run.add_argument("--keep", action="store_true", help="把生成的运行脚本保存到 runs/")

    p_test = sub.add_parser("test", help="运行测试套件")
    p_test.add_argument("pattern", nargs="?", help="攻击入口键或 unittest 目标")

    sub.add_parser("interactive", help="交互式选择并执行攻击")
    sub.add_parser("doctor", help="检查运行环境（SageMath / PyCryptodome）")

    p_docs = sub.add_parser("docs", help="生成攻击清单文档")
    p_docs.add_argument("--readme", action="store_true", help="同时刷新 README.md 中的自动生成区块")

    # 让 --sage / --python / --timeout 既能写在子命令前，也能写在子命令后
    for subparser in sub.choices.values():
        subparser.add_argument("--sage", default=argparse.SUPPRESS, help="SageMath 的 sage 可执行文件路径")
        subparser.add_argument("--python", default=argparse.SUPPRESS, help="直接指定解释器")
        subparser.add_argument("--timeout", type=int, default=argparse.SUPPRESS, help="单个任务超时秒数")

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(line_buffering=True)  # 保证与子进程输出顺序一致
        except (AttributeError, ValueError):  # pragma: no cover
            pass

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        # 未给子命令时直接进入交互模式，最省事（保留全局选项）
        extra = list(argv) if argv is not None else sys.argv[1:]
        args = parser.parse_args(extra + ["interactive"])

    attacks = load_registry()

    dispatch = {
        "list": cmd_list,
        "search": cmd_search,
        "info": cmd_info,
        "run": cmd_run,
        "test": cmd_test,
        "interactive": cmd_interactive,
        "doctor": cmd_doctor,
        "docs": cmd_docs,
    }
    handler = dispatch.get(args.command)
    if handler is None:
        parser.print_help()
        return 2
    try:
        return handler(attacks, args)
    except KeyboardInterrupt:
        print("\n[cam] 已中断")
        return 130
    except (BrokenPipeError, OSError) as exc:
        # 下游管道被关闭（例如 `| head`）：安静退出，不打印回溯
        if isinstance(exc, OSError) and not isinstance(exc, BrokenPipeError) and exc.errno not in (22, 32, 232):
            raise
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except OSError:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
