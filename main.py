from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Задаем путь к Excel-файлу и загружаем его содержимое
excel_path = "Checklist.xlsx"
loader = UnstructuredExcelLoader(excel_path, mode="elements")  # или mode="single" для одного элемента
documents = loader.load()

with open("5.txt", 'r', encoding='utf-8') as file:
    txt_content = file.read()


# Объединяем текст из всех документов в один промпт
excel_text = "\n".join(doc.page_content for doc in documents)

# Создаем модель ChatOpenAI
model = ChatOpenAI(model="o3-mini")

message = [
    SystemMessage(
        content=f"У тебя есть Excel-файл с текстом. Вот его содержимое:\n\n{excel_text}\n\nТвоя задача оценить по данному чек листу насколько хорошо выполнена работа сотрудника больницы. Так же ты должен давать рекомендации врачу, что ему надо сделать что бы повысить свою оценку(Не трогать чек лист). Если есть какие то ошибки с субординации, при упоминание приводи цитату, где врач был неформален в общении. Формат ответа такой: \n\n Выполено критериев чеклиста:(Проценты выполеной работы)\n Допущенные ошибки:\n-(Перечисление ошибок через черту)\nРекомендации:\n-(Перечисление рекомендаций через черту)\n\Финальная оценка: (Оценка по 10-бальной шкале)\n\n",
        sender="system",
    ),
    HumanMessage(content=txt_content, sender="human"),
]
# Отправляем текст Excel-файла в модель
result = model.invoke(message)

print(result.content)
