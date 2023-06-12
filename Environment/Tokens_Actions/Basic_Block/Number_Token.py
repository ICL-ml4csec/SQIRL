from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.String_Token import String_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class Number_Token(Token):
    def __init__(self,num) -> None:
        super().__init__()
        self.token_list = [Whitespace_Token(0),NumberRepresentation_Token(num),Whitespace_Token(0)]

    def type(self):
        return "String Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
    
    def parse(num):
        assert(Number_Token.is_valid_number(num))
        return Number_Token(float(num))
        
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)