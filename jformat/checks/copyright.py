from datetime import datetime
from enum import Enum
from typing import IO, Union, Iterable, Dict
import re

from .. import FormatWarning, Languages, language, Token
from ..languages.cpp import ctokenizer, CppTokens

@language([Languages.C, Languages.Cpp])
class CopyrightCheck:

    _commentStart = [CppTokens.LineCommentStart, CppTokens.BlockCommentStart]
    _commentFormat = "/* {0} - (c) {1} {2} */\n"
    _commentRegex = re.compile("\\s")

    def __init__(self, language : Languages, options : Dict[str, str] = { }):
        self._curfile = None
        self._opts = { "year": datetime.now().year, "author": "James Renwick" }
        self._opts.update(options)

    def checkTokens(self, tokens : Iterable[Token]):
        for token in tokens:
            if token.file != self._curfile:
                self._curfile = token.file
                if token.value not in self._commentStart:
                    yield FormatWarning(token.file, token.line, token.column, "Missing copyright specifier.")
                    yield Token(token.file, token.line, token.column, False, str.format(
                        self._commentFormat, token.file, self._opts["year"], self._opts["author"]
                    ))
            yield token

    def checkStream(self, filename : str, file_in : IO[str], file_out : IO[str]):
        pass
