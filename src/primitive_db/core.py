from primitive_db import constants, utils, decorators


@decorators.handle_db_errors
def create_table(metadata, table_name, columns):
    """
    Функция для создания таблицы
    """
    if table_name in metadata:
        raise ValueError(f'Таблица {table_name} уже существует')
    contains_key = False
    for key in columns.keys():
        if key.lower() == 'id':
            contains_key = True
            break
        if contains_key == False:
            columns = {'ID' : 'int', **columns}
        
        for value in columns.values():
            if value not in constants.TYPES:
                raise ValueError(
                    f"Некорректный тип данных, "
                    f"допустимые: {', '.join(constants.TYPES)}")
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
            errors.append(f'Количество переданных столбцов не соответсвует количеству столбцов в {table_name}')
        else:
            for i in range(1, len(column_types)):
                expected_type = constants.TYPES.get(column_types[i])
                inserted_value = values[i-1]
                if type(inserted_value) is not expected_type:
                    errors.append(f"Несоответсвующий тип данных : значение {inserted_value} должно быть {column_types[i]}")
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
            is_valid_row = True
            for column, value in where_clause.items():
                if row.get(column) != value:
                    is_valid_row = False
                    break
            if is_valid_row:
                filtered_data.append(row)
        return filtered_data

@decorators.confirm_action("изменение записей таблицы")
def update(table_data, set_clause, where_clause):
    """
    Функция для изменения записей таблицы
    """
    for row in table_data:
        is_valid_row = True
        for column, value in where_clause.items():
            if row.get(column) != value:
                is_valid_row = False
                break
        if is_valid_row:
            row.update(set_clause)
    return table_data
@decorators.confirm_action("удаление записей таблицы")
def delete(table_data, where_clause):
    """
    Функция для удаления записей из таблицы
    """
    kept_rows = []
    for row in table_data:
        is_valid_row = True
        for column, value in where_clause.items():
            if row.get(column) != value:
                is_valid_row = False
                break
        if not is_valid_row:
            kept_rows.append(row)
    return kept_rows

def create_cacher():
    """
    Возвращает функцию кэширования, хранящую кэш в замыкании
    """
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result


def print_help():
    return



                






















