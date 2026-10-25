from pathlib import Path

COMMANDS = {
    "exit": "выйти из программы",
    "help": "справочная информация"
}

METADATA_PATH = Path("db_meta.json")
TABLE_PATH = Path("data")


FUNCTIONS_NAMES = {
    "create_table": "создать таблицу",
    "drop_table": "удалить таблицу",
    "insert into": "добавить запись",
    "select from": "выбрать записи",
    "update": "изменить записи",
    "delete from": "удалить записи",
    "list_tables": "показать список таблиц"
}
COMMAND_USAGE = {
    "create_table": "create_table <таблица> <столбец>:<тип> ...",
    "drop_table": "drop_table <таблица>",
    "insert into": "insert into <таблица> values <значение> ...",
    "select from": "select from <таблица> [where <столбец> = <значение>]",
    "update": "update <таблица> set <столбец>=<значение> where <столбец>=<значение>",
    "delete from": "delete from <таблица> where <столбец> = <значение>",
    "list_tables": "list_tables"
}


TABLE_REQUIRED = (
    "create_table", "drop_table", "insert into",
    "select from", "update", "delete from",
)

COMPOUND_COMMANDS = ("insert into", "delete from", "select from")

TYPES = {
    "int": int,
    "str": str,
    "bool": bool
}

SEPARATORS = ("and", ",")