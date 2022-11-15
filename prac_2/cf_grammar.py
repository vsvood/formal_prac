"""This module provide class for context-free grammar"""


class CFGrammar:
    """This class represents context-free grammar"""

    def __init__(self, data: str = None):
        self.var = None
        self.alpha = None
        self.start = None
        self.rel = {}
        if data:
            lines = data.split('\n')
            macro_count = 0
            while lines[macro_count].startswith("$"):
                self.__parse_header(lines[macro_count])
                macro_count += 1
            self.__parse_rel(lines[macro_count:])

    def __parse_header(self, line: str):
        if line.startswith("$VARIABLES:"):
            self.__parse_var(line)
        elif line.startswith("$ALPHABET:"):
            self.__parse_alpha(line)
        elif line.startswith("$START:"):
            self.__parse_start(line)
        else:
            raise Exception("unknown macro: %s" % line.split()[0])

    def __parse_var(self, line: str):
        self.var = set(line.split()[1:])

    def __parse_alpha(self, line: str):
        self.alpha = set(line.split()[1:])

    def __parse_start(self, line: str):
        self.start = line.split()[1]

    def __parse_rel(self, lines: list[str]):
        rel = [rule.split('->') for rule in lines if rule != ""]

        if self.start is None:
            if len(rel) > 0:
                if len(rel[0]) > 0:
                    self.start = rel[0][0]
                else:
                    raise Exception("bad variable ''")

        for key, rule_set in rel:
            if key == "":
                raise Exception("bad variable ''")
            if self.var and key not in self.var:
                raise Exception("unknown variable %s" % key)

            rule_set = {tuple(rule.split(" ")) for rule in rule_set.split("|")}
            self.__check_rule_set(rule_set)

            if key not in self.rel:
                self.rel[key] = rule_set
            else:
                self.rel[key].update(rule_set)

        self.__guess_missing()

    def __check_rule_set(self, rule_set):
        for rule in rule_set:
            for token in rule:
                if (self.var and token not in self.var) and \
                        (self.alpha and token not in self.alpha) and \
                        token != "":
                    raise Exception("unknown token %s" % token)

    def __guess_missing(self):
        if self.var is None:
            self.__guess_var()
        if self.alpha is None:
            self.__guess_alpha()

    def __guess_var(self):
        self.var = set(self.rel.keys())

    def __guess_alpha(self):
        self.alpha = set()
        for rule_set in self.rel.values():
            for rule in rule_set:
                for token in rule:
                    if token not in self.var and token != "":
                        self.alpha.add(token)

    def __str__(self):
        return "$VARIABLES: " + \
               " ".join(self.var) + "\n" + \
               "$ALPHABET: " + \
               " ".join(self.alpha) + "\n" + \
               "$START: " + \
               str(self.start) + "\n" + \
               "\n".join([key + "->" + "|".join([" ".join(rule) for rule in rule_set])
                          for key, rule_set in self.rel.items()])
