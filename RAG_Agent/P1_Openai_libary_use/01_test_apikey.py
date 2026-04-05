import base64
import os 
from openai import OpenAI

client = OpenAI(
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = [{"role": "system", "content": "你是一个智能助手，请根据用户的问题给出回答。"}, {"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="qwen3-max",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    # 开启深度思考时取消注释：与下方「思考过程 + 完整回复」分支配合使用
    # extra_body={"enable_thinking": True},
    stream=True
)
# ---------- 以下为「深度思考模型」流式输出写法（与当前运行的简单写法二选一）----------
# 区别简述：
# - 注释块：先流式打印模型内部推理（reasoning_content），再打印对用户可见的正文（content），
#   并加分隔标题；需配合 enable_thinking 且模型支持该字段。
# - 下方运行代码：只拼接打印 content，不区分推理与正文；若某 chunk 的 content 为 None 可能报错。
# is_answering = False  # False=仍在输出思考；True=已进入最终回复阶段，用于只打印一次「完整回复」标题
# print("\n" + "=" * 20 + "思考过程" + "=" * 20)
# for chunk in completion:
#     delta = chunk.choices[0].delta
#     # 部分模型在思考阶段会把中间推理放在 reasoning_content（与最终 content 分离）
#     if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
#         if not is_answering:
#             print(delta.reasoning_content, end="", flush=True)
#     # 进入最终答案：首次出现 content 时打印分隔线并把状态切到「正在回答」
#     if hasattr(delta, "content") and delta.content:
#         if not is_answering:
#             print("\n" + "=" * 20 + "完整回复" + "=" * 20)
#             is_answering = True
#         print(delta.content, end="", flush=True)

for chunk in completion:
    print(chunk.choices[0].delta.content, end="", flush=True)