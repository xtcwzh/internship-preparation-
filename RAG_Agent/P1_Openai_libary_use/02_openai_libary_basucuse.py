from openai import OpenAI

client = OpenAI(
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

repose = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "你是一个霸道总裁，请根据用户的问题给出回答。"},
        {"role": "user", "content": "你是谁"}
    ],
    stream=True
)

# print(repose.choices[0].message.content)

for chunk in repose:
    print(chunk.choices[0].delta.content, end="", flush=True)