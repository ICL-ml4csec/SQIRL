


from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token


class FullComment_Token(Token):

    def __init__(self,comment_type:int,commented_part_tokens:list) -> None:
        super().__init__()
        assert(isinstance(commented_part_tokens,list))
        assert(all([isinstance(current_token,Token) for current_token in commented_part_tokens]))
        assert(Comment_Token.is_valid_type(comment_type))
        
        self.commented_part_tokens = commented_part_tokens
        self.token_list = [Comment_Token(comment_type)]
        self.token_list.extend(commented_part_tokens)
        

    def type(self):
        return "Full Comment Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def parse(comment:Comment_Token,commented_list:list):
        return FullComment_Token(comment.type_value(),commented_list)