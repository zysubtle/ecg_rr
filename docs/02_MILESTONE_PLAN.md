# Milestone Plan v0.1

## M0：项目启动问诊与 Project Brief

目的：确认项目边界、输入输出、技术栈、测试方式。

状态：已完成。

## M1：项目启动包与最小工程骨架

目的：沉淀项目文档、协作规则、IO contract、Codex runbook、当前任务文件，并建立最小 Python 工程骨架。

产出：

1. `docs/00_PROJECT_BRIEF.md`
2. `docs/01_DECISION_LOG.md`
3. `docs/02_MILESTONE_PLAN.md`
4. `docs/03_ALGORITHM_SCOPE.md`
5. `docs/04_IO_CONTRACT.md`
6. `AGENTS.md`
7. `docs/09_CODEX_RUNBOOK.md`
8. `docs/10_CODEX_NEXT_TASK.md`
9. `data/examples/bidmc_01_Signals_2500.csv`
10. 最小 Python 包骨架与 layout 测试

不做：

1. 不实现完整降采样算法；
2. 不实现完整 R 峰检测；
3. 不实现完整 GUI；
4. 不做 HR / HRV；
5. 不做临床准确性评价。

## M2：数据读取、字段校验与降采样管线

目的：读取 CSV，完成字段归一化、采样率校验、125Hz 到 50Hz 降采样，输出降采样后的 ECG / PPG / timestamp。

## M3：R 峰检测与 RR 输出

目的：在 50Hz ECG 上检测 R 峰，计算 RR，并导出逐采样点 CSV。

## M4：CLI 完整化与 smoke test

目的：完善命令行入口、错误处理、测试命令、基于示例 CSV 的回归测试。

## M5：GUI 最小可用版本

目的：实现选择文件、运行分析、波形显示、R 峰标注、结果表格、导出 CSV。

## M6：审查、风险收敛与文档固化

目的：整理 README、使用说明、测试说明、已知限制和后续计划。
