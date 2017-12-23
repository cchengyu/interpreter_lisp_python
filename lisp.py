#coding: utf-8
# 词法分析-分解输入的字符串
def tokenize(chars):
    "将字符串转换成由token组成的列表。"
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


# 语法分析-组合成语法树（列表）
def parse(program):
    "从字符串中读取Scheme表达式"
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    "从一串token之中读取表达式"
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "数字转为对应的Python数字，其余的转为符号"
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

Symbol = str          # Scheme符号由Python str表示
List   = list         # Scheme列表由Python list表示
Number = (int, float) # Scheme数字由Python的整数或浮点数表示


#设置环境
import math
import operator as op

Env = dict          # 环境是{变量: 值}之间的映射

def standard_env():
    "一个包含着一些Scheme标准过程的环境。"
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.div,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'abs':     abs,
        'append':  op.add,
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:],
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_,
        'equal?':  op.eq,
        'length':  len,
        'list':    lambda *x: list(x),
        'list?':   lambda x: isinstance(x,list),
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()


#语义分析-eval过程--评估表达式进行应用
def eval(x, env=global_env):
    "对在某个环境下的表达式进行求值"
    if isinstance(x, Symbol):      # 变量引用
        return env[x]
    elif not isinstance(x, List):  # 字面常量
        return x
    elif x[0] == 'if':             # 条件
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # 定义
        (_, var, exp) = x
        env[var] = eval(exp, env)
    else:                          # 过程调用
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

#驱动循环
def repl(prompt='lis.py> '):
    "REPL的懒人实现。"
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None:
            print(schemestr(val))

def schemestr(exp):
    "将一个Python对象转换回可以被Scheme读取的字符串。"
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)

#运行驱动循环
if __name__ == '__main__':
    repl()