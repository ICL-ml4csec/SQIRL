

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class SLEEP_Token(Token):
    def __init__(self,time) -> None:
        super().__init__()
        SLEEP_keyword = KeywordRepresentation_Token("SLEEP")
        para_1 = Paranthesis_Token(0)
        time = NumberRepresentation_Token(time)
        para_2 = Paranthesis_Token(1)

        self.token_list = [Whitespace_Token(0),SLEEP_keyword,Whitespace_Token(0),para_1,time,para_2]

    def type(self):
        return "OR Token"
    def category(self):
        return Token.Category.BEHAVIOR_CHANGING
        
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)