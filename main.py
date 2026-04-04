def parse(tokens):
    return parse_add_sub(tokens)[0]

def parse_parens(tokens):
    pass

def parse_expr(tokens):
    (a, tokens) = parse_term(tokens)
    print(tokens)
    if not a:
        print("expr a failed")
        return (None, tokens)
    (op, tokens) = parse_symbol(tokens, "^")
    print(op)
    if op != "^":
        print("expr op failed " + str(a))
        return (a, tokens)
    (b, tokens) = parse_expr(tokens)
    if not b:
        raise ValueError(f"{op} requires a right side")
    match op:
        case "^": return (a^b, tokens)

def parse_mult_div(tokens):
    print(tokens)
    (a, tokens) = parse_expr(tokens)
    if not a:
        print("mult_div a failed")
        return (None, tokens)
    (op, tokens) = parse_symbol(tokens, "*/")
    if not op:
        print("mult_div op failed")
        return (a, tokens)
    (b, tokens) = parse_mult_div(tokens)
    if not b:
        raise ValueError(f"{op} requires a right side")
    match op:
        case "*": return (a*b, tokens)
        case "/": return (a/b, tokens)

def parse_add_sub(tokens):
    print(tokens)
    (a, tokens) = parse_mult_div(tokens)
    print(tokens)
    if not a:
        print("add_sub a failed")
        return (None, tokens)
    # (a, tokens) = parse_mult_div(tokens)
    # print(a)
    # print(tokens)
    # if not a:
    #     print("add_sub b failed")
    #     print(tokens)
    #     return (None, tokens)
    while True:
        print("add_sub is true")
        (op, tokens) = parse_symbol(tokens, "+-")
        if not op:
            print("add_sub op failed")
            return (a, tokens)
        (b, tok) = parse_mult_div(tokens)
        if not b:
            raise ValueError(f"{op} requires a right side")
        match op:
            case "+": a += b
            case "-": a -= b
        tokens = tok

def parse_term(tokens):
    return parse_num(tokens)

def parse_num(tokens):
    if len(tokens) == 0:
        return (None, tokens)
    if isinstance(tokens[0], int):
        return (tokens[0], tokens[1:])
    else:
        return (None, tokens)

def parse_symbol(tokens, symbols):
    if len(tokens) == 0:
        return (None, tokens)

    if tokens[0] in symbols:
        return (tokens[0], tokens[1:])
    else:
        return (None, tokens)

def lex(inp):
    tokens = []
    i = 0
    while i < len(inp):
        c = inp[i]
        if c in "+-/*()<>^":
            tokens.append(c)
            i += 1
        elif c.isdigit():
            num = c
            i += 1
            while i < len(inp) and inp[i].isdigit():
                num += inp[i]
                i += 1
            tokens.append(int(num))
        else:
            i += 1
    return tokens

        
while True:
    inp = input("> ")
    print(parse(lex(inp)))
