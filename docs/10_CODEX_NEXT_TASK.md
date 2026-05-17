# docs/10_CODEX_NEXT_TASK.md

# M2：数据读取、字段校验与降采样管线

## 本轮目标

在 M1 最小工程骨架基础上，实现 BIDMC CSV 的读取、字段归一化校验、125Hz → 50Hz 降采样管线，并通过仓库内示例 CSV 完成 smoke test。

本轮只完成“数据进入算法前的稳定管线”，为 M3 的 R 峰检测与 RR 输出做准备。

## 本轮非目标

1. 不实现 R 峰检测。
2. 不计算 RR。
3. 不输出 HR。
4. 不输出 HRV。
5. 不实现完整 GUI。
6. 不输出医疗诊断结论。
7. 不做临床准确性评价。

## 允许修改的范围

1. `docs/10_CODEX_NEXT_TASK.md`
2. `src/ecg_rr_tool/`
3. `tests/`
4. `README.md`，仅限补充 M2 运行命令时可修改
5. `docs/09_CODEX_RUNBOOK.md`，仅限补充 M2 运行命令时可修改

## 不允许修改的范围

1. 不改变 `docs/04_IO_CONTRACT.md` 中已确认的最终输入/输出字段定义。
2. 不改变示例 CSV 路径：`data/examples/bidmc_01_Signals_2500.csv`。
3. 不删除或替换示例 CSV。
4. 不把 ChatGPT sources、聊天附件路径、本地绝对路径写入代码或测试。
5. 不改变技术栈。
6. 不新增医疗诊断相关功能。
7. 不抢做 M3 的 R 峰检测、RR 计算或最终逐采样点算法输出。

## 输入数据

仓库内示例 CSV 路径：

```text
data/examples/bidmc_01_Signals_2500.csv
```

关键字段：

1. 时间戳字段：`Time [s]`
2. ECG 字段：标准名 `II`，原始 CSV 可能为 ` II`
3. PPG 字段：标准名 `PLETH`，原始 CSV 可能为 ` PLETH`

字段匹配要求：

- 读取 CSV 后，必须对列名使用 `strip()` 归一化匹配。
- 不得依赖前导空格作为唯一匹配方式。
- 如果 `strip()` 后出现重复字段名，应报错，不要静默选择其中一个。
- 如果缺少必要字段，应抛出清晰错误。

## 建议实现

可按实际代码组织调整，但建议至少沉淀以下能力：

1. CSV 读取与字段标准化：
   - 输入：CSV path
   - 输出：只包含标准列的结构化数据，例如 `time_s`、`ecg_raw`、`ppg_raw`

2. 采样率校验：
   - 验证 `time_s` 单调递增；
   - 基于时间戳中位数间隔估计原始采样率；
   - 对示例 CSV 应识别为约 125Hz；
   - 若采样率明显不符，应报错或给出明确 warning。

3. 降采样：
   - ECG：125Hz → 50Hz；
   - PPG：125Hz → 50Hz；
   - 时间戳同步生成 50Hz 时间轴；
   - 推荐使用 `scipy.signal.resample_poly(..., up=2, down=5)` 处理 ECG/PPG；
   - 50Hz 时间戳建议从原始首个时间戳开始，以 0.02s 为步长生成，长度与降采样信号一致。

4. CLI smoke 入口：
   - 支持输入 CSV 路径；
   - 支持 `--output` 指定 M2 降采样结果 CSV；
   - 执行后输出简短摘要，例如输入行数、输出行数、估计采样率、输出文件路径。

## M2 中间输出 CSV

M2 可生成“降采样中间文件”，用于验证数据管线。该文件不是 M3 后的最终 RR 分析结果。

建议 M2 中间输出字段：

| 字段 | 含义 |
|---|---|
| `sample_index_50hz` | 50Hz 采样点索引 |
| `time_s` | 50Hz 时间戳，单位秒 |
| `ecg_50hz` | 降采样后的 ECG |
| `ppg_50hz` | 降采样后的 PPG |

注意：

- M2 不应伪造 `r_peak` 或 `rr_ms`。
- `r_peak` 和 `rr_ms` 在 M3 实现。
- 不得把 M2 中间文件描述为医疗或最终诊断结果。

## 测试命令

至少执行：

```bash
python -m pytest
python -m ecg_rr_tool.cli --help
python -m ecg_rr_tool.gui --help
python -m ecg_rr_tool.cli data/examples/bidmc_01_Signals_2500.csv --output /tmp/ecg_rr_m2_resampled.csv
```

如果本地环境要求 `PYTHONPATH=src`，可使用：

```bash
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m ecg_rr_tool.cli --help
PYTHONPATH=src python -m ecg_rr_tool.gui --help
PYTHONPATH=src python -m ecg_rr_tool.cli data/examples/bidmc_01_Signals_2500.csv --output /tmp/ecg_rr_m2_resampled.csv
```

## 通过标准

1. `python -m pytest` 通过。
2. CLI 和 GUI 的 `--help` 均可运行。
3. 示例 CSV 可被读取。
4. 必要字段经 `strip()` 后可正确匹配：`Time [s]`、`II`、`PLETH`。
5. 对示例 CSV 能识别原始采样率约为 125Hz。
6. 降采样输出约为 50Hz，时间戳单调递增，相邻间隔约 0.02s。
7. 示例 CSV 2500 行输入应输出约 1000 行 50Hz 数据。
8. M2 中间输出 CSV 字段完整：`sample_index_50hz`、`time_s`、`ecg_50hz`、`ppg_50hz`。
9. 未实现 R 峰检测、RR、HR、HRV 或医疗诊断功能。
10. 未改变 Project Brief v0.1 和 IO Contract v0.1 已确认的需求。

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
