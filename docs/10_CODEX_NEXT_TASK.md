# docs/10_CODEX_NEXT_TASK.md

# M1：项目启动包与最小工程骨架

## 本轮目标

建立桌面端 ECG 分析项目的启动包和最小 Python 工程骨架，确保文档、示例数据路径、协作规则和基础测试都已入仓库。

## 本轮非目标

1. 不实现完整降采样算法。
2. 不实现完整 R 峰检测算法。
3. 不实现完整 GUI。
4. 不输出 HR。
5. 不输出 HRV。
6. 不输出医疗诊断结论。
7. 不做临床准确性评价。

## 允许修改的范围

1. `README.md`
2. `AGENTS.md`
3. `docs/`
4. `data/examples/`
5. `pyproject.toml`
6. `src/ecg_rr_tool/`
7. `tests/`

## 不允许修改的范围

1. 不新增与当前里程碑无关的大型算法模块。
2. 不新增医疗诊断相关功能。
3. 不改变已确认的输入输出字段。
4. 不改变示例 CSV 路径。
5. 不把 ChatGPT sources、附件路径或本地绝对路径写进代码或测试。

## 必须包含的文件

1. `docs/00_PROJECT_BRIEF.md`
2. `docs/01_DECISION_LOG.md`
3. `docs/02_MILESTONE_PLAN.md`
4. `docs/03_ALGORITHM_SCOPE.md`
5. `docs/04_IO_CONTRACT.md`
6. `AGENTS.md`
7. `docs/09_CODEX_RUNBOOK.md`
8. `docs/10_CODEX_NEXT_TASK.md`
9. `data/examples/bidmc_01_Signals_2500.csv`
10. `pyproject.toml`
11. `src/ecg_rr_tool/__init__.py`
12. `src/ecg_rr_tool/cli.py`
13. `src/ecg_rr_tool/gui.py`
14. `tests/test_project_layout.py`

## 示例 CSV

仓库内相对路径：

```text
data/examples/bidmc_01_Signals_2500.csv
```

关键字段：

1. 时间戳字段：`Time [s]`
2. ECG 字段：`II`，原始 CSV 可能为 ` II`
3. PPG 字段：`PLETH`，原始 CSV 可能为 ` PLETH`

字段匹配要求：

- 读取 CSV 后，对列名使用 `strip()` 归一化匹配。
- 不得依赖前导空格作为唯一匹配方式。

## 当前 M1 测试命令

```bash
python -m pytest
python -m ecg_rr_tool.cli --help
python -m ecg_rr_tool.gui --help
```

## 通过标准

1. 上述必需文件存在。
2. 示例 CSV 位于 `data/examples/bidmc_01_Signals_2500.csv`。
3. 测试能确认示例 CSV 可读取，且 `strip()` 后包含 `Time [s]`、`II`、`PLETH`。
4. `python -m pytest` 通过。
5. `python -m ecg_rr_tool.cli --help` 可运行。
6. `python -m ecg_rr_tool.gui --help` 可运行。
7. 未实现完整算法、完整 GUI 或医疗诊断功能。
8. 未改变 Project Brief v0.1 已确认的需求。

## 失败时应报告的信息

1. 失败命令；
2. 完整错误信息；
3. 失败文件；
4. 是否涉及 S0 决策；
5. 建议下一步修复范围。

## Codex 输出摘要格式

请在执行后提供：

```text
Summary
Changed files
Test commands
Test results
Known limitations
未完成事项
```
