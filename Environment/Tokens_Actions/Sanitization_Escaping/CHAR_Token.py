


from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token


class CHAR_Token(Token):
    def __init__(self,number_representation_token) -> None:
        super().__init__()
        assert(isinstance(number_representation_token,NumberRepresentation_Token))
        # concat
        CHAR_keyword = KeywordRepresentation_Token("CHAR")
        para_1 = Paranthesis_Token(0)
        para_2 = Paranthesis_Token(1)
        self.token_list = [CHAR_keyword,para_1,number_representation_token,para_2]
        
    def type(self):
        return f"CHAR Token"
    def category(self):
        return Token.Category.SANATISATION_ESCAPING