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
    PPDirective = 7
    Syntax = 8

CTokens = CppTokens

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
    ttype = CppTokens.Other

    while True:
        if c == '': break

        consumeChar = True
        yieldToken = False
        id = str.isalnum(c) or c == '_'
        sp = str.isspace(c)

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
                else:
                    yield Token(filename, line, column - 1, CppTokens.Syntax, b)
                    consumeChar = False
            elif ttype == CppTokens.LineComment:
                if c == '/':
                    inLineComment = True
                else:
                    yield Token(filename, line, column - 1, CppTokens.Syntax, b)
                    consumeChar = False
            if id:
                ttype = CppTokens.Identifier
            elif ttype == CppTokens.Identifier:
                yieldToken = True
                consumeChar = False


        if consumeChar:
            value +=c

        if yieldToken:
            yield Token(filename, line, column, ttype, value)
            value = str()
            ttype = CppTokens.Other

        if consumeChar:
            b = c
            c = file.read(1)

            if c == '\n':
                column = 1
                line += 1
            else:
                column += 1


    # yield Token(filename, 1, 1, CppTokens.Whitespace, "  ")
    # yield Token(filename, 1, 3, CppTokens.Other, "int")
    # yield Token(filename, 1, 6, CppTokens.Whitespace, " ")
    # yield Token(filename, 1, 7, CppTokens.Other, "main")
    # yield Token(filename, 1, 11, CppTokens.LParen)
    # yield Token(filename, 1, 12, CppTokens.RParen)
    # yield Token(filename, 1, 13, CppTokens.Whitespace, " ")
    # yield Token(filename, 1, 14, CppTokens.LBrace)
    # yield Token(filename, 1, 15, CppTokens.Whitespace, "\n")
    # yield Token(filename, 1, 16, CppTokens.Whitespace, "    ")
    # yield Token(filename, 1, 20, CppTokens.Return)
    # yield Token(filename, 1, 26, CppTokens.Whitespace, " ")
    # yield Token(filename, 1, 27, CppTokens.Other, "0")
    # yield Token(filename, 1, 28, CppTokens.Semicolon)
    # yield Token(filename, 1, 29, CppTokens.RBrace)
