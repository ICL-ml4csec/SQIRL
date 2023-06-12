

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.TokenUtil import TokenUtil


class UNION_Token(Token):
    def __init__(self) -> None:
        super().__init__()
        UNION_keyword = KeywordRepresentation_Token("UNION")
        statement = TokenUtil.generate_random_statement()        
        self.token_list = [Whitespace_Token(0),UNION_keyword,Whitespace_Token(0),statement]

    def type(self):
        return "UNION Token"
    def category(self):
        return Token.Category.BEHAVIOR_CHANGING