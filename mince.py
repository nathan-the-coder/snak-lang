#!/usr/bin/env python3
# type: ignore

import os
import sys
import time

modules = ["tk"]
debug = False

# returns the current character while skipping over comments
def Look():
    # comments are entered by # and exited by \n or \0
    global pc

    if source[pc] == '/' and source[pc+1] == '/':
        while source[pc] != '\n' and source[pc] != '\0':
            # scan over comments here
            pc += 1
    return source[pc]


# takes away and returns the current character
def Take():
    global pc
    c = Look()
    pc += 1
    return c


# returns whether a certain string could be taken starting at pc
def TakeString(word):
    global pc
    copypc = pc
    for c in word:
        if Take() != c:
            pc = copypc
            return False
    return True


# returns the next non-whitespace character
def Next():
    while Look() == ' ' or Look() == '\t' or Look() == '\n' or Look() == '\r':
        Take()
    return Look()


# eats white-spaces, returns whether a certain character could be eaten
def TakeNext(c):
    if Next() == c:
        Take()
        return True
    else:
        return False


# recognizers
def IsDigit(c): return (c >= '0' and c <= '9')
def IsAlpha(c): return ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'))
def IsAlNum(c): return (IsDigit(c) or IsAlpha(c))
def IsAddOp(c): return (c == '+' or c == '-')
def IsMulOp(c): return (c == '*' or c == '/')


def TakeNextAlNum():
    alnum = ""
    if IsAlpha(Next()):
        while IsAlNum(Look()):
            alnum += Take()
    return alnum

# --------------------------------------------------------------------------------------------------


def BooleanFactor(act):
    inv = TakeNext('!')
    e = Expression(act)
    b = e[1]
    Next()
    # a single mathexpression may also serve as a boolean factor
    if (e[0] == 'i'):
        if TakeString("=="):
            b = (b == MathExpression(act))
        elif TakeString("!="):
            b = (b != MathExpression(act))
        elif TakeString("<="):
            b = (b <= MathExpression(act))
        elif TakeString("<"):
            b = (b < MathExpression(act))
        elif TakeString(">="):
            b = (b >= MathExpression(act))
        elif TakeString(">"):
            b = (b > MathExpression(act))
    else:
        if TakeString("=="):
            b = (b == StringExpression(act))
        elif TakeString("!="):
            b = (b != StringExpression(act))
        else:
            b = (b != "")
    # always returns False if inactive
    return act[0] and (b != inv)


def BooleanTerm(act):
    b = BooleanFactor(act)
    while TakeString('and'):
        # logical and corresponds to multiplication
        b = b & BooleanFactor(act)
    return b


def BooleanExpression(act):
    b = BooleanTerm(act)
    while TakeString('or'):
        # logical or corresponds to addition
        b = b | BooleanTerm(act)
    return b


def MathFactor(act):
    m = 0
    if TakeNext('('):
        m = MathExpression(act)
        if not TakeNext(')'):
            Error("missing ')'")
    elif IsDigit(Next()):
        while IsDigit(Look()):
            m = 10 * m + ord(Take()) - ord('0')
    elif TakeString("val("):
        s = String(act)
        if act[0] and s.isdigit():
            m = int(s)
        if not TakeNext(')'):
            Error("missing ')'")
    else:
        ident = TakeNextAlNum()
        if ident not in variables or variables[ident][0] != 'i':
            Error("unknown variables")
        elif act[0]:
            m = variables[ident][1]
    return m


def MathTerm(act):
    m = MathFactor(act)
    while IsMulOp(Next()):
        c = Take()
        m2 = MathFactor(act)
        if c == '*':
            # multiplication
            m = m * m2
        else:
            # division
            m = m / m2
    return m


def MathExpression(act):
    # check for an optional leading sign
    c = Next()
    if IsAddOp(c):
        c = Take()
    m = MathTerm(act)
    if c == '-':
        m = -m
    while IsAddOp(Next()):
        c = Take()
        m2 = MathTerm(act)
        if c == '+':
            # addition
            m = m + m2
        else:
            # subtraction
            m = m - m2
    return m


