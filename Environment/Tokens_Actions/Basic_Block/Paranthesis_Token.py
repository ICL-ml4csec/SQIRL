
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class Paranthesis_Token(Token):
    paranthesis_type_mapping = {0:"(",1:")",2:"[",3:"]"}
    def __init__(self,type) -> None:
        super().__init__()
        self.__type = type
    
    def value(self):
        return Paranthesis_Token.paranthesis_type_mapping[self.__type]

    def type(self):
        return f"Parenthesis type {self.__type} Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
        
    def __str__(self) -> str:
        return Paranthesis_Token.paranthesis_type_mapping[self.__type]

    def is_valid_type(type_query:int):
        return type_query in Paranthesis_Token.paranthesis_type_mapping.keys()
    
    def is_paranthesis(s:str):
        return True if s in Paranthesis_Token.paranthesis_type_mapping.values() else False
    
    def parse(s:str):
        assert(Paranthesis_Token.is_paranthesis(s))
        type = list(Paranthesis_Token.paranthesis_type_mapping.keys())[list(Paranthesis_Token.paranthesis_type_mapping.values()).index(s)]
        return Paranthesis_Token(type)
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)