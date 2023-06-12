
from Environment.Tokens_Actions.Basic_Block.Token import Token


class Comma_Token(Token):
    comma_types = [",",";"]
    def __init__(self) -> None:
        super().__init__()

    def value(self):
        return ","

    def type(self):
        return f"Comma Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return ","

    def is_comma(s:str):
        return True if s in Comma_Token.comma_types else False

    def parse(s:str):
        assert(Comma_Token.is_comma(s))
        return Comma_Token()