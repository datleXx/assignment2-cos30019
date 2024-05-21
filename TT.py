def TT_ENTAILS(KB, q):
    symbols = extract_symbols(KB, q)
    return TT_CHECK_ALL(KB, q, symbols, {})


def TT_CHECK_ALL(KB, q, symbols, model):
    if not symbols:
        for clause in KB.clauses:
            if not PL_TRUE(clause, model):
                return True  # When KB is false, always return true
        return PL_TRUE(q, model)
    else:
        P = symbols[0]
        rest = symbols[1:]
        return (TT_CHECK_ALL(KB, q, rest, {**model, P: True}) and
                TT_CHECK_ALL(KB, q, rest, {**model, P: False}))


def PL_TRUE(sentence, model):
    if isinstance(sentence, str):
        # return model.get(sentence, False)
        return True
    elif isinstance(sentence, dict):
        return all(PL_TRUE(p, model) for p in sentence['PREMISE']) and PL_TRUE(sentence['CONCLUSION'], model)
    else:
        raise ValueError("Invalid sentence format")


def extract_symbols(KB, q):
    # Extract the list of proposition symbols from KB and q
    symbols = set()

    # Extract symbols from the knowledge base
    for clause in KB.clauses:
        for symbol in clause["PREMISE"]:
            symbols.add(symbol)
        symbols.add(clause["CONCLUSION"])

    # Extract symbols from the query
    if isinstance(q, str):
        symbols.add(q)
    elif isinstance(q, tuple):
        symbols.update(q[1:])

    return list(symbols)
