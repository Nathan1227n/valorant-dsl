from lark import Lark


def carregar_parser():
    """
    Carrega a gramática da ValorScript e cria o parser LALR.
    """
    with open("grammar.lark", "r", encoding="utf-8") as arquivo:
        grammar = arquivo.read()

    return Lark(grammar, parser="lalr")


def analisar_codigo(parser, codigo):
    """
    Analisa sintaticamente um código ValorScript.

    Retorna a árvore sintática.
    """
    return parser.parse(codigo)


def obter_tokens(parser, codigo):
    """
    Retorna os tokens reconhecidos pelo lexer.
    """
    return list(parser.lex(codigo))