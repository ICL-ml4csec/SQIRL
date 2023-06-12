
from enum import Enum

from Environment.Tokens_Actions.Basic_Block.Token import Token

class Comment_Category(Enum):
    Full_Comment = 0
    Open_Range_Comment = 1
    Close_Range_Comment = 2


class Comment_Token(Token):
    comment_type_mapping = {0:"#",1:"-- ",2:"/*",3:"*/"}
    comment_type_category = {0:Comment_Category.Full_Comment,1:Comment_Category.Full_Comment,2:Comment_Category.Open_Range_Comment,3:Comment_Category.Close_Range_Comment}

    def __init__(self,type) -> None:
        super().__init__()
        self.__type = type
        self.__comment_category = Comment_Token.comment_type_category[type]

    def value(self):
        return Comment_Token.comment_type_mapping[self.type_value()]

    def type(self):
        return f"Comment type {self.__type} Token"
    def type_value(self):
        return self.__type
    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return Comment_Token.comment_type_mapping[self.__type]
    
    def is_valid_type(type:int):
        return type in Comment_Token.comment_type_mapping.keys()
        
    def comment_category(self):
        return self.__comment_category

    def is_comment(s:str):
        return True if s in Comment_Token.comment_type_mapping.values() else False
    
    def parse(s:str):
        assert(Comment_Token.is_comment(s))
        type = list(Comment_Token.comment_type_mapping.keys())[list(Comment_Token.comment_type_mapping.values()).index(s)]
        return Comment_Token(type)