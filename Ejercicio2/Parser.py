def parse_grammar_lines(lines):
    """
    Dadas las líneas validadas, retorna:
      - grammar: dict nonterminal -> set(production_tuples)
      - start_symbol: primer LHS encontrado
    Representación: cada producción es una tupla de símbolos; epsilon -> empty tuple ()
    """
    grammar = defaultdict(set)
    start_symbol = None
    for lineno, line in enumerate(lines, start=1):
        m = PROD_RE.match(line)
        if not m:
            raise ValueError(f"Línea {lineno} inválida: {line!r}")
        lhs = m.group('lhs')
        rhs = m.group('rhs')
        if start_symbol is None:
            start_symbol = lhs
        # split by '|' and strip
        alternatives = [alt.strip() for alt in re.split(r'\|', rhs)]
        for alt in alternatives:
            if alt in ('ε', 'eps'):
                prod = tuple()  # epsilon = empty tuple
            else:
                # alt is a sequence of symbols (each character treated as symbol)
                # According to problem: letras individuales son símbolos; sin embargo
                # si aparecen dígitos o secuencias, se toman carácter a carácter.
                prod = tuple(list(alt))
            grammar[lhs].add(prod)
    return grammar, start_symbol

def grammar_to_string(grammar):
    lines = []
    for A in sorted(grammar.keys()):
        prods = grammar[A]
        rhs = []
        for p in sorted(prods):
            if len(p) == 0:
                rhs.append('ε')
            else:
                rhs.append(''.join(p))
        lines.append(f"{A} -> " + " | ".join(rhs))
    return "\n".join(lines)