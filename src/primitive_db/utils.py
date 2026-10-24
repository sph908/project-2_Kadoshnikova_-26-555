import json
from pathlib import Path
from primitive_db import constants

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
        json.dump(data,f, ensure_ascii=False, indent=4)

def get_table_path(table_name):
    return Path(constants.TABLE_PATH) / f"{table_name}.json"

def load_table_data(table_name):
    """
    Загрузка данных таблицы из JSON-файла
    """
    filepath = get_table_path(table_name)
    try:
        with open(filepath,'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_table_data(table_name, data):
    """
    Сохранение данных таблицы в отдельный JSON-файл
    """
    Path(constants.TABLE_PATH).mkdir(exist_ok=True)
    filepath = get_table_path(table_name)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data,f, ensure_ascii=False, indent=4)
        