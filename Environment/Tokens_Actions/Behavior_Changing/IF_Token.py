


from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.TokenUtil import TokenUtil


class IF_Token(Token):
    def __init__(self) -> None:
        super().__init__()
        IF_keyword = KeywordRepresentation_Token("IF")
        para_1 = Paranthesis_Token(0)
        condition = TokenUtil.generate_random_condition()
        para_2= Paranthesis_Token(1)
        BEGIN_1 = KeywordRepresentation_Token("BEGIN")
        true_expresion = TokenUtil.generate_random_statement()
        END_1 = KeywordRepresentation_Token("END")
        ELSE_1 = KeywordRepresentation_Token("ELSE")
        BEGIN_2 = KeywordRepresentation_Token("BEGIN")
        false_expression = TokenUtil.generate_random_statement()
        END_2 = KeywordRepresentation_Token("END")
        self.token_list = [Whitespace_Token(0),IF_keyword,Whitespace_Token(0),para_1,condition,para_2,Whitespace_Token(0),BEGIN_1,Whitespace_Token(0),true_expresion,Whitespace_Token(0),END_1,Whitespace_Token(0),ELSE_1,Whitespace_Token(0),BEGIN_2,Whitespace_Token(0),false_expression,Whitespace_Token(0),END_2]

    def type(self):
        return "IF Token"
    def category(self):
        return Token.Category.BEHAVIOR_CHANGING
    