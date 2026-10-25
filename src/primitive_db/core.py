from primitive_db import constants, decorators, utils


@decorators.handle_db_errors
def create_table(metadata, table_name, columns):
    """
    Функция для создания таблицы
    """
    if table_name in metadata:
        raise ValueError(f'Таблица {table_name} уже существует')
    contains_key = False
    if not table_name.isidentifier():
        raise ValueError(
        f"Недопустимое имя таблицы: {table_name}. "
        f"Имя должно начинаться c буквы или подчёркивания")
    if not columns:
        raise ValueError("Нужно указать хотя бы один столбец, например name:str")
    for key in columns.keys():
        if key.lower() == 'id':
            contains_key = True
            break
    if not contains_key:
        columns = {'ID' : 'int', **columns}
        
    for name,value in columns.items():
        if value not in constants.TYPES:
            raise ValueError(
            f"Некорректный тип данных, "
            f"допустимые: {', '.join(constants.TYPES)}")
        if not name.isidentifier():
            raise ValueError(
            f"Недопустимое имя столбца: {name}. "
            f"Имя должно начинаться c буквы или подчёркивания"
        )
    metadata.update({table_name: columns})
    return metadata

@decorators.handle_db_errors
@decorators.confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """
    Функция для удаления таблицы
    """
    if table_name not in metadata:
        raise KeyError(table_name)
    del metadata[table_name]
    return metadata

def validate_table(metadata, table_name, values):
        """
        Функция для проверки ошибок при записи данных в таблицу
        """
        errors = []
        column_types = list(metadata.get(table_name).values())
        if len(values) != len(column_types)-1:
            errors.append(f'''Кол-во переданных столбцов 
не соответсвует изначальному в {table_name}''')
        else:
            for i in range(1, len(column_types)):
                expected_type = constants.TYPES.get(column_types[i])
                inserted_value = values[i-1]
                if type(inserted_value) is not expected_type:
                    errors.append(f'''Несоответсвующий тип данных: 
{inserted_value} должно быть {column_types[i]}''')
        return errors

@decorators.handle_db_errors
@decorators.log_time
def insert(metadata, table_name, values):
    """
    Функция для добавления записей в таблицу
    """
    if table_name not in metadata:
       raise KeyError(table_name)
    errors = validate_table(metadata, table_name, values)
    if errors:
        raise ValueError("; ".join(errors))
    column_names = list(metadata.get(table_name).keys())
    data = utils.load_table_data(table_name)
    new_row = {"ID" : max((row["ID"] for row in data), default=0) + 1}
    for i in range(1, len(column_names)):
        new_row.update({column_names[i] : values[i-1]})
    data.append(new_row)
    utils.save_table_data(table_name, data)
    return data


def is_matching_row(row, where_clause):
    """
    Функция проверяет соответсвие заданным условиям
    """
    for column, value in where_clause.items():
        if row.get(column) != value:
            return False
    return True


@decorators.log_time
def select(table_data, where_clause=None):
    """
    Функция для просмотра записей таблицы
    """
    if not where_clause:
        return table_data
    else: 
        filtered_data = []
        for row in table_data:
            if is_matching_row(row, where_clause):
                filtered_data.append(row)
        return filtered_data

@decorators.confirm_action("изменение записей таблицы")
def update(table_data, set_clause, where_clause):
    """
    Функция для изменения записей таблицы
    """
    for row in table_data:
        if is_matching_row(row, where_clause):
            row.update(set_clause)
    return table_data

@decorators.confirm_action("удаление записей таблицы")
def delete(table_data, where_clause):
    """
    Функция для удаления записей из таблицы
    """
    kept_rows = []
    for row in table_data:
        if not is_matching_row(row, where_clause):
            kept_rows.append(row)
    return kept_rows


def print_help():
    """
    Функция для вывода справочной информации
    """
    rows = []
    rows_2 =[]
    for command, description in constants.FUNCTIONS_NAMES.items():
        rows.append(f"  {command} - {description}")
        rows.append(f"      {constants.COMMAND_USAGE[command]}")
    for command, description in constants.COMMANDS.items():
        rows_2.append(f"{command} - {description}")
    print(
        f'''***Процесс работы с таблицей***
Команды:
{"\n".join(rows)}
Допустимые типы столбцов:
{', '.join(constants.TYPES)}
Общие команды:
{"\n".join(rows_2)}''')
    return


def list_tables(metadata):
    """
    Возвращает список таблиц с перечнем их столбцов
    """
    return [
        {"таблица": table_name, "столбцы": ", ".join(columns)}
        for table_name, columns in metadata.items()
    ]



                






















