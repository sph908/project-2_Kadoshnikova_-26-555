import prompt
import shlex
import prettytable
from primitive_db import constants, core, utils, parser, decorators


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

cacher = core.create_cacher()

@decorators.handle_db_errors
def commands(metadata, params):
    func_name = params[0]
    global cacher
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
            if core.drop_table(metadata, table_name)  is not None:
                 utils.save_metadata(constants.METADATA_PATH, metadata)
        
        case 'insert into':
            table_name = params[1]
            values = [parser.convert_value(v) for v in params[3:]]
            core.insert(metadata, table_name, values)
            cacher = core.create_cacher()
        
        case 'select from':
            table_name = params[1]
            if table_name not in metadata:
                raise KeyError(table_name)
            table_data = utils.load_table_data(table_name)
            conditions = parser.parse_where(params)
            key = (table_name, tuple(sorted(conditions.items())) if conditions else None)
            rows = cacher(key, lambda: core.select(table_data, conditions))           
            table = prettytable.PrettyTable()
            if rows:
                table.field_names = rows[0].keys()
                for row in rows:
                    table.add_row(row.values())
            print(table)
            
        case 'update':  
            table_name = params[1]
            if table_name not in metadata:
                raise KeyError(table_name)
            set_values = parser.parse_set(params)
            conditions = parser.parse_where(params)
            if set_values is None:
                print('Для update нужна часть set, по типу: set column_name = value')
                return
            if conditions is None:
                print('Для update нужно условие where')
                return
            table_data = utils.load_table_data(table_name)
            data_updated = core.update(table_data, set_values, conditions)
            if data_updated is not None:
                cacher = core.create_cacher()
                utils.save_table_data(table_name, data_updated)
            
        case 'delete from':
            table_name = params[1]
            if table_name not in metadata:
                raise KeyError(table_name)
            conditions = parser.parse_where(params)
            if conditions is None:
                print('Для delete нужно условие where')
                return
            table_data = utils.load_table_data(table_name)
            data_deleted = core.delete(table_data, conditions)
            if data_deleted is not None:
                cacher = core.create_cacher()
                utils.save_table_data(table_name, data_deleted)
        case _ if func_name not in constants.FUNCTIONS_NAMES.keys():
            print(f'Функции {func_name} нет. Попробуйте снова.')



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
        commands(metadata, params)


def validateColumns(columns={}):
        # Проверить правильность заполнения столбцов
    return

def validateTableName(name=str):
        # Проверить правильность заполнения названия таблицы
    return
