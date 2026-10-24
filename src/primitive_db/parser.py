import shlex
from primitive_db import constants

def convert_value(token):
    if token.startswith(('"', "'")):
        return token[1:-1]
    if token.lstrip("-").isdigit():
        return int(token)
    if token.lower() in ("true", "false"):
        return token.lower() == "true"
    return token


def parse_conditions(user_input):
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