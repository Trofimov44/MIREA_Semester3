def OPZ(expression):
    output = []  # Список для хранения выходного выражения
    stack = []   # Стек для хранения операторов и скобок
    # Обрабатываем каждый токен в выражении
    for token in expression.split():
        if token.isalnum():  # Если токен - число или переменная
            output.append(token)  
        elif token == '(': # Если токен - открывающая скобка
            stack.append(token)  
        elif token == ')':  # Если токен - закрывающая скобка
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() 
        else:  # Если токен - оператор
            while (stack and priority(stack[-1]) >= priority(token)):
                output.append(stack.pop())
            stack.append(token)  # Добавляем текущий оператор в стек

    # Выталкиваем все оставшиеся операторы из стека в выходной список
    while stack:
        output.append(stack.pop())
    return ' '.join(output)  # Возвращаем результат в виде строки

def priority(op):
    # Определяет приоритет операторов
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0

expression = input("Введите алгебраическое выражение, разделяя пробелами: ")
result = OPZ(expression)
print(result)  # Вывод
