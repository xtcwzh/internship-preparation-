from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate

model = ChatTongyi(model="qwen3-max")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},生了一个{gender}性孩子,请为这个孩子起一个名字，并封装为json格式返回给我，key为name，value就是你起的名字，请严格按照此要求回复"
)

second_prompt = PromptTemplate.from_template("请解析{name}这个名字的含义")

json_output_parser = JsonOutputParser()
str_output_parser = StrOutputParser()

chain = first_prompt | model | json_output_parser | second_prompt | model | str_output_parser

res = chain.invoke({"lastname":"张","gender":"男"})

print(res)