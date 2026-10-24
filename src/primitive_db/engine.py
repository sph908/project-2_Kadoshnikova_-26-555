import prompt
import shlex
import prettytable
from primitive_db import constants, core, utils, parser


def welcome():
    """
    приветствие и основной цикл обработки команд
    """
    print("Первая попытка запустить проект!")
    print()
    print("***")
    while True:
        for command, description in constants.COMMANDS.items():
            print(f"<command> {command} - {description}")
        answer = prompt.string("Введите команду: ")
        print()
        if answer == "exit":
            break

def run():
    """
    Основая команды работы программы
    """
    while True:
        metadata = utils.load_metadata(constants.METADATA_PATH)
        user_input = input("Введите команду:")
        params = shlex.split(user_input, posix=False)
        if not params:
            continue
        if len(params) >= 2:
            pair = f"{params[0]} {params[1]}"
            if pair in constants.COMPOUND_COMMANDS:
                params = [pair, *params[2:]]
        func_name = params[0]
        # if func_name in constants.FUNCTION_NAMES.keys():
        match func_name:
            case 'create_table':
                table_name = params[1]
                validateTableName(table_name)
                columns = dict(param.split(":", 1) for param in params[2:])
                validateColumns(columns)
                if core.create_table(metadata, table_name, columns):
                    utils.save_metadata(constants.METADATA_PATH, metadata)
            case 'drop_table':
                table_name = params[1]
                core.drop_table(metadata, table_name)
                utils.save_metadata(constants.METADATA_PATH, metadata)
            case 'insert into':
                table_name = params[1]
                values = [parser.convert_value(v) for v in params[3:]]
                core.insert(metadata, table_name, values)
            case 'select from':
                table_name = params[1]
                table_data = utils.load_table_data(table_name)
                #проверка на существование таблицы для селекта
                if "where" in params:
                    where_index = params.index("where")
                    conditions = parser.parse_conditions(" ".join(params[where_index + 1:]))
                else:
                    conditions = {}
                rows = core.select(table_data, conditions)
                table = prettytable.PrettyTable()
                if rows:
                    table.field_names = rows[0].keys()
                    for row in rows:
                        table.add_row(row.values())
                print(table)
            case 'update':  
                table_name = params[1]
                table_data = utils.load_table_data(table_name)
                if "where" not in params:
                    print("Для update нужно условие where")
                    continue              
                where_index = params.index("where")
                conditions = parser.parse_conditions(" ".join(params[where_index+1:]))
                set_values = parser.parse_conditions(" ".join(params[3:where_index]))
                data_updated = core.update(table_data, set_values, conditions)
                utils.save_table_data(table_name, data_updated)
            case 'delete from':
                table_name = params[1]
                table_data = utils.load_table_data(table_name)
                if "where" not in params:
                    print("Для update нужно условие where")
                    continue
                where_index = params.index("where")
                conditions = parser.parse_conditions(" ".join(params[where_index+1:]))
                data_deleted = core.delete(table_data, conditions)
                utils.save_table_data(table_name, data_deleted)
            case _ if func_name not in constants.FUNCTIONS_NAMES.keys():
                print(f'Функции {func_name} нет. Попробуйте снова.')
            
def validateColumns(columns={}):
        # Проверить правильность заполнения столбцов
    return

def validateTableName(name=str):
        # Проверить правильность заполнения названия таблицы
    return
