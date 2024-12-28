from colorama import Fore, Back, Style
Bin_num = ['1', '0', 'B', 'b']
Oct_num = [ '0', '1', '2', '3', '4', '5', '6', '7', 'O', 'o']
Dec_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'D', 'd']
Hex_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ,
           'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f', 'H', 'h']
real_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e', 'E']
keywords = ["for", "do", "while", "int", "float", "bool", "end", "begin",
            "if", "else", "for", "to", "next", "writeln", "readln", "true", "false", "step"]

class States:
    H = "H"
    ID = "ID"
    NM = "NM"
    ASGN = "ASGN"
    DLM = "DLM"
    COMM = "COMM"
    ERR = "ERR"

class TokNames:
    KWORD = "KWORD"
    IDENT = "IDENT"
    NUM = "NUM"
    OPER = "OPER"
    DELIM = "DELIM"
    ERR = "ERR"

class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value

class LexemeTable:
    def __init__(self, tok=None):
        self.tok = tok
        self.next = None

lt = None
lt_head = None

def is_kword(id):
    return id in keywords

def add_token(tok):
    global lt, lt_head
    new_entry = LexemeTable(tok)
    if lt is None:
        lt = new_entry
        lt_head = new_entry
    else:
        lt.next = new_entry
        lt = new_entry


tokens_names = []
tokens_values = []
line_count = 0
line_err = []

