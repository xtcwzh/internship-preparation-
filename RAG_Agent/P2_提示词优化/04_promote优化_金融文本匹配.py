from openai import OpenAI

client = OpenAI(
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

examples_data = {
    "是": [
        ("公司ABC发布了季度财报，显示盈利增长。", "财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。", "财报披露，公司ITCAST更赚钱了。"),
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。", "新能源技术的创新。"),
    ],
}

questions = [
    ("利率上升，影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。", "未来智能城市的建设趋势越加明显。"),
    ("股票市场今日大涨，投资者乐观。", "持续上涨的市场让投资者感到满意。"),
]

message = [
    {"role": "system", "content": "你是一个金融分析专家,根据用户给出的用[]分隔的两个句子判断两个句子是否属于同一事件,是则返回是,否则返回不是."},
]

for key,value in examples_data.items():
    for example in value:
        message.append({"role":"user","content":f"句子1:[{example[0]}],句子2:[{example[1]}]"})
        message.append({"role":"assistant","content":key})

for question in questions:
    response = client.chat.completions.create(
        model="qwen3-max",
        messages=message + [{"role":"user","content":f"句子1:[{question[0]}],句子2:[{question[1]}]"}],
    )
    print(response.choices[0].message.content)