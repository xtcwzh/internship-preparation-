from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Tongyi

model = Tongyi(model="qwen-max")

prompt_template = PromptTemplate.from_template(
    "我的领居最近买了一辆新车{car}，你能告诉我这辆车的性能如何吗？"
)

# res = model.invoke(prompt_template.format(car="宝马3系"))
# print(res)

chain = prompt_template | model

res = chain.invoke(input={"car":"奔驰c63"})
print(res)