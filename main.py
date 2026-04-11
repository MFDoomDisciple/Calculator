def parse(tokens):
    return parse_add_sub(tokens)[0]

def parse_parens(tokens):
    (op, tokens) = parse_symbol(tokens, "(")
    (op, tokens) = parse_symbol(tokens, ")")
    if not op:
        print("returning")
        return (None, tokens)
    print("Got Here")
    (a, tokens) = parse_add_sub(tokens)
    if not a:
        return (None, tokens)
    return (a, tokens)

def parse_expr(tokens):
    (a, tokens) = parse_term(tokens)
    if not a:
        return (None, tokens)
    (op, tokens) = parse_symbol(tokens, "^")
    if op != "^":
        return (a, tokens)
    (b, tokens) = parse_term(tokens)
    if not b:
        raise ValueError(f"{op} requires a right side")
    match op:
        case "^": return (a**b, tokens)

def parse_mult_div(tokens):
    (a, tokens) = parse_expr(tokens)
    if not a:
        return (None, tokens)
    (op, tokens) = parse_symbol(tokens, "*/")
    if not op:
        return (a, tokens)
    (b, tokens) = parse_mult_div(tokens)
    if not b:
        raise ValueError(f"{op} requires a right side")
    match op:
        case "*": return (a*b, tokens)
        case "/": return (a/b, tokens)

def parse_add_sub(tokens):
    (para, tokens) = parse_parens(tokens)
    (a, tokens) = parse_mult_div(tokens)
    if not a:
        return (None, tokens)
    # (a, tokens) = parse_mult_div(tokens)
    # print(a)
    # print(tokens)
    # if not a:
    #     print("add_sub b failed")
    #     print(tokens)
    #     return (None, tokens)
    while True:
        (op, tokens) = parse_symbol(tokens, "+-")
        if not op:
            return (a, tokens)
        (para, tokens) = parse_parens(tokens)
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

    if str(tokens[0]) in symbols:
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