def String(act):
    s = ""
    # is it a literal string?
    if TakeNext('\"'):
        while not TakeString("\""):
            if Look() == '\0':
                Error("unexpected EOF")
            if TakeString("\\n"):
                s += '\n'
            else:
                s += Take()
    else:
        ident = TakeNextAlNum()
        if ident in variables and variables[ident][0] == 's':
            s = variables[ident][1]
        else:
            Error("not a string")
    return s


def StringExpression(act):
    s = String(act)
    while TakeNext('+'):
        # string addition = concatenation
        s += String(act)
    return s


def Expression(act):
    global pc
    copypc = pc
    ident = TakeNextAlNum()
    # scan for identifier or "str"
    pc = copypc
    if(Next() == '\"' or (ident in variables and variables[ident][0] == 's')):
        return ('s', StringExpression(act))
    else:
        return ('i', MathExpression(act))


def DoWhile(act):
    global pc
    local = [act[0]]
    # save PC of the while statement
    pc_while = pc
    while BooleanExpression(local):
        Block(local)
        pc = pc_while
    # scan over inactive block and leave while
    Block([False])


def DoIfElse(act):
    b = BooleanExpression(act)
    if act[0] and b:
        # process if block?
        Block(act)
    else:
        Block([False])
    Next()
    if TakeString("elif"):
        if act[0] and not b:
            Block(act)
        elif not act[0] and b:
            Block([b])
        else:
            Block([False])
    Next()
    # process else block?
    if TakeString("else"):
        if act[0] and not b:
            Block(act)
        else:
            Block([False])


param_count = 0
def DoCallFun(act):
    global pc, param_count
    ident = TakeNextAlNum()
    if ident not in variables or variables[ident][0] != 'p':
        Error("unknown function")

    if param_count != 0:
        if TakeNext("("):
            arg1 = TakeNextAlNum()

            if TakeNext(":"):
                value = ""

                if IsDigit(source[pc]):
                    while IsDigit(source[pc]):
                        value += source[pc]
                        pc += 1
                    variables[arg1] = ('s', value)
                elif source[pc] == '"':
                    pc += 1
                    while source[pc] != '"':
                        value += source[pc]
                        pc += 1
                    pc+= 1

                    variables[arg1] = ('s', value)

    if TakeNext(",") and not TakeNext(')'):
            arg2 = TakeNextAlNum()

            if TakeNext(":"):
                value = ""

                if IsDigit(source[pc]):
                    while IsDigit(source[pc]):
                        value += source[pc]
                        pc += 1
                    variables[arg2] = ('s', value)
                elif source[pc] == '"':
                    pc += 1
                    while source[pc] != '"':
                        value += source[pc]
                        pc += 1
                    pc+= 1

                    variables[arg2] = ('s', value)

    if not TakeNext(")"):
        Error("missing ')'")

    ret = pc
    pc = variables[ident][1]
    Block(act)
    # execute block as a subroutine
    pc = ret

def DoImport(act):
    e = Expression(act)

    if e[1] in modules:
        variables['m'] = e



def DoFunDef():
    global pc, param_count

    ident = TakeNextAlNum()

    if ident == "":
        Error("missing function identifier")

    if TakeNext("("):
        param1 = TakeNextAlNum()
        if param1 != "":
            param_count += 1
            if TakeNext(":"):
                value = ""
                if IsDigit(source[pc]):
                    while IsDigit(source[pc]):
                        value += source[pc]
                        pc += 1
                    variables[param1] = ('s', value)
                elif source[pc] == '"':
                    pc += 1
                    while source[pc] != '"':
                        value += source[pc]
                        pc += 1
                    pc+= 1

                    variables[param1] = ('s', value)
            else:
                variables[param1] = ('s', '')

        if TakeNext(','):
            param2 = TakeNextAlNum()
            param_count += 1

            if TakeNext(":"):
                value = ""
                while len(source) < 0 and source[pc].isdigit():
                    value += source[pc]
                print(value)
                variables[param2] = ('s', Next())

            variables[param2] = ('s', '')

    if not TakeNext(")"):
        Error("missing ')'")


    variables[ident] = ('p', pc)
    Block([False])


