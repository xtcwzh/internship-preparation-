from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms import Tongyi

model = Tongyi(model = "qwen-max")

example_template = PromptTemplate.from_template(
    "单词:{word},反义词:{antonym}"
)

example_datas = [
    {"word":"大","antonym":"小"},
    {"word":"快","antonym":"慢"},
    {"word":"长","antonym":"短"},
    {"word":"重","antonym":"轻"},
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = example_template,
    examples = example_datas,
    prefix = "告知我一个单词的反义词，以下是一些示例",
    suffix = "基于我之前的示例，告诉我{word}的反义词",
    input_variables = ["word"],
)

prompt_text = few_shot_prompt.invoke({"word":"高"})
print(prompt_text.to_string())

res = model.invoke(prompt_text)
print(res)