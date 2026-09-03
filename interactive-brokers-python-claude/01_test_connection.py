"""
第一步：只测试 Python 能否连上 TWS / IB Gateway 的模拟账户。

运行前请确认：
1. TWS 或 IB Gateway 已经登录到 Paper Trading（模拟账户）
2. 在 TWS/Gateway 里：File -> Global Configuration -> API -> Settings
   - 勾选 "Enable ActiveX and Socket Clients"
   - 记下 "Socket port"（TWS 默认 7497，Gateway 默认 4002）
   - "Trusted IP Addresses" 里加上 127.0.0.1（本机连接一般不需要，但加了更保险）
   - 建议先不要额外勾选 "Read-Only API"（否则以后没法下单，但查数据阶段勾上更安全）
"""

from ib_async import IB

from config import IB_HOST, IB_PORT, IB_CLIENT_ID


def main() -> None:
    ib = IB()
    print(f"正在连接 {IB_HOST}:{IB_PORT} (clientId={IB_CLIENT_ID}) ...")
    ib.connect(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID, timeout=10)

    print("连接成功！")
    print("服务器时间:", ib.reqCurrentTime())

    account = ib.managedAccounts()
    print("模拟账户列表:", account)

    summary = ib.accountSummary()
    print("\n账户摘要（前几项）:")
    for item in summary[:10]:
        print(f"  {item.tag:<20} {item.value:<15} {item.currency}")

    ib.disconnect()
    print("\n已断开连接。测试通过。")


if __name__ == "__main__":
    main()
