

from Environment.Tokens_Actions.Basic_Block.IdentifierRepresentation_Token import IdentifierRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token


class Identifier_Token(Token):
    def __init__(self,identifier,quote_type) -> None:
        super().__init__()
        self.token_list = [Quote_Token(quote_type),IdentifierRepresentation_Token(identifier),Quote_Token(quote_type)]
    

    def type(self):
        return "Identifier Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def parse(identifier,quote:Quote_Token):
        return Identifier_Token(str(identifier),quote.type_value())