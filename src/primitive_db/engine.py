import prompt
import shlex
from primitive_db import constants, core, utils


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
    while True:
        metadata = utils.load_metadata(constants.METADATA_PATH)
        func_input = input("Введите команду:")
        params = shlex.split(func_input, posix=False);
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
            case _ if func_name not in constants.FUNCTIONS_NAMES.keys():
                print(f'Функции {func_name} нет. Попробуйте снова.')
            
def validateColumns(columns={}):
        # Проверить правильность заполнения столбцов
    return

def validateTableName(name=str):
        # Проверить правильность заполнения названия таблицы
    return
