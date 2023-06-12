

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.TokenUtil import TokenUtil

class AND_Token(Token):
    and_type_mapping = {0:"AND",1:"&"}

    def __init__(self,type=0) -> None:
        super().__init__()
        assert(AND_Token.is_valid_type(type))
        self.type = type
        if type == 0:
            AND_keyword = KeywordRepresentation_Token("AND")
            condition = TokenUtil.generate_random_condition()
            self.token_list = [Whitespace_Token(0),AND_keyword,Whitespace_Token(0),condition]
        elif type == 1:
            AND_keyword = OperatorRepresentation_Token("&")
            condition = TokenUtil.generate_random_condition()
            self.token_list = [Whitespace_Token(0),AND_keyword,Whitespace_Token(0),condition]
        else:
            raise Exception("AND token type not found ")

    def whitespace_type_value(self):
        return self.token_list[0].type_value()

    def type(self):
        return "AND Token"

    def type_value(self):
        return self.type
        
    def category(self):
        return Token.Category.BEHAVIOR_CHANGING
        
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)

    def is_valid_type(type):
        return True if type in AND_Token.and_type_mapping.keys() else False

    def change_type(self,type):
        assert(AND_Token.is_valid_type(type))
        if type == self.type:
            pass
        else:
            self.type = type
            if type == 0:
                AND_keyword = KeywordRepresentation_Token("AND")
                condition = TokenUtil.generate_random_condition()
                self.token_list = [Whitespace_Token(0),AND_keyword,Whitespace_Token(0),condition]
            elif type == 1:
                AND_keyword = OperatorRepresentation_Token("&")
                condition = TokenUtil.generate_random_condition()
                self.token_list = [Whitespace_Token(0),AND_keyword,Whitespace_Token(0),condition]
            else:
                raise Exception("AND token type not found ")



