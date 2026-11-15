# 贡献者 / Contributors

本项目遵循「提交即署名」：通过 Pull Request 或 Issue 为本项目做出贡献的人都会列在这里。

> 说明：GitHub 仓库右侧和 Insights → Contributors 里的图表由提交历史**自动生成**，无法手工编辑；
> 本文件是一份可人工维护、更详细的名单，用于明确记录每个人的具体贡献。

## 维护者 / Maintainer

| 贡献者 | 角色 | 贡献 |
| --- | --- | --- |
| [@J1ann](https://github.com/J1ann) | 作者 / Maintainer | 统一调度器（`crypto_attack_machine.py`）、攻击整合、文档与测试框架、许可证整理 |

## 贡献者 / Contributors

| 贡献者 | PR | 贡献内容 |
| --- | --- | --- |
| [@XinyiYu-XJTU](https://github.com/XinyiYu-XJTU) | [#1](https://github.com/J1ann/Crypto_attack_mechine/pull/1) | 修订并澄清 README 的安装说明，明确 PyCryptodome 的用途与安装方式（`README.md` +16 / −6） |
| [@Duanzhoutao](https://github.com/Duanzhoutao) | [#2](https://github.com/J1ann/Crypto_attack_mechine/pull/2) | 为 `PartialInteger` 补充单元测试，并修复 `parse_be` 的自递归问题（`test/shared/test_partial_integer.py` +163，`shared/partial_integer.py` ±1） |

## 如何成为贡献者

1. Fork 本仓库，从 `main` 切出功能分支；
2. 提交 Pull Request，说明改动目的与验证方式（攻击相关请附可复现的最小样例）；
3. PR 合并后，名字会被加入上面的名单，同时自动计入 GitHub 的 Contributors 图表。

发现 bug、有新的攻击思路或文档改进建议，也欢迎直接开 Issue。
