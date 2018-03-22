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
                    print("{0}:{1}:{2}: warning: {3}".format(
                        token.file, token.line, token.column, token.message), file=sys.stderr)
                else:
                    outfile.write(token.value)

if __name__ == "__main__":
    main()
