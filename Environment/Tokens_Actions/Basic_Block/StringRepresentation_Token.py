

from Environment.Tokens_Actions.Basic_Block.Token import Token


class StringRepresentation_Token(Token):
    def __init__(self,string) -> None:
        super().__init__()
        self.__string = string

    def value(self):
        return self.__string

    def set_value(self,new_value):
        self.__string = new_value

    def type(self):
        return "String Representation Token"
        
    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return self.__string

    def parse(s:str):
        return StringRepresentation_Token(s)
    