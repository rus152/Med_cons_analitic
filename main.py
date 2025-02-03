from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime
import os
import json
from alive_progress import alive_bar



with open("res/5.txt", 'r', encoding='utf-8') as file:
    txt_content = file.read()

with open("prompt.txt", 'r', encoding='utf-8') as file:
    prompt = file.read()

model_name = "o1"

# Создаем модель ChatOpenAI
model = ChatOpenAI(model=model_name)

message = [
    SystemMessage(
        content=prompt,
        sender="system",
    ),
    HumanMessage(content=txt_content, sender="human"),
]

range_value = 3

with alive_bar(range_value, title='Обработка вопросов') as bar:
    for i in range(range_value):
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
            with open(f'results/Промпт2-0--{model_name}--response_{timestamp}.json', 'w', encoding='utf-8') as file:
                file.write(result.content)


        data = json.loads(result.content)

        # Если JSON представляет список, работаем с первым элементом
        if isinstance(data, list) and data:
            item = data[0]

            # Вывод информации из "Completion_of_the_checklist"
            checklist = item.get("Completion_of_the_checklist", "Нет информации")
            print("Completion_of_the_checklist:", checklist)

            # Подсчёт количества ответов True (учитываем True, "true" и "True")
            true_count = 0

            # Проходим по списку вопросов
            for question in item.get("Questions", []):
                # Для каждого вопроса проходим по его результатам
                for result_item in question.get("Results", []):
                    # Получаем значение ключа "result"
                    res = result_item.get("result")

                    # Если значение - булево True
                    if res is True:
                        true_count += 1
                    # Если значение строковое и его значение "true" (без учёта регистра)
                    elif isinstance(res, str) and res.lower() == "true":
                        true_count += 1

            print("Количество ответов True:", true_count)
        else:
            print("Полученные данные не соответствуют ожидаемому формату.")

        #print(result.content)
        print(i+1)
        bar()




