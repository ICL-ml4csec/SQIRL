


from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token


class CommentRange_Token(Token):
    comment_range_type_to_comment_type_mapping = {0:[2,3]}
    def __init__(self,commented_part_tokens,type) -> None:
        super().__init__()
        assert(isinstance(commented_part_tokens,list))
        assert(all([isinstance(current_token,Token) for current_token in commented_part_tokens]))
        assert(type in CommentRange_Token.comment_range_type_to_comment_type_mapping.keys())
        self.commented_part_tokens = commented_part_tokens
        self.token_list = [Comment_Token(CommentRange_Token.comment_range_type_to_comment_type_mapping[type][0])]
        self.token_list.extend(commented_part_tokens)
        self.token_list.extend([Comment_Token(CommentRange_Token.comment_range_type_to_comment_type_mapping[type][1])])
        

    def type(self):
        return "Comment Range Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
    
    def parse(comment_list:list):
        return CommentRange_Token(comment_list,0)