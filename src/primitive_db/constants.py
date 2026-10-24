from pathlib import Path
COMMANDS = {
    "exit": "выйти из программы",
    "help": "справочная информация"
}

BASE_DIR = Path(__file__).parent

METADATA_PATH = BASE_DIR / "db_meta.json"
TABLE_PATH = BASE_DIR / "data"


FUNCTIONS_NAMES = {
    "create_table": "создать таблицу",
    "drop_table": "удалить таблицу",
    "insert into": "добавить запись",
    "select from": "выбрать записи",
    "update": "изменить записи",
    "delete from": "удалить записи",
}

COMPOUND_COMMANDS = ("insert into", "delete from", "select from")

TYPES = {
    "int": int,
    "str": str,
    "bool": bool,
}

SEPARATORS = ("and", ",")