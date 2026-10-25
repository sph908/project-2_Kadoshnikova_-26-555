import shlex

import prettytable
import prompt

from primitive_db import constants, core, decorators, parser, utils


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

cacher = decorators.create_cacher()


def check_table_exists(metadata, table_name):
    """
    Проверяет, что таблица существует
    """
    if table_name not in metadata:
        raise KeyError(table_name)

@decorators.handle_db_errors
def commands(metadata, params):
    """
    Функция работы всех комманд
    """
    func_name = params[0]
    global cacher
    
    if func_name in constants.TABLE_REQUIRED and len(params) < 2:
        print(f'Для команды "{func_name}" нужно указать таблицу.')
        print(f'Формат: {constants.COMMAND_USAGE[func_name]}')
        return
    
    match func_name:

        case 'help':
            core.print_help()

        case 'create_table':
            table_name = params[1]
            columns = dict(param.split(":", 1) for param in params[2:])
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
            cacher = decorators.create_cacher()
        
        case 'select from':
            table_name = params[1]
            check_table_exists(metadata, table_name)
            table_data = utils.load_table_data(table_name)
            conditions = parser.parse_where(params)
            key = (table_name, tuple(sorted(conditions.items())) 
                   if conditions else None)
            rows = cacher(key, lambda: core.select(table_data, conditions))           
            table = prettytable.PrettyTable()
            if not rows:
                print("Записи не найдены")
                return
            if rows:
                table.field_names = rows[0].keys()
                for row in rows:
                    table.add_row(row.values())
            print(table)
            
        case 'update':  
            table_name = params[1]
            check_table_exists(metadata, table_name)
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
                cacher = decorators.create_cacher()
                utils.save_table_data(table_name, data_updated)
            
        case 'delete from':
            table_name = params[1]
            check_table_exists(metadata, table_name)
            conditions = parser.parse_where(params)
            if conditions is None:
                print('Для delete нужно условие where')
                return
            table_data = utils.load_table_data(table_name)
            data_deleted = core.delete(table_data, conditions)
            if data_deleted is not None:
                cacher = decorators.create_cacher()
                utils.save_table_data(table_name, data_deleted)
        case 'list_tables':
            tables = core.list_tables(metadata)
            if not tables:
                print("В базе данных нет таблиц")
                return
            table = prettytable.PrettyTable()
            table.field_names = tables[0].keys()
            for row in tables:
                table.add_row(row.values())
            print(table)
        case _ if func_name not in constants.FUNCTIONS_NAMES.keys():
            print(f'Функции {func_name} нет. Попробуйте снова:')



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
        if params[0] == 'exit':
            print('До свидания!')
            break
        commands(metadata, params)

