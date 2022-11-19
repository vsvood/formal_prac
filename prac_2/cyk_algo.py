from cf_grammar import CFGrammar


def init(dp: dict, grammar: CFGrammar, phrase: str):
    for key in grammar.rel:
        dp[key] = []
        for j in range(len(phrase)+1):
            dp[key].append([])
            for _ in range(len(phrase)+1):
                dp[key][j].append(False)

    for key, rule_set in grammar.rel.items():
        for rule in rule_set:
            if len(rule) == 1 and rule != ("",):
                for idx, char in enumerate(phrase):
                    if (char,) == rule:
                        dp[key][idx][idx+1] = True


def process_words(dp: dict[list[list[bool]]], grammar: CFGrammar, length: int, phrase_len: int):
    for start in range(phrase_len - length+1):
        for mid in range(start + 1, start + length):
            for key, rule_set in grammar.rel.items():
                for rule in rule_set:
                    if len(rule) == 2:
                        if dp[rule[0]][start][mid] and dp[rule[1]][mid][start + length]:
                            dp[key][start][start + length] = True


def cyk_check(grammar: CFGrammar, phrase: str) -> bool:
    if phrase == "":
        return ("",) in grammar.rel[grammar.start]

    dp = {}
    init(dp, grammar, phrase)

    for length in range(2, len(phrase)+1):
        process_words(dp, grammar, length, len(phrase))

    return dp[grammar.start][0][len(phrase)]
