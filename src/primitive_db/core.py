

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
        
        allowed_types = {'int', 'str', 'bool'}
        for value in columns.values():
            if value not in allowed_types:
                print(f"Некорректный тип данных, допустимые типы данных - {allowed_types}")
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
    
