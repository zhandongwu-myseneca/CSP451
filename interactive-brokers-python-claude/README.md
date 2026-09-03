# Interactive Brokers + Python + Claude 打通指南

把 IB 模拟账户、Python 和 Claude 连起来，分三层，每一层单独测试，出问题时容易定位：

```
TWS / IB Gateway (模拟账户)  <--socket-->  Python (ib_async)  --数据-->  Claude API
```

## 第 0 步：确认 IB 端的"全局配置"

打开 TWS（或 IB Gateway），登录 **Paper Trading（模拟）** 账户，然后：

`File -> Global Configuration -> API -> Settings`

逐项对照：

| 配置项 | 应该是 |
|---|---|
| Enable ActiveX and Socket Clients | ✅ 勾选 |
| Socket port | TWS 模拟盘默认 **7497**；IB Gateway 模拟盘默认 **4002** |
| Read-Only API | 先勾选（只查数据更安全），需要下单时再取消 |
| Trusted IP Addresses | 加入 `127.0.0.1` |
| Allow connections from localhost only | 本机测试时可以勾选 |

⚠️ 注意：**TWS/Gateway 必须一直保持登录并在前台运行**，Python 才能连上——它不是后台服务，是要连接一个正在运行的桌面程序的 socket 端口。

## 第 1 步：Python 环境

```bash
cd interactive-brokers-python-claude
python -m venv venv
source venv/bin/activate      # Windows 用 venv\Scripts\activate
pip install -r requirements.txt
```

## 第 2 步：配置密钥

```bash
cp .env.example .env
```

编辑 `.env`，填入：
- `IB_PORT`：和上面第 0 步里 TWS/Gateway 实际显示的端口一致
- `ANTHROPIC_API_KEY`：从 https://console.anthropic.com/ 生成

`.env` 已经在 `.gitignore` 里，不会被提交到 git。

## 第 3 步：测试 IB 连接

先保证 TWS/Gateway 开着、已登录模拟账户，然后：

```bash
python 01_test_connection.py
```

看到账户摘要打印出来，说明 Python <-> IB 这条链路通了。

常见报错：
- `TimeoutError` / 连不上 → 检查端口号、"Enable ActiveX and Socket Clients" 有没有勾、TWS 是不是真的在前台登录着
- `clientId 已被占用` → 换一个 `IB_CLIENT_ID`（比如从 1 改成 2）
- 弹出一个"是否允许连接"的确认框 → 在 TWS 里点允许，或者把 IP 加入 Trusted IP Addresses 后就不会再弹

## 第 4 步：拉取行情数据

```bash
python 02_fetch_market_data.py
```

会生成 `market_data.csv`（某支股票最近 30 天日K线），并打印当前模拟账户持仓。

## 第 5 步：交给 Claude 分析

```bash
python 03_claude_analysis.py
```

这一步会把 `market_data.csv` 里最近的数据发给 Claude API，返回一段中文的走势摘要。

## 之后可以怎么扩展

- 把 `03_claude_analysis.py` 的输出结果，作为下单逻辑的输入（比如让 Claude 生成信号，Python 再用 `ib.placeOrder(...)` 在**模拟账户**下单验证）
- 用 `ib.reqMktData` 换成实时行情（需要 TWS 有对应的行情权限）
- 把整个流程包装成一个定时任务（cron / 后台脚本），定期跑一次分析并把结果发到 Slack/邮件

## 安全提醒

- 全程使用 **Paper Trading（模拟账户）**，不要在没充分测试前连实盘
- `ANTHROPIC_API_KEY` 和 IB 账户信息都不要硬编码进代码或提交到 git
- Claude 生成的内容仅做参考/教学用途，不构成投资建议
