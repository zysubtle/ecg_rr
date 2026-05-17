# Codex Runbook v0.1

## 环境建议

- Python 3.10+
- macOS
- 建议使用虚拟环境

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

如果环境不支持 extras，可使用：

```bash
python -m pip install -e .
python -m pip install pytest
```

## 当前 M1 测试命令

```bash
python -m pytest
python -m ecg_rr_tool.cli --help
python -m ecg_rr_tool.gui --help
```

## 示例数据路径

```text
data/examples/bidmc_01_Signals_2500.csv
```

## 重要限制

1. 不要使用 ChatGPT 附件路径。
2. 不要使用本地绝对路径。
3. 不要假设 Codex 能访问对话里的 sources。
4. 所有测试必须使用仓库内相对路径。
