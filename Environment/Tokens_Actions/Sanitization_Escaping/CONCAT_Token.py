

from Environment.Tokens_Actions.Basic_Block.Comma_Token import Comma_Token
from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class CONCAT_Token(Token):
    concat_type_mapping = {0:"concat", 1 :"+", 2:"||"}
    def __init__(self,type,str) -> None:
        super().__init__()
        assert(all([isinstance(str_cur,Token)for str_cur in str]))
        assert(CONCAT_Token.is_valid_type(type))
        self.type = type
        if type == 0:
            # concat
            CONCAT_keyword = KeywordRepresentation_Token("CONCAT")
            para_1 = Paranthesis_Token(0)
            para_2 = Paranthesis_Token(1)
            self.token_list = [Whitespace_Token(0),CONCAT_keyword,para_1]
            
            for current_str in range(len(str)-1):
                self.token_list.extend([str[current_str],Comma_Token()])

            self.token_list.extend([str[-1],para_2])
        elif type == 1:
            # +
            for current_str in range(len(str)-1):
                self.token_list.extend([str[current_str],OperatorRepresentation_Token("+")])

            self.token_list.append(str[-1])
            
        elif type == 2:
            for current_str in range(len(str)-1):
                self.token_list.extend([str[current_str],OperatorRepresentation_Token("||")])

            self.token_list.append(str[-1])
        else:
            # defalt
            CONCAT_keyword = KeywordRepresentation_Token("CONCAT")
            para_1 = Paranthesis_Token(0)
            para_2 = Paranthesis_Token(1)
            self.token_list = [Whitespace_Token(0),CONCAT_keyword,para_1]
            
            for current_str in range(len(str)-1):
                self.token_list.extend([str[current_str],Comma_Token()])

            self.token_list.extend([str[-1],para_2])

    def type(self):
        return f"Comment type {self.type} Token"

    def category(self):
        return Token.Category.SANATISATION_ESCAPING
        
    def is_valid_type(type:int):
        return type in CONCAT_Token.concat_type_mapping.keys()
