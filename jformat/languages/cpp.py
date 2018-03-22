from jformat import Token
from enum import Enum

class CppTokens(Enum):
    Other = 0
    Identifier = 1
    Whitespace = 2
    LineComment = 3
    BlockComment = 4
    CharLiteral = 5
    StringLiteral = 6
    IntLiteral = 7
    PPDirective = 8
    Syntax = 9

CTokens = CppTokens

__csymbols = ['!','/','~',',','.','<','>','=','-','+',';',':','%','&','|','*','(',')','{','}','[',']','?','\\']

def ctokenizer(filename, file):
    inString = False
    inChar = False
    inPPD = False
    inLineComment = False
    inBlockComment = False
    inWhitespace = False
    inEscape = False

    line = 1
    column = 1

    b = None
    c = file.read(1)
    value = ""
    ttype = None

    while True:
        consumeChar = True
        yieldToken = False
        id = str.isalnum(c) or c == '_'
        sp = str.isspace(c)

        if c == '':
            if ttype is not None:
                yieldToken = True

        if inString or inChar:
            if c == '\\':
                inEscape = not inEscape
            elif inString and not inEscape and c == '"':
                inString = False
                yieldToken = True
            elif inChar and not inEscape and c == "'":
                inChar = False
                yieldToken = True

        elif inPPD:
            if not id:
                consumeChar = False
                yieldToken = True
                inPPD = False

        elif inLineComment:
            if c == '\n':
                consumeChar = False
                yieldToken = True
                inLineComment = False

        elif inBlockComment:
            if b == '*' and c == '/':
                yieldToken = True
                inBlockComment = False

        elif inWhitespace:
            if not sp:
                yieldToken = True
                consumeChar = False
                inWhitespace = False

        else:
            if ttype == CppTokens.BlockComment:
                if c == '*':
                    inBlockComment = True
                elif c == '/':
                    inLineComment = True
                else:
                    yield Token(filename, line, column - 1, CppTokens.Syntax, b)
                    consumeChar = False
                    ttype = None
                    value = str()

            elif ttype == CppTokens.IntLiteral:
                if not str.isdecimal(c):
                    if b != '0' or c not in ['x', 'b']:
                        consumeChar = False
                        yieldToken = True

            elif ttype == CppTokens.Identifier:
                if not id:
                    yieldToken = True
                    consumeChar = False

            elif ttype is None:
                if sp:
                    inWhitespace = True
                    ttype = CppTokens.Whitespace
                elif c == '#':
                    inPPD = True
                    ttype = CppTokens.PPDirective
                elif c == '/':
                    ttype = CppTokens.BlockComment
                elif c == "'":
                    ttype = CppTokens.CharLiteral
                    inChar = True
                elif c == '"':
                    ttype = CppTokens.StringLiteral
                    inString = True
                elif str.isdecimal(c):
                    ttype = CppTokens.IntLiteral
                elif id:
                    ttype = CppTokens.Identifier
                elif c in __csymbols:
                    ttype = CppTokens.Syntax
                    yieldToken = True
                else:
                    ttype = CppTokens.Other
                    yieldToken = True

        if consumeChar:
            value +=c

        if yieldToken:
            yield Token(filename, line, column, ttype, value)
            value = str()
            ttype = None

        if c == '':
            break

        if consumeChar:
            b = c
            c = file.read(1)

            if c == '\n':
                column = 1
                line += 1
            else:
                column += 1
