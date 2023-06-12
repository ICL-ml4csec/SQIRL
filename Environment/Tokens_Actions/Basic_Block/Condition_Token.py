


from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token


class Condition_Token(Token):
    def __init__(self,operand_1:Token,operand_2:Token,operator:OperatorRepresentation_Token) -> None:
        super().__init__()
        self.token_list = [operand_1,operator,operand_2]
        pass

    def type(self):
        return "Condition Token"
    def category(self):
        return Token.Category.BASIC_BLOCK