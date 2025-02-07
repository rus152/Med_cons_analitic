from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime
import os
import json
from alive_progress import alive_bar

with open("res/5.txt", 'r', encoding='utf-8') as file:
    dialog = file.read()

with open("prompt.txt", 'r', encoding='utf-8') as file:
    prompt = file.read()

qz = {}

for i in range(3):
    with open(f"qz/{i}.txt", 'r', encoding='utf-8') as file:
        qz[i] = file.read()

model = ChatOpenAI(model="gpt-4o", temperature=0.000000000000000001)

result = {}

for i in range(6):
    with alive_bar(3, title='Обработка вопросов') as bar:
        for i in range(3):
            message = [
            SystemMessage(
            content=prompt + "\n" + dialog,
            sender="system",
            ),
            HumanMessage(content="Задавал ли врач эти вопросы?\n" + qz[i], sender="human"),
            ]
            result[i] = model.invoke(message)
            if (result[i].content == "Error. The text is not a dialogue."):
                print("Ошибка, удостоверьтесь, что текст является диалогом.\n")
                exit()
            elif (result[i].content == "Error. The dialog doesn't look right."):
                print("Ошибка, диалог не выглядит правильным.\n")
                exit()
            if i == 2:
                os.makedirs('results', exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_path = f'results/Промпт4-0--gpt-4o--response_{timestamp}.txt'
                # Запись данных в файл
                with open(file_path, 'w', encoding='utf-8') as file:
                    combined_content = "\n".join([result[j].content for j in range(3)])
                    file.write(combined_content)
                # Чтение данных из файла
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    count = 0
                    for line in lines:
                        if line.strip() == "true":
                            count += 1
                    print(f'Количество строк с "true": {count}')
            bar()