def lexer(filename):
    global int_flag, bool_flag, float_flag
    global line_count, line_err
    try:
        with (open(filename, "r", encoding="utf-8") as fd):
            CS = States.H
            c = fd.read(1)
            while c:
                if CS == States.H:
                    while c in [' ', '\t', '\n']:
                        if c == '\n':
                            line_count += 1
                            tok = Token(TokNames.DELIM, '\\n')  # Создаём токен новой строки
                            add_token(tok)
                            tokens_names.append(tok.token_name)
                            tokens_values.append(tok.token_value)
                        c = fd.read(1)
                    if c.isalpha():
                        CS = States.ID
                    elif c.isdigit() or c == '.':
                        CS = States.NM
                    elif c == ':':
                        CS = States.ASGN
                    elif c == '(':
                        c = fd.read(1)
                        if c == '*':  # Begin comment
                            CS = States.COMM
                            c = fd.read(1)
                        else:
                            tok = Token(TokNames.DELIM, '(')
                            add_token(tok)
                            CS = States.H
                            tokens_names.append(tok.token_name)
                            tokens_values.append(tok.token_value)
                    else:
                        CS = States.DLM
                elif CS == States.ASGN:
                    c = fd.read(1)
                    if c == '=':
                        tok = Token(TokNames.OPER, ":=")
                        add_token(tok)
                        c = fd.read(1)
                        CS = States.H
                    else:
                        tok = Token(TokNames.DELIM, ":")
                        add_token(tok)
                        CS = States.H
                    tokens_names.append(tok.token_name)
                    tokens_values.append(tok.token_value)
                elif CS == States.DLM:
                    if c in ['(', ')', ';', ',', '"']:
                        tok = Token(TokNames.DELIM, c)
                        add_token(tok)
                        c = fd.read(1)
                        CS = States.H
                    elif c in ['*', '/', '!', '=', '<', '>', '+', '-']:
                        buf = c
                        c = fd.read(1)
                        if buf in ['<', '>', '=', '!']:
                            if c == '=':
                                buf += c
                                tok = Token(TokNames.OPER, buf)
                                add_token(tok)
                                c = fd.read(1)

                            elif buf in ['<', '>']:
                                tok = Token(TokNames.OPER, buf)
                                add_token(tok)
                                c = fd.read(1)
                            else:
                                tok = Token(TokNames.ERR, buf)
                                line_err.append(line_count + 1)
                                add_token(tok)
                                c = fd.read(1)
                                CS = States.ERR
                        elif buf == '=' and c == '=':
                            buf += c
                            tok = Token(TokNames.OPER, buf)
                            add_token(tok)
                            c = fd.read(1)
                        else:
                            tok = Token(TokNames.OPER, buf)
                            add_token(tok)
                        CS = States.H
                    elif c == '&':
                        buf = c
                        c = fd.read(1)
                        if c == '&':
                            buf += c
                            tok = Token(TokNames.OPER, buf)
                            add_token(tok)
                            c = fd.read(1)
                        else:
                            tok = Token(TokNames.ERR, buf)
                            line_err.append(line_count + 1)
                            add_token(tok)
                        CS = States.H
                    elif c == '|':
                        buf = c
                        c = fd.read(1)
                        if c == '|':
                            buf += c
                            tok = Token(TokNames.OPER, buf)
                            add_token(tok)
                            c = fd.read(1)
                        else:
                            tok = Token(TokNames.ERR, buf)
                            line_err.append(line_count + 1)
                            add_token(tok)
                        CS = States.H
                    else:
                        tok = Token(TokNames.ERR, c)
                        line_err.append(line_count + 1)
                        add_token(tok)
                        c = fd.read(1)
                        CS = States.ERR
                    tokens_names.append(tok.token_name)
                    tokens_values.append(tok.token_value)
                elif CS == States.COMM:
                    while c:
                        if c == '*':
                            c = fd.read(1)
                            if c == ')':
                                c = fd.read(1)
                                CS = States.H
                                break
                        c = fd.read(1)
                elif CS == States.ERR:
                    CS = States.H
                elif CS == States.ID:
                    buf = c
                    c = fd.read(1)
                    while c.isalnum() or c == '_':
                        buf += c
                        c = fd.read(1)
                    if is_kword(buf):
                        tok = Token(TokNames.KWORD, buf)
                    else:
                        tok = Token(TokNames.IDENT, buf)
                    tokens_names.append(tok.token_name)
                    tokens_values.append(tok.token_value)
                    add_token(tok)
                    CS = States.H
                elif CS == States.NM:
                    buf = ''

                    is_Bin = True
                    is_Oct = True
                    is_Dec = True
                    is_Hex = True
                    is_real = True

                    B_count = 0
                    O_count = 0
                    D_count = 0
                    H_count = 0

                    E_count = 0
                    dot_count = 0
                    plus_minus_count = 0

                    while c.isdigit() or c.isalpha() or (c == '.') :
                        if c not in Bin_num or c in ['B','b']:
                            if c not in Bin_num:
                                is_Bin = False
                            else:
                                B_count += 1
                        if c not in Oct_num or c in ['O', 'o']:
                            if c not in Oct_num:
                                is_Oct = False
                            else:
                                O_count += 1
                        if c not in Dec_num or c in ['D', 'd']:
                            if c not in Dec_num:
                                is_Dec = False
                            else:
                                D_count += 1
                        if c not in Hex_num or c in ['H', 'h']:
                            if c not in Hex_num:
                                is_Hex = False
                            else:
                                H_count += 1
                        if c not in real_num or c in ['E', 'e', '.']:
                                if c not  in real_num:
                                    is_real = False
                                else:
                                    while c.isdigit() or c.isalpha() or c in ['E', 'e', '.', '+', '-']:
                                        if c.isalpha() and c not in real_num:
                                            is_real = False
                                        if c in ['E', 'e']:
                                            E_count += 1
                                            buf = buf + c
                                            c = fd.read(1)
                                            if c in ['+', '-']:
                                                plus_minus_count += 1
                                            continue
                                        elif c == '.':
                                            dot_count += 1
                                        buf = buf + c
                                        c = fd.read(1)
                                    break
                        buf = buf + c
                        c = fd.read(1)
                    if is_Bin and buf[-1] in ['B', 'b'] and B_count == 1:
                        tok = Token(TokNames.NUM, buf)
                        add_token(tok)
                    elif is_Oct and buf[-1] in ['O', 'o'] and O_count == 1:
                        tok = Token(TokNames.NUM, buf)
                        add_token(tok)
                    elif is_Dec and buf[-1] in ['D', 'd'] and D_count == 1:
                        tok = Token(TokNames.NUM, buf)
                        add_token(tok)
                    elif is_Hex and buf[-1] in ['H', 'h'] and H_count == 1:
                        tok = Token(TokNames.NUM, buf)
                        add_token(tok)
                    elif (is_real and E_count <= 1 and dot_count <= 1
                          and plus_minus_count <= 1 and buf[-1] not in ['E', 'e', '+', '-']):
                        tok = Token(TokNames.NUM, buf)
                        add_token(tok)
                    else:
                        tok = Token(TokNames.ERR, buf)
                        line_err.append(line_count + 1)
                        add_token(tok)
                    tokens_names.append(tok.token_name)
                    tokens_values.append(tok.token_value)
                    CS = States.H

    except FileNotFoundError:
        print(f"\nCannot open file {filename}.\n")
        return -1

