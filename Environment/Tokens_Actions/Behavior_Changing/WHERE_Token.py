

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.TokenUtil import TokenUtil


class WHERE_Token(Token):
    def __init__(self) -> None:
        super().__init__()
        WHERE_keyword = KeywordRepresentation_Token("WHERE")
        condition = TokenUtil.generate_random_condition()
        self.token_list = [Whitespace_Token(0),WHERE_keyword,Whitespace_Token(0),condition]

    def type(self):
        return "WHERE Token"
        
    def category(self):
        return Token.Category.BEHAVIOR_CHANGING