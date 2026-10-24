from primitive_db import constants, utils


def create_table(metadata={}, table_name=str, columns={}):
    """
    Функция для создания таблицы
    """
    if table_name in metadata:
        print(f'Таблица {table_name} уже существует')
    else:
        contains_key = False
        for key in columns.keys():
            if key.lower() == 'id':
                contains_key = True
                break
        if contains_key == False:
            columns = {'ID' : 'int', **columns}
        
        for value in columns.values():
            if value not in constants.TYPES:
                print(f"Некорректный тип данных, допустимые: {', '.join(constants.TYPES)}")
                return
        metadata.update({table_name: columns})
        return metadata


def drop_table(metadata, table_name):
    """
    Функция для удаления таблицы
    """
    if table_name not in metadata:
        print(f'Таблицы {table_name} не существует')
        return metadata
    del metadata[table_name]
    return metadata

def validate_table(metadata, table_name, values):
        errors = []
        if table_name not in metadata:
            errors.append(f'Таблицы {table_name} не существует')
        if table_name in metadata:
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

def insert(metadata, table_name, values):
    errors = validate_table(metadata, table_name, values)
    if errors:
        for error in errors:
            print(error)
        return
    column_names = list(metadata.get(table_name).keys())
    data = utils.load_table_data(table_name)
    new_row = {"ID" : max((row["ID"] for row in data), default=0) + 1}
    for i in range(1, len(column_names)):
        new_row.update({column_names[i] : values[i-1]})
    data.append(new_row)
    utils.save_table_data(table_name, data)
    return data

def select(table_data, where_clause=None):
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

def update(table_data, set_clause, where_clause):
    for row in table_data:
        is_valid_row = True
        for column, value in where_clause.items():
            if row.get(column) != value:
                is_valid_row = False
                break
        if is_valid_row:
            row.update(set_clause)
    return table_data

def delete(table_data, where_clause):
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



                






















