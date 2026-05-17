# ECG RR Tool

桌面端 ECG 分析算法项目，用于读取 BIDMC CSV，对 ECG / PPG 从 125Hz 降采样到 50Hz，在 50Hz ECG 上检测 R 峰并输出 RR。

> 当前仓库处于 M1：项目启动包与最小工程骨架阶段。完整降采样、R 峰检测、RR 输出和 GUI 功能将在后续里程碑实现。

## 项目定位

本项目是研究 / 工程分析工具，不作为医疗诊断软件。

## 示例数据

```text
data/examples/bidmc_01_Signals_2500.csv
```

输入字段采用 `strip()` 归一化匹配：

- `Time [s]`
- `II`，兼容原始列名 ` II`
- `PLETH`，兼容原始列名 ` PLETH`

## 安装

```bash
python -m pip install -e ".[dev]"
```

## M1 测试

```bash
python -m pytest
python -m ecg_rr_tool.cli --help
python -m ecg_rr_tool.gui --help
```

## 后续里程碑

- M2：数据读取、字段校验与降采样管线
- M3：R 峰检测与 RR 输出
- M4：CLI 完整化与 smoke test
- M5：GUI 最小可用版本
- M6：审查、风险收敛与文档固化
