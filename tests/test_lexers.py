"""
Tests for additional lexers for pygount.
"""
# Copyright (c) 2016-2024, Thomas Aglassinger.
# All rights reserved. Distributed under the BSD License.

from pygments.token import Token

import pygount.lexers


def test_can_lex_idl():
    lexer = pygount.lexers.IdlLexer()
    text = "\n".join(
        [
            "/* some",
            " * comment */",
            "module HelloApp {",
            "  interface Hello {",
            "    string sayHello(); // Be friendly!",
            "  };",
            "};",
        ]
    )
    text_tokens = list(lexer.get_tokens(text))
    assert text_tokens == [
        (Token.Comment.Multiline, "/* some\n * comment */"),
        (Token.Text.Whitespace, "\n"),
        (Token.Name, "module"),
        (Token.Text.Whitespace, " "),
        (Token.Name, "HelloApp"),
        (Token.Text.Whitespace, " "),
        (Token.Punctuation, "{"),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "  "),
        (Token.Keyword.Declaration, "interface"),
        (Token.Text, " "),
        (Token.Name.Class, "Hello"),
        (Token.Text.Whitespace, " "),
        (Token.Punctuation, "{"),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Name, "string"),
        (Token.Text.Whitespace, " "),
        (Token.Name.Function, "sayHello"),
        (Token.Punctuation, "("),
        (Token.Punctuation, ")"),
        (Token.Punctuation, ";"),
        (Token.Text.Whitespace, " "),
        (Token.Comment.Single, "// Be friendly!"),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "  "),
        (Token.Punctuation, "}"),
        (Token.Punctuation, ";"),
        (Token.Text.Whitespace, "\n"),
        (Token.Punctuation, "}"),
        (Token.Punctuation, ";"),
        (Token.Text.Whitespace, "\n"),
    ]


def test_can_lex_m4():
    lexer = pygount.lexers.MinimalisticM4Lexer()
    text = ""
    text += "#\n"
    text += "# comment\n"
    text += "define(FRUIT, apple) # Healthy stuff!\n"
    text += "Eat some FRUIT!"
    text_tokens = list(lexer.get_tokens(text))
    assert text_tokens == [
        (Token.Comment.Single, "#\n"),
        (Token.Comment.Single, "# comment\n"),
        (Token.Text, "define(FRUIT, apple) "),
        (Token.Comment.Single, "# Healthy stuff!\n"),
        (Token.Text, "Eat some FRUIT!\n"),
    ]


def test_can_lex_vbscript():
    lexer = pygount.lexers.MinimalisticVBScriptLexer()
    text = "".join(["' comment\n", 'WScript.Echo "hello world!"'])
    text_tokens = list(lexer.get_tokens(text))
    assert text_tokens == [
        (Token.Comment.Single, "' comment\n"),
        (Token.Text, 'WScript.Echo "hello world!"\n'),
    ]


def test_can_lex_webfocus():
    lexer = pygount.lexers.MinimalisticWebFocusLexer()
    text = "".join(["-*\n", "-* comment\n", "-set &some='text';\n", "table file some print * end;"])
    text_tokens = list(lexer.get_tokens(text))
    assert text_tokens == [
        (Token.Comment.Single, "-*\n"),
        (Token.Comment.Single, "-* comment\n"),
        (Token.Text, "-set &some='text';\n"),
        (Token.Text, "table file some print * end;\n"),
    ]


def test_can_lex_plain_text():
    lexer = pygount.lexers.PlainTextLexer()
    text = "".join(
        [
            "a\n",  # line with text
            "\n",  # empty line
            " \t \n",  # line containing only white space
            "  ",  # trailing while space line without newline character
        ]
    )
    text_tokens = list(lexer.get_tokens(text))
    assert text_tokens == [(Token.Comment.Single, "a\n"), (Token.Text, "\n \t \n  \n")]


def test_can_lex_notebook():
    lexer = pygount.lexers.JupyterLexer()
    # The most minimal notebook allowed by
    # https://github.com/jupyter/nbformat/blob/main/nbformat/v4/nbformat.v4.schema.json
    text = "".join(
        [
            "{",
            '    "metadata": {',
            "    },",
            '    "nbformat": 4,',
            '    "nbformat_minor": 5,',
            '    "cells": [',
            "    ]",
            "}",
        ]
    )
    text_tokens = list(lexer.get_tokens(text))
    assert text_tokens == [
        (Token.Punctuation, "{"),
        (Token.Text.Whitespace, "    "),
        (Token.Name.Tag, '"metadata"'),
        (Token.Punctuation, ":"),
        (Token.Text.Whitespace, " "),
        (Token.Punctuation, "{"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, "},"),
        (Token.Text.Whitespace, "    "),
        (Token.Name.Tag, '"nbformat"'),
        (Token.Punctuation, ":"),
        (Token.Text.Whitespace, " "),
        (Token.Literal.Number.Integer, "4"),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "    "),
        (Token.Name.Tag, '"nbformat_minor"'),
        (Token.Punctuation, ":"),
        (Token.Text.Whitespace, " "),
        (Token.Literal.Number.Integer, "5"),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "    "),
        (Token.Name.Tag, '"cells"'),
        (Token.Punctuation, ":"),
        (Token.Text.Whitespace, " "),
        (Token.Punctuation, "["),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, "]}"),
        (Token.Text.Whitespace, "\n"),
    ]
