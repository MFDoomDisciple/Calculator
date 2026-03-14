def parse(tokens):
    return parse_add_sub(tokens)[0]

def parse_parens(tokens):
    pass

def parse_expr(tokens):
    pass

def parse_mult_div(tokens):
    (a, tokens) = parse_term(tokens)
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
    (a, tokens) = parse_mult_div(tokens)
    if not a:
        return (None, tokens)
    (op, tokens) = parse_symbol(tokens, "+-")
    if not op:
        return (a, tokens)
    (b, tokens) = parse_add_sub(tokens)
    if not b:
        raise ValueError(f"{op} requires a right side")
    match op:
        case "+": return (a+b, tokens)
        case "-": return (a-b, tokens)

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
        if c in "+-/*()<>":
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
