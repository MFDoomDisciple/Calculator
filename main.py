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
    print(lex(inp))
