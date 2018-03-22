import os
import sys

from typing import IO
from jformat.checks.copyright import CopyrightCheck
from jformat.languages.cpp import ctokenizer
from jformat import Languages, Token, FormatWarning

def main():
    checks = [CopyrightCheck(Languages.Cpp, { })]

    with open("output.c", "w") as outfile:
        with open("test.c") as infile:
            tokenIter = ctokenizer("test.c", infile)
            for check in checks:
                tokenIter = check.checkTokens(tokenIter)
            for token in tokenIter:
                if type(token) == FormatWarning:
                    print("warning: {0}:{1}: {2}".format(token.line, token.column, token.message))
                    print("  in file '{0}'".format(token.file))
                else:
                    outfile.write(token.value)

if __name__ == "__main__":
    main()
