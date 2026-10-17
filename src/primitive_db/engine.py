import prompt

COMMANDS = {
    "exit": "выйти из программы",
    "help": "справочная информация",
}


def welcome():
    """
    приветствие и основной цикл обработки команд
    """
    print("Первая попытка запустить проект!")
    print()
    print("***")
    while True:
        for command, description in COMMANDS.items():
            print(f"<command> {command} - {description}")
        answer = prompt.string("Введите команду: ")
        print()
        if answer == "exit":
            break