from Environment.Tokens_Actions.Basic_Block.Token import Token


class IdentifierRepresentation_Token(Token):
    def __init__(self,identifier) -> None:
        super().__init__()
        self.__identifier = identifier

    def value(self):
        return self.__identifier

    def set_value(self,new_value):
        self.__identifier = new_value

    def type(self):
        return "Identifier representation Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
        
    def __str__(self) -> str:
        return self.__identifier

    def parse(s:str):
        return IdentifierRepresentation_Token(s)