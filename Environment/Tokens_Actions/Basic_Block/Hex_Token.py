


from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token


class Hex_Token(Token):
    def __init__(self,string) -> None:
        super().__init__()
        assert(isinstance(string,str))
        string = StringRepresentation_Token(string)
        # concat
        HEX_keyword = KeywordRepresentation_Token("UNHEX")
        para_1 = Paranthesis_Token(0)
        para_2 = Paranthesis_Token(1)
        self.token_list = [HEX_keyword,para_1,string,para_2]
        
    def type(self):
        return f"HEX Token"
        
    def category(self):
        return Token.Category.SANATISATION_ESCAPING