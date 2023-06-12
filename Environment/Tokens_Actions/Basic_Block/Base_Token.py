
from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class Base_Token(Token):
    def __init__(self) -> None:
        super().__init__()
        pass

    def append_token_base_idx(self,token:Token):
        self.token_list.append(token)

    def insert_token_base_idx(self,token:Token,pos:int):
        assert(isinstance(token,Token))
        assert(self.is_valid_append_base_idx(pos))
        self.token_list.insert(pos,token)

    def remove_token_base_idx(self,pos:int):
        return self.token_list.pop(pos)

  
    def is_valid_append_base_idx(self,pos:int):
        return pos <= len(self.token_list) and pos >= 0 

    def is_valid_base_idx_range(self,pos_start:int,pos_end:int):
        return pos_start >= 0 and pos_end < len(self.token_list)

    def is_valid_append_base_idx_range(self,pos_start:int,pos_end:int):
        return pos_start >= 0 and pos_end <= len(self.token_list)
    
    def get_tokens_list_base_idx(self,pos_start:int,pos_end:int):
        assert(self.is_valid_append_base_idx_range(pos_start,pos_end))
        return self.token_list[pos_start:pos_end]
    
    def replace_range_tokens_base_idx(self,pos_start:int,pos_end:int,token:Token):
        assert(self.is_valid_append_base_idx_range(pos_start,pos_end))
        del self.token_list[pos_start:pos_end]
        self.token_list.insert(pos_start,token)

    def is_valid_flat_idx(self,pos:int):
        # flatten tokens lenght
        length = self.flat_idx_length()
        # check if valid idx
        return pos < length and pos >= 0

    def get_token_flat_idx(self,pos:int):
        assert(self.is_valid_flat_idx(pos))
        return self.flat_idx_tokens_list()[pos]

    def is_keyword_flat_idx(self,pos:int):
        assert(self.is_valid_flat_idx(pos))
        # get flat index tokens
        flat_idx_token = self.get_token_flat_idx(pos)
        return isinstance(flat_idx_token,KeywordRepresentation_Token)
    
    def is_string_flat_idx(self,pos:int):
        assert(self.is_valid_flat_idx(pos))
        # get flat index tokens
        flat_idx_token = self.get_token_flat_idx(pos)
        return isinstance(flat_idx_token,StringRepresentation_Token)

    def is_whitespace_flat_idx(self,pos:int):
        assert(self.is_valid_flat_idx(pos))
        # get flat index tokens
        flat_idx_token = self.get_token_flat_idx(pos)
        return isinstance(flat_idx_token,Whitespace_Token)

    def base_idx_length(self):
        return len(self.token_list)


    def type(self):
        return "Base Token"
    def category(self):
        return Token.Category.BASIC_BLOCK