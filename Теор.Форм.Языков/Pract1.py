# Приоритет операторов
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    if op == '^':
        return 3
    return 0


# Функция для проверки, является ли символ оператором
def is_operator(c):
    return c in {'+', '-', '*', '/', '^'}


# Преобразование инфиксной записи в обратную польскую запись
def infix_to_postfix(expression):
    stack = []  # Стек для операторов
    result = []  # Выходная строка (ОПЗ)

    for char in expression:
        # Если символ — операнд, добавляем его к результату
        if char.isalnum():  # Если символ буква или цифра
            result.append(char)
        # Если символ — открывающая скобка, помещаем его в стек
        elif char == '(':
            stack.append(char)
        # Если символ — закрывающая скобка
        elif char == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()  # Убираем '(' из стека
        # Если символ — оператор
        else:
            while stack and precedence(stack[-1]) >= precedence(char):
                result.append(stack.pop())
            stack.append(char)

    # Выкидываем все оставшиеся операторы из стека в результат
    while stack:
        result.append(stack.pop())

    return ''.join(result)


# Пример использования
expression = "a+b*(c^d-e)^(f+g*h)-i"
print("Исходное выражение:", expression)
print("Обратная польская запись:", infix_to_postfix(expression))

