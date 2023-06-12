
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token

class Statement_Token(Token):
    def __init__(self,tokens) -> None:
        super().__init__()
        self.token_list = tokens
        
    def type(self):
        return "Statement Token"
        
    def category(self):
        return Token.Category.BASIC_BLOCK
    def change_whitespace_type(self,type):
        for current_token in self.token_list:
            if isinstance(current_token,Whitespace_Token):
                current_token.change_type(type)
            elif isinstance(current_token, Token):
                current_token.change_whitespace_type(type)