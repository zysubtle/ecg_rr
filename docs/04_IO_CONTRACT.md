# IO Contract v0.1

## 输入 CSV

### 示例路径

```text
data/examples/bidmc_01_Signals_2500.csv
```

### 采样率

```text
125Hz
```

### 字段匹配策略

读取 CSV 后，对列名做 `strip()` 归一化，再进行字段匹配。

| 标准字段 | 允许原始字段示例 | 含义 |
|---|---|---|
| `Time [s]` | `Time [s]` | 时间戳，单位秒 |
| `II` | ` II`, `II` | ECG 导联 II |
| `PLETH` | ` PLETH`, `PLETH` | PPG 信号 |

## 输出 CSV

### 输出结构

逐采样点输出，每行对应一个 50Hz 采样点。

### 输出字段

| 字段 | 类型建议 | 含义 |
|---|---|---|
| `sample_index_50hz` | int | 50Hz 下的采样点索引 |
| `time_s` | float | 降采样后的时间戳，单位秒 |
| `ecg_50hz` | float | 降采样后的 ECG 信号 |
| `ppg_50hz` | float | 降采样后的 PPG 信号 |
| `r_peak` | int | 是否为 R 峰，0 / 1 |
| `rr_ms` | float or empty | 当前 R 峰对应 RR，单位 ms；非 R 峰行为空值 |

## 输出约束

1. 不输出 HR。
2. 不输出 HRV。
3. 不输出医疗诊断结论。
4. R 峰检测基于 50Hz ECG。
5. RR 基于 50Hz R 峰时间戳计算。
