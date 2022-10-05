"""This module defines functions to work with regular expressions"""


def regexp_to_rpn(regexp: str) -> list:
    """Translates regular expression to
    reverse polish notation stored as list"""
    stack = []
    result = []
    token = ""
    mul_flag = False
    i = 0
    while i < len(regexp):
        while i < len(regexp) and regexp[i].isalpha():
            if i == len(regexp) - 1:
                token += regexp[i]
            elif regexp[i + 1] != "^":
                token += regexp[i]
            else:
                if token:
                    result.append(token)
                    stack.append("&")
                token = regexp[i]
            i += 1
        if token:
            if mul_flag:
                stack.append("&")
            mul_flag = True
            result.append(token)
            token = ""
        if i >= len(regexp):
            break
        if regexp[i] == "^":
            mul_flag = True
            if i == len(regexp) - 1:
                raise Exception("Bad degree at " + str(i))
            i += 1
            if regexp[i] in ["+", "*"]:
                result.append(regexp[i])
                i += 1
            elif regexp[i].isdigit():
                token = 0
                while i < len(regexp) and regexp[i].isdigit():
                    token *= 10
                    token += int(regexp[i])
                    i += 1
                result.append(str(token))
                token = ""
            else:
                raise Exception("Bad degree value at " + str(i) + ": " + regexp[i])
        elif regexp[i] == "(":
            if mul_flag:
                stack.append("&")
            mul_flag = False
            stack.append("(")
            i += 1
        elif regexp[i] == ")":
            mul_flag = True
            while True:
                if not stack:
                    raise Exception("No '(' for ')' at " + str(i))
                token = stack.pop()
                if token == "(":
                    break
                result.append(token)
            token = ""
            i += 1
        elif regexp[i] == "*":
            mul_flag = False
            stack.append("&")
            i += 1
        elif regexp[i] == "+":
            mul_flag = False
            while stack and stack[-1] in "&":
                result.append(stack.pop())
            stack.append("|")
            i += 1
        elif regexp[i] == "1":
            if mul_flag:
                stack.append("&")
            mul_flag = True
            result.append("")
            i += 1
        else:
            raise Exception("Unknown symbol at " + str(i) + ": '" + regexp[i] + "'")
    while stack:
        result.append(stack.pop())
    return result
