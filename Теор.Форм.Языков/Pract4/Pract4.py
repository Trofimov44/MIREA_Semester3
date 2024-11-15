Bin_num = ['1', '0', 'B', 'b']
Oct_num = [ '0', '1', '2', '3', '4', '5', '6', '7', 'O', 'o']
Dec_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'D', 'd']
Hex_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ,
           'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f', 'H', 'h']
real_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'e', 'E']
keywords = ["for", "do", "while", "int", "float", "bool", "end", "begin",
            "if", "else", "for", "to", "next", "writeln", "readln", "true", "false"]

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

def lexer(filename):
    try:
        with (open(filename, "r") as fd):
            CS = States.H
            c = fd.read(1)
            while c:
                if CS == States.H:
                    while c in [' ', '\t', '\n']:
                        c = fd.read(1)
                    if c.isalpha() or c == '_':
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
                    else:
                        CS = States.DLM
                elif CS == States.ASGN:
                    colon = c
                    c = fd.read(1)
                    if c == '=':
                        tok = Token(TokNames.OPER, ":=")
                        add_token(tok)
                        c = fd.read(1)
                        CS = States.H
                    else:
                        tok = Token(TokNames.OPER, ":")
                        add_token(tok)
                        CS = States.H
                elif CS == States.DLM:
                    if c in ['(', ')', ';', ',', '"']:
                        tok = Token(TokNames.DELIM, c)
                        add_token(tok)
                        c = fd.read(1)
                        CS = States.H
                    elif c in ['+', '-', '*', '/', '!', '=', '<', '>', '+', '-']:
                        buf = c
                        c = fd.read(1)
                        if buf in ['<', '>', '=']:
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
                                print(f"\nUnknown character: {buf}")
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
                            print(f"\nUnknown character after &: {c}")
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
                            print(f"\nUnknown character after |: {c}")
                        CS = States.H
                    else:
                        print(f"\nUnknown character: {c}")
                        c = fd.read(1)
                        CS = States.ERR
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
                    elif is_real and E_count <= 1 and dot_count <= 1 and plus_minus_count <= 1 and buf[-1] not in ['E', 'e']:
                        tok = Token(TokNames.NUM, buf)
                        add_token(tok)
                    else:
                        print(f"Unknown character: {buf}")
                    CS = States.H

    except FileNotFoundError:
        print(f"\nCannot open file {filename}.\n")
        return -1

def print_tokens(lt_head):
    current = lt_head
    while current:
        print(f"Token Name: {current.tok.token_name}, Token Value: {current.tok.token_value}")
        current = current.next

def main():
    filename = "test.txt"

    result = lexer(filename)

    if result == -1:
        print("Lexical analysis failed.")
    else:
        print("\nLexical analysis successful.")
        print_tokens(lt_head)

if __name__ == "__main__":
    main()
