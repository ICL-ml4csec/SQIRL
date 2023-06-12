from Environment.Tokens_Actions.Basic_Block.Token import Token



class Quote_Token(Token):
    quote_type_mapping = {0:"\'",1:"\"",2:"`"}
    def __init__(self,type) -> None:
        assert(Quote_Token.is_valid_type(type))
        super().__init__()
        self.__type = type
        self.__value = Quote_Token.quote_type_mapping[self.__type]
        

    def value(self):
        return self.__value 

    def type(self):
        return f"Quote type {self.__type} Token"

    def type_value(self):
        return self.__type
        
    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        return Quote_Token.quote_type_mapping[self.__type]

    def is_valid_type(type_query:int):
        return type_query in Quote_Token.quote_type_mapping.keys()

    def is_quote(s:str):
        return True if s in Quote_Token.quote_type_mapping.values() else False

    def add_null_byte(self):
        self.__value = "0x00"+Quote_Token.quote_type_mapping[self.__type]
        
    def has_null_byte(self):
        return True if self.__value.startswith("0x00") else False

    def parse(s:str):
        assert(Quote_Token.is_quote(s))
        type = list(Quote_Token.quote_type_mapping.keys())[list(Quote_Token.quote_type_mapping.values()).index(s)]

        return Quote_Token(type)