import json


def load_metadata(filepath):
    """
    Загрузка данных из JSON-файла
    """
    try:
        with open(filepath,'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_metadata(filepath, data):
    """
    Сохранение данных в JSON-файл
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data,f)



