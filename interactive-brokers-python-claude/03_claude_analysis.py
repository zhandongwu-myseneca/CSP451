"""
第三步：把上一步拉到的市场数据丢给 Claude，让它做一个简单的文字分析。
（示例用途：教学/研究性质的摘要生成，不构成投资建议，也不会自动下单。）
"""

import pandas as pd
from anthropic import Anthropic

from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


def main() -> None:
    df = pd.read_csv("market_data.csv")
    recent = df.tail(10).to_string(index=False)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": (
                    "下面是某支股票最近的日K线数据（来自 Interactive Brokers 模拟账户）：\n\n"
                    f"{recent}\n\n"
                    "请用中文简要总结一下近期的价格走势和成交量变化，"
                    "只做客观描述，不要给出买卖建议。"
                ),
            }
        ],
    )

    print("Claude 的分析：\n")
    print(message.content[0].text)


if __name__ == "__main__":
    main()
