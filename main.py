from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime
import os


with open("res/5.txt", 'r', encoding='utf-8') as file:
    txt_content = file.read()

with open("prompt.txt", 'r', encoding='utf-8') as file:
    prompt = file.read()

# Создаем модель ChatOpenAI
model = ChatOpenAI(model="o3-mini")

message = [
    SystemMessage(
        content=prompt,
        sender="system",
    ),
    HumanMessage(content=txt_content, sender="human"),
]
# Отправляем текст Excel-файла в модель
result = model.invoke(message)

if (result.content == "Error. The text is not a dialogue."):
    print("Ошибка, удостоверьтесь, что текст является диалогом.\n")
    exit()
elif (result.content == "Error. The dialog doesn't look right."):
    print("Ошибка, диалог не выглядит правильным.\n")
    exit()
else:
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'results/response_{timestamp}.json', 'w', encoding='utf-8') as file:
        file.write(result.content)

print(result.content)

