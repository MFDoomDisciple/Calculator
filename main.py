def parse(tokens):
    return parse_expr(tokens)[0]

def parse_expr(tokens):
    return parse_add_sub(tokens)

def parse_mult_div(tokens):
    (a, tokens) = parse_unary(tokens)
    if not a:
        return (None, tokens)
    while True:
        (op, tokens) = parse_symbol(tokens, "*/")
        if not op:
            return (a, tokens)
        (b, tok) = parse_unary(tokens)
        if not b:
            raise ValueError(f"{op} requires a right side")
        match op:
            case "*": a *= b
            case "/": a /= b
        tokens = tok

def parse_add_sub(tokens):
    (a, tokens) = parse_mult_div(tokens)
    if not a:
        return (None, tokens)
    while True:
        (op, tokens) = parse_symbol(tokens, "+-")
        if not op:
            return (a, tokens)
        (b, tok) = parse_mult_div(tokens)
        if not b:
            raise ValueError(f"{op} requires a right side")
        match op:
            case "+": a += b
            case "-": a -= b
        tokens = tok

def parse_unary(tokens):
    (op, tokens) = parse_symbol(tokens, "-")
    if not op:
        return parse_power(tokens)
    (num, tokens) = parse_unary(tokens)
    match op:
        case "-": num = -num
    return (num, tokens)

def parse_power(tokens):
    (a, tokens) = parse_term(tokens)
    if not a:
        return (None, tokens)
    while True:
        (op, tokens) = parse_symbol(tokens, "^")
        if not op:
            return (a, tokens)
        (b, tok) = parse_term(tokens)
        if not b:
            raise ValueError(f"{op} requires a right side")
        match op:
            case "^": a **= b
        tokens = tok
    

def parse_term(tokens):
    (num, tokens) = parse_num(tokens)
    if num:
        return (num, tokens)
    (paren, tokens) = parse_symbol(tokens, "(")
    if not paren:
        return (None, tokens)
    (expr, tokens) = parse_expr(tokens)
    (paren, tokens) = parse_symbol(tokens, ")")
    if not paren:
        raise ValueError("Expected )")
    return (expr, tokens)

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
    try:
        print(parse(lex(inp)))
    except Exception as e:
        print(f"Error: {e}")

