import re
def RE_ATTR():
    return re.compile(r'([^\s\(\)]+(\.[^\s\(\)]+)*)\.(\w*)$')



def XONSH_EXPR_TOKENS():
    return {
        'and ', 'else', 'for ', 'if ', 'in ', 'is ', 'lambda ', 'not ', 'or ',
        '+', '-', '/', '//', '%', '**', '|', '&', '~', '^', '>>', '<<', '<',
        '<=', '>', '>=', '==', '!=', ',', '?', '??', '$(',
        '${', '$[', '...', '![', '!(', '@(', '@$(', '@',
        }


def XONSH_STMT_TOKENS():
    return {
        'as ', 'assert ', 'break', 'class ', 'continue', 'def ', 'del ',
        'elif ', 'except ', 'finally:', 'from ', 'global ', 'import ',
        'nonlocal ', 'pass', 'raise ', 'return ', 'try:', 'while ', 'with ',
        'yield ', '-', '/', '//', '%', '**', '|', '&', '~', '^', '>>', '<<',
        '<', '<=', '->', '=', '+=', '-=', '*=', '/=', '%=', '**=',
        '>>=', '<<=', '&=', '^=', '|=', '//=', ';', ':', '..',
        }
def XONSH_TOKENS():
    return set(XONSH_EXPR_TOKENS) | set(XONSH_STMT_TOKENS)