def get_tokens():
    current = lt_head
    while current:
        yield current.tok
        current = current.next

def print_tokens(lt_head):
    current = lt_head
    while current:
        if current.tok.token_name == 'ERR':
            print(Style.RESET_ALL + Back.RED + Fore.BLACK + f"Error token '{current.tok.token_value}' in line {line_err[0]}" )
            break
        else:
            print(Style.RESET_ALL + f"Token Name: {current.tok.token_name}, Token Value: {current.tok.token_value}")
        current = current.next

class SyntaxError(Exception):
    def __init__(self, message, line):
        super().__init__(f"Синтаксическая ошибка на строке {line}: {message}")
        self.line = line
        self.message = message

IDENT_list = []
def parser():
    global IDENT_list
    global begin_flag
    begin_flag = False
    global line_count, tokens_names, tokens_values
    token_iter = get_tokens()
    current_token = next(token_iter, None)

    def expect(expected_name, expected_value=None):
        nonlocal current_token
        if not current_token:
            raise SyntaxError("Неожиданный конец ввода", line_count)
        if current_token.token_name != expected_name or (expected_value and current_token.token_value != expected_value):
            raise SyntaxError(
                f"Ожидалось '{expected_name}' ('{expected_value}'), но получено '{current_token.token_name}' ('{current_token.token_value}')",
                line_count,
            )
        current_token = next(token_iter, None)

    def parse_declaration():
        global IDENT_list
        type_token = current_token
        expect(TokNames.KWORD)
        while current_token and current_token.token_name == TokNames.IDENT:
            if current_token.token_value in IDENT_list:
                 raise SyntaxError("Переменная уже объявлена", line_count)
            else:
                IDENT_list.append(current_token.token_value)
                expect(TokNames.IDENT)
            if current_token and current_token.token_value == ',':
                expect(TokNames.DELIM, ',')
                if current_token.token_name != TokNames.IDENT:
                    raise SyntaxError("Ожидался идентификатор в объявлении переменной", line_count)
            elif current_token and current_token.token_value == ':':
                expect(TokNames.DELIM, ':')
                break
            elif current_token and current_token.token_value == '\\n':
                expect(TokNames.DELIM, '\\n')
                break
            else:
                raise SyntaxError("Ожидался ',' или ':' или \\n в объявлении переменной", line_count)


    def parse_assignment():
        global begin_flag
        expect(TokNames.IDENT)  # Ожидаем идентификатор
        expect(TokNames.OPER, ':=')  # Ожидаем оператор присваивания
        if current_token.token_name in [TokNames.NUM, TokNames.IDENT]:  # Ожидаем число или идентификатор
            expect(current_token.token_name)
        else:
            raise SyntaxError("Ожидалось число или идентификатор в присваивании", line_count)
        if begin_flag:
            if current_token and current_token.token_value == '\\n':
                expect(TokNames.DELIM, '\\n')
        else:
            if current_token and current_token.token_value == ':':
                expect(TokNames.DELIM, ':')
            elif current_token and current_token.token_value == '\\n':
                expect(TokNames.DELIM, '\\n')
            else:
                raise SyntaxError("Ожидался ':' или \\n", line_count)

    def parse_statement():
        if current_token.token_value == '\\n':
            expect(TokNames.DELIM, '\\n')
        elif current_token.token_name == TokNames.KWORD and current_token.token_value == "while":
            parse_while()
        elif current_token.token_name == TokNames.IDENT:
            parse_assignment()
        elif current_token.token_name == TokNames.KWORD and current_token.token_value == "writeln":
            parse_writeln()
        elif current_token.token_name == TokNames.KWORD and current_token.token_value == "readln":
            parse_readln()
        elif current_token.token_name == TokNames.KWORD and current_token.token_value == "begin":
            parse_begin()
        elif current_token.token_name == TokNames.KWORD and current_token.token_value == "for":
            parse_for()
        elif current_token.token_name == TokNames.KWORD and current_token.token_value == "if":
            parse_if()
        else:
            raise SyntaxError("Неожиданный токен в инструкции", line_count)

    def parse_while():
        count_bracket = 0
        expect(TokNames.KWORD, "while")
        expect(TokNames.DELIM, '(')
        while current_token.token_value == '(':
            expect(TokNames.DELIM, '(')
            count_bracket += 1
        parse_condition()
        expect(TokNames.DELIM, ')')
        while current_token.token_value == ')':
            expect(TokNames.DELIM, ')')
            count_bracket -= 1
        if count_bracket != 0:
            raise SyntaxError("Неожиданный токен в инструкции", line_count)
        parse_statement()
        while current_token and not (current_token.token_name == TokNames.DELIM and current_token.token_value == ";"):
            parse_statement()
        expect(TokNames.DELIM, ';')

    def parse_condition():
        expect(TokNames.IDENT)
        if current_token.token_name == TokNames.OPER and current_token.token_value in ['==', '!=', '<', '>', '<=', '>=']:
            expect(TokNames.OPER)
        else:
            raise SyntaxError("Ожидался оператор сравнения в условии", line_count)
        if current_token.token_name == TokNames.NUM or current_token.token_name == TokNames.IDENT:
            expect(current_token.token_name)
        else:
            raise SyntaxError("Ожидалось число или идентификатор в условии", line_count)

    def parse_begin():
        global begin_flag
        expect(TokNames.KWORD, "begin")
        begin_flag = True
        while current_token and not (current_token.token_name == TokNames.KWORD and current_token.token_value == "end"):
            parse_statement()
        begin_flag = False
        expect(TokNames.KWORD, "end")

    def parse_for():
        expect(TokNames.KWORD, "for")
        expect(TokNames.IDENT)  # Переменная цикла
        expect(TokNames.OPER, ":=")  # Присваивание
        expect(TokNames.NUM)  # Начальное значение
        expect(TokNames.KWORD, "to")  # Ключевое слово to
        if current_token.token_name in [TokNames.NUM, TokNames.IDENT]:  # Конечное значение
            expect(current_token.token_name)
        else:
            raise SyntaxError("Ожидалось конечное значение в цикле for", line_count)

        if current_token.token_name == TokNames.KWORD and current_token.token_value == "step":  # Необязательный step
            expect(TokNames.KWORD, "step")
            if current_token.token_name in [TokNames.NUM, TokNames.IDENT]:
                expect(current_token.token_name)
            else:
                raise SyntaxError("Ожидалось значение шага в цикле for", line_count)

        # Ожидаем тело цикла
        while current_token and not (current_token.token_name == TokNames.KWORD and current_token.token_value == "next"):
            parse_statement()

        expect(TokNames.KWORD, "next")  # Завершающее ключевое слово
        expect(TokNames.DELIM, ';')  # Символ ';'

    def parse_writeln():
        global begin_flag
        count_bracket = 0
        expect(TokNames.KWORD, "writeln")
        while current_token and (current_token.token_name == TokNames.IDENT or current_token.token_name == TokNames.NUM
        or current_token.token_value == '('):
            if current_token.token_name == TokNames.IDENT:
                expect(TokNames.IDENT)
            elif current_token.token_value == '(':
                expect(TokNames.DELIM, '(')
                while current_token.token_value == '(':
                    expect(TokNames.DELIM, '(')
                    count_bracket += 1
                parse_condition()
                expect(TokNames.DELIM, ')')
                while current_token.token_value == ')':
                    expect(TokNames.DELIM, ')')
                    count_bracket -= 1
                if count_bracket != 0:
                    raise SyntaxError("Неожиданный токен в инструкции", line_count)
            elif current_token.token_name == TokNames.NUM:
                expect(TokNames.NUM)
            if current_token and current_token.token_value == ',':
                expect(TokNames.DELIM, ',')
                if current_token.token_value == '\\n':
                    raise SyntaxError("Ожидался идентификатор", line_count)
            if begin_flag:
                if current_token and current_token.token_value == '\\n':
                    expect(TokNames.DELIM, '\\n')
            else:
                if current_token and current_token.token_value == ':':
                    expect(TokNames.DELIM, ':')
                elif current_token and current_token.token_value == '\\n':
                    expect(TokNames.DELIM, '\\n')
                else:
                    raise SyntaxError("Ожидался ':' или \\n", line_count)

    def parse_readln():
        global begin_flag
        expect(TokNames.KWORD)
        while current_token and current_token.token_name == TokNames.IDENT:
            expect(TokNames.IDENT)
            if current_token and current_token.token_value == ',':
                expect(TokNames.DELIM, ',')
                expect(TokNames.IDENT)
        if begin_flag:
            if current_token and current_token.token_value == '\\n':
                expect(TokNames.DELIM, '\\n')
        else:
            if current_token and current_token.token_value == ':':
                expect(TokNames.DELIM, ':')
            elif current_token and current_token.token_value == '\\n':
                expect(TokNames.DELIM, '\\n')
            else:
                raise SyntaxError("Ожидался ':' или \\n", line_count)

    def parse_if():
        expect(TokNames.KWORD, "if")
        count_bracket = 0
        expect(TokNames.DELIM, '(')
        while current_token.token_value == '(':
            expect(TokNames.DELIM, '(')
            count_bracket += 1
        parse_condition()
        expect(TokNames.DELIM, ')')
        while current_token.token_value == ')':
            expect(TokNames.DELIM, ')') 
            count_bracket -= 1
        if count_bracket != 0:
            raise SyntaxError("Неожиданный токен в инструкции", line_count)
        parse_statement()
        while current_token and not (current_token.token_value in [';', 'else']):
            parse_statement()
        if current_token.token_name == TokNames.KWORD and current_token.token_value == "else":
            expect(TokNames.KWORD, 'else')
            while current_token and not (current_token.token_value in [';']):
                parse_statement()
        expect(TokNames.DELIM, ';')

    try:
        while current_token:
            if current_token.token_value == '\\n':
                current_token = next(token_iter, None)
            elif current_token.token_name == TokNames.KWORD and current_token.token_value in ['int', 'bool', 'float']:
                parse_declaration()
            else:
                parse_statement()
    except SyntaxError as e:
        print(Style.RESET_ALL + Back.RED + Fore.BLACK + f"{e.message}")
        return -1
    return 0


def main():
    filename = "test.txt"

    result = lexer(filename)
    if result == -1:
        print("Лексический анализ завершился с ошибкой.")
    else:
        print(Style.RESET_ALL + Back.GREEN + Fore.BLACK +"Лексический анализ успешно завершён:")
        print_tokens(lt_head)

        parse_result = parser()
        if parse_result == 0:
            print(Style.RESET_ALL + Back.GREEN + Fore.BLACK + "Синтаксический анализ успешно завершён.")
        else:
            print(Style.RESET_ALL + Back.RED + Fore.BLACK + "Синтаксический анализ завершился с ошибкой.")

if __name__ == "__main__":
    main()
