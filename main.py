import math
def parse(tokens):
    return round(parse_expr(tokens)[0], 12)

def parse_fn(tokens): 
    if not tokens:
        return(None, tokens)
    if tokens[0] != "fn":
        return (None, tokens)
    (name, tokens) = (tokens[0], tokens[1:])
    params = []
    while True:
        if not tokens:
            raise ValueError("Function requires parameters")
        (param, tokens) = (tokens[0], tokens[1:])
        if param == "=":
            break
        params.append(param)
    


def parse_expr(tokens):
    return parse_equals(tokens)

variables = {}

def parse_equals(tokens):
    if not tokens:
        return(None, tokens)
    (name, tok) = (tokens[0], tokens[1:])
    (op, tok) = parse_symbol(tok, "=")
    if not op:
        return parse_add_sub(tokens)
    (value, tokens) = parse_expr(tok)
    variables[name] = value
    return (value, tokens)

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

def parse_mult_div(tokens):
    (a, tokens) = parse_unary(tokens)
    if not a:
        return (None, tokens)
    while True:
        (op, tokens) = parse_symbol(tokens, "*/")
        if not op:
            if tokens and tokens[0] == "(":
                op = "*"
            else:
                return (a, tokens)
        (b, tok) = parse_unary(tokens)
        if not b:
            raise ValueError(f"{op} requires a right side")
        match op:
            case "*": a *= b
            case "/": a /= b
        tokens = tok

def parse_unary(tokens):
    (op, tokens) = parse_symbol(tokens, ["-","sin","cos","tan","asin","acos","atan"])
    if not op:
        return parse_power(tokens)
    (num, tokens) = parse_unary(tokens)
    match op:
        case "-": num = -num
        case "sin": num = math.sin(num)
        case "cos": num = math.cos(num)
        case "tan": num = math.tan(num)
        case "asin": num = math.asin(num)
        case "acos": num = math.acos(num)
        case "atan": num = math.atan(num)
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
    if tokens[0] in symbols:
        return (None, tokens)
    else:
        match tokens[0]:
            case "pi": return (math.pi, tokens[1:])
            case _: return (variables[tokens[0]], tokens[1:])

def parse_symbol(tokens, symbols):
    if len(tokens) == 0:
        return (None, tokens)

    if str(tokens[0]) in symbols:
        return (tokens[0], tokens[1:])
    else:
        return (None, tokens)

symbols = "+-/*()<>^="

def lex(inp):
    tokens = []
    i = 0
    while i < len(inp):
        c = inp[i]
        if c in symbols:
            tokens.append(c)
            i += 1
        elif c.isdigit():
            num = c
            i += 1
            while i < len(inp) and inp[i].isdigit():
                num += inp[i]
                i += 1
            tokens.append(int(num))
        elif c.isalpha():
            word = c
            i += 1
            while i < len(inp) and inp[i].isalpha():
                word += inp[i]
                i += 1
            tokens.append(word)
        else:
            i += 1
    return tokens

        
while True:
    inp = input("> ")
    try:
        print(parse(lex(inp)))
    except Exception as e:
        print(f"Error: {e}")

