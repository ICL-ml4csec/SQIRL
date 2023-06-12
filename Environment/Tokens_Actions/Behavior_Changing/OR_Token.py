

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.TokenUtil import TokenUtil


class OR_Token(Token):
    def __init__(self) -> None:
        super().__init__()
        OR_keyword = KeywordRepresentation_Token("OR")
        condition = TokenUtil.generate_random_condition()
        self.token_list = [Whitespace_Token(0),OR_keyword,Whitespace_Token(0),condition]

    def type(self):
        return "OR Token"
    def category(self):
        return Token.Category.BEHAVIOR_CHANGING