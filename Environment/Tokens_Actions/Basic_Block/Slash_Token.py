
from Environment.Tokens_Actions.Basic_Block.Token import Token


class Slash_Token(Token):
    slash_types = ["\\"]
    def __init__(self) -> None:
        super().__init__()

    def value(self):
        return "\\"

    def type(self):
        return f"slash Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return "\\"

    def is_slash(s:str):
        return True if s in Slash_Token.slash_types else False

    def parse(s:str):
        assert(Slash_Token.is_slash(s))
        return Slash_Token()