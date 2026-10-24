import shlex
from primitive_db import constants

def convert_value(token):
    """
    Разбивает введенные пользователем условия на токены
    """
    if token.startswith(('"', "'")):
        return token[1:-1]
    if token.lstrip("-").isdigit():
        return int(token)
    if token.lower() in ("true", "false"):
        return token.lower() == "true"
    return token


def parse_conditions(user_input):
    """
    Возвращает условия в виде: 'column_name' : value
    """
    lexer = shlex.shlex(user_input, punctuation_chars="=")
    lexer.whitespace_split = True
    tokens = [t for t in lexer if t not in constants.SEPARATORS]
    if len(tokens) % 3 != 0:
        print(f"Неверный формат условия: {user_input}, ожидается условие типа: column_name=value")
        return {}
    conditions = {}
    for i in range(0, len(tokens), 3):
        column, sign, value = tokens[i:i + 3]
        if sign != "=":
            print(f"Ожидался знак =, получено {sign}")
            return {}
        conditions[column] = convert_value(value)
    return conditions

def parse_where(params):
    """
    Возвращает условия из части where или None, если where не указан
    """
    if "where" not in params:
        return None
    where_index = params.index("where")
    return parse_conditions(" ".join(params[where_index + 1:]))


def parse_set(params):
    """
    Возвращает значения из части set или None, если set не указан
    """
    if "set" not in params:
        return None
    set_index = params.index("set")
    end = params.index("where") if "where" in params else len(params)
    return parse_conditions(" ".join(params[set_index + 1:end]))