def DoAssign(act):
    ident = TakeNextAlNum()

    if not TakeNext('=') or ident == "":
        Error("unknown statement")

    e = Expression(act)

    if e[1] == "false":
        return 1
    elif e[1] == "true":
        return 0


    if act[0] or ident not in variables:
        # assert initialization even if block is inactive
        variables[ident] = e


def DoReturn(act):
    ident = TakeNextAlNum()
    e = Expression(act)
    if act[0] or ident not in variables:
        variables[ident] = e


def DoRun(act):
    ident = TakeNextAlNum()

    e = Expression(act)

    os.system(e[1])

    if act[0] or ident not in variables:
        variables[ident] = e


def DoBreak(act):
    if act[0]:
        # switch off execution within enclosing loop (while, ...)
        act[0] = False


def DoPrint(act):
    # process comma-separated arguments
    while True:
        e = Expression(act)
        if act[0]:
            print(e[1], end="")
        if not TakeNext(','):
            return


def DoExit(act):
    e = Expression(act)
    exit(e[1])


def DoRead(act):
    ident = TakeNextAlNum()

    f1 = Expression(act)
    e = Expression(act)

    with open(f1[1], "r") as f:
        if e is not None:
            print(f.read(e[1]))
        else:
            print(f.read())

    if act[0] or ident not in variables:
        variables[ident] = e


def DoWrite(act):
    ident = TakeNextAlNum()

    e = Expression(act)
    fi = Expression(act)

    with open(e[1], "w+") as f:
        f.write(fi[1])

    if act[0] or ident not in variables:
        variables[ident] = e

def DoError(act):
    # process comma-separated arguments
    while True:
        e = Expression(act)
        line = str(source[:pc].count("\n"))
        if act[0]:
            print(f"mince: {sys.argv[1]}:{line}: {e[1]}")
            exit(1)
        # if not TakeNext(','):
        #     return

def DoIncrement(act):
    ident = TakeNextAlNum()
    print(ident)

    e = Expression(act)
    e2 = list(e)

    n= e2.pop()
    n += 1
    e2.append(n)
 
    if act[0] or ident not in variables:
        variables[ident] = (e[0], e[1])

def Statement(act):
    if debug:
        print(variables)
    if TakeString("echo"):
        DoPrint(act)
    elif TakeString("inc"):
        DoIncrement(act)
    elif TakeString("sh"):
        DoRun(act)
    elif TakeString("error"):
        DoError(act)
    elif TakeString("break"):
        DoBreak(act)
    elif TakeString("read"):
        DoRead(act)
    elif TakeString("write"):
        DoWrite(act)
    elif TakeString("if"):
        DoIfElse(act)
    elif TakeString("while"):
        DoWhile(act)
    elif TakeString("for"):
        DoFor(act)
    elif TakeString("call"):
        DoCallFun(act)
    elif TakeString("define"):
        DoFunDef()
    elif TakeString("use"):
        DoImport(act)
    else:
        DoAssign(act)


def Block(act):
    if TakeNext("{"):
        while not TakeNext("}"):
            Block(act)
    else:
        Statement(act)


def Program():
    act = [True]
    while Next() != '\0':
        Block(act)


def Error(text):
    s = source[:pc].rfind("\n") + 1
    e = source.find("\n", pc)
    print("[ERROR] " + text + " in line " +
          str(source[:pc].count("\n") + 1) +
          ": '" + source[s:pc] + "_" + source[pc:e] + "'\n")
    sys.exit(1)


# --------------------------------------------------------------------------------------------------


pc = 0
# program couter, identifier -> (type, value) lookup table
variables = {}
file = sys.argv[1]

if len(sys.argv) < 2:
    print("Usage: mince [options] [file]")
    print("No arguments provided!")
    exit(1)

if sys.argv[1].startswith("-"):
    if sys.argv[1].endswith('d'):
        file = sys.argv[2]
        debug = True
else:
    file = sys.argv[1]
try:
    f = open(file, 'r')

except FileNotFoundError:
    print("ERROR: Can't find source file \'" + sys.argv[1] + "\'.")
    sys.exit(1)


# append a null termination
source = f.read() + '\0'


f.close()

Program()
