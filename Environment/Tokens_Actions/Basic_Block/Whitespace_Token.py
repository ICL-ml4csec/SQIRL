
from Environment.Tokens_Actions.Basic_Block.Token import Token


class Whitespace_Token(Token):
    whitespace_type_mapping = {0:" ",1:"/**/"}

    def __init__(self,type) -> None:
        super().__init__()
        self.__type = type

    def value(self):
        return Whitespace_Token.whitespace_type_mapping[self.__type]

    def type(self):
        return f"whitespace type {self.__type} Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return Whitespace_Token.whitespace_type_mapping[self.__type]

    def change_type(self,new_type:int):
        assert(Whitespace_Token.is_valid_type(new_type))
        self.__type = new_type
        
    def type_value(self)->int:
        return self.__type

    def is_valid_type(type_query):
        return type_query in Whitespace_Token.whitespace_type_mapping

    def is_whitespace(s:str):
        return True if s in Whitespace_Token.whitespace_type_mapping.values() else False

    def parse(s:str):
        assert(Whitespace_Token.is_whitespace(s))
        type = list(Whitespace_Token.whitespace_type_mapping.keys())[list(Whitespace_Token.whitespace_type_mapping.values()).index(s)]
        return Whitespace_Token(type)