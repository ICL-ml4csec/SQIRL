
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class String_Token(Token):
    def __init__(self,string,quote_type) -> None:
        super().__init__()
        self.token_list = [Quote_Token(quote_type),StringRepresentation_Token(string),Quote_Token(quote_type)]

    def type(self):
        return "String Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
    
    def parse(quote_token_1:Quote_Token,string_token:StringRepresentation_Token,quote_token_2:Quote_Token):
        return String_Token(str(string_token),quote_token_1.type_value())
        
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)