

from Environment.Tokens_Actions.Basic_Block.Token import Token


class NumberRepresentation_Token(Token):
    def __init__(self,number) -> None:
        super().__init__()
        self.__number = number
        
    def value(self):
        return self.__number

    def set_value(self,new_value):
        self.__number = new_value

    def type(self):
        return "Number Representation Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
        
    def __str__(self) -> str:
        return str(self.__number)

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    def parse(s:str):
        assert(NumberRepresentation_Token.is_number(s))
        return NumberRepresentation_Token(float(s))
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)