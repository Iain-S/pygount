"""
Additional lexers for pygount that fill gaps left by :py:mod:`pygments`.
"""

import json
from itertools import chain

# Copyright (c) 2016-2024, Thomas Aglassinger.
# All rights reserved. Distributed under the BSD License.
import pygments.lexer
import pygments.lexers
import pygments.token
import pygments.util


class IdlLexer(pygments.lexers.JavaLexer):
    """
    Lexer for OMG Interface Definition Language (IDL) that simply uses the
    existing Java lexer to find comments. While this is useless for syntax
    highlighting it is good enough for counting lines.
    """

    name = "IDL"
    filenames = ["*.idl"]


class MinimalisticM4Lexer(pygments.lexer.RegexLexer):
    """
    Minimalistic lexer for m4 macro processor that can distinguish between
    comments and code. It does not recognize a redefined comment mark though.
    """

    name = "M4"
    tokens = {
        "root": [
            (r"(.*)(#.*\n)", pygments.lexer.bygroups(pygments.token.Text, pygments.token.Comment.Single)),
            (r".*\n", pygments.token.Text),
        ]
    }


class MinimalisticVBScriptLexer(pygments.lexer.RegexLexer):
    """
    Minimalistic lexer for VBScript that can distinguish between comments and
    code.
    """

    name = "VBScript"
    tokens = {"root": [(r"\s*'.*\n", pygments.token.Comment.Single), (r".*\n", pygments.token.Text)]}


class MinimalisticWebFocusLexer(pygments.lexer.RegexLexer):
    """
    Minimalistic lexer for WebFOCUS that can distinguish between comments and
    code.
    """

    name = "WebFOCUS"
    tokens = {"root": [(r"-\*.*\n", pygments.token.Comment.Single), (r".*\n", pygments.token.Text)]}


class PlainTextLexer(pygments.lexer.RegexLexer):
    """
    Simple lexer for plain text that treats every line with non white space
    characters as :py:data:`pygments.Token.Comment.Single` and only lines
    that are empty or contain only white space as
    :py:data:`pygments.Token.Text`.

    This way, plaint text files count as documentation.
    """

    name = "Text"
    tokens = {"root": [(r"\s*\n", pygments.token.Text), (r".+\n", pygments.token.Comment.Single)]}


class DynamicMixin:
    """
    Mixin class for lexers that need to see the text.
    """

    def peek(self, _text) -> None:
        """Peek at the text."""
        raise NotImplementedError


class JupyterLexer(pygments.lexer.Lexer, DynamicMixin):
    """
    Jupyter notebooks are stored in JSON format.
    """

    def __init__(self):
        self.language = None
        super().__init__()

    @property
    def name(self) -> str:
        """The name of the language used in the notebook."""
        # It is an error to call this property before calling get_tokens.
        assert self.language is not None
        return self.language

    def peek(self, text) -> None:
        from pygments.lexers import get_lexer_by_name

        self.json_dict = json.loads(text)
        # should we do a["metadata"]["kernelspec"]["language"]?
        self.language = "{}".format(self.json_dict["metadata"]["language_info"]["name"])
        self.lexer = get_lexer_by_name(self.language)

    def get_tokens(self, text, unfiltered=False):
        """Use a lexer appropriate for the language of the notebook."""
        from pygments.lexers.python import PythonLexer

        code = ""
        docs = ""
        for cell in self.json_dict["cells"]:
            source = "".join(cell["source"])
            if cell["cell_type"] == "code":
                code += source
            elif cell["cell_type"] == "markdown":
                docs += source

        code_tokens = PythonLexer().get_tokens(code)
        doc_tokens = PlainTextLexer().get_tokens(docs)
        return chain(code_tokens, doc_tokens)
