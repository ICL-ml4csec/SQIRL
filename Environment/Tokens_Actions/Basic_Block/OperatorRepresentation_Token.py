from Environment.Tokens_Actions.Basic_Block.Token import Token
import re

from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token

class OperatorRepresentation_Token(Token):
    special_operators = ["^-=","|*=",">=","<=","<>","+=","-=","*=","/=","%=","&=","||","+","-","*","/","%","&","|","^","=",">","<","."]
    def __init__(self,operator) -> None:
        super().__init__()
        assert(OperatorRepresentation_Token.is_operator(operator))
        self.__operator = operator
        
    def value(self):
        return self.__operator

    def set_value(self,new_value):
        assert(OperatorRepresentation_Token.is_operator(new_value))
        self.__operator = new_value

    def type(self):
        return "Operator Representation Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return str(self.__operator)
    
    def is_operator(s:str):
        return True if (s in OperatorRepresentation_Token.special_operators or s == "op") else False
    
    def parse(s:str):
        assert(OperatorRepresentation_Token.is_operator(s))
        return OperatorRepresentation_Token(s)
        
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)