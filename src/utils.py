import re


def remove_symbols(string):
    string = "".join([c for c in string if c.isalpha() or c.isdigit() or c == " "]).rstrip()
    string = re.sub(" +", " ", string)
    return string
