def evaluate_rpn(expression):
    stack = []

    for token in expression.split():
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            # Если токен - число, добавляем его в стек
            stack.append(int(token))
        else:
            # Если токен - оператор, извлекаем два последних числа из стека
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)  # Целочисленное деление

    # В конце в стеке должно остаться одно число - результат
    return stack[0]

# Пример использования
expression = "3 4 + 2 * 7 /"
result = evaluate_rpn(expression)
print(f"Результат выражения '{expression}' = {result}")
