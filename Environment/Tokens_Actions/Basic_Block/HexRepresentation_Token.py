

from Environment.Tokens_Actions.Basic_Block.Token import Token


class HexRepresentation_Token(Token):
    def __init__(self,hex:str) -> None:
        super().__init__()
        assert(HexRepresentation_Token.is_hex(hex))
        if hex.startswith("0x") or hex =="hex":
            self.__hex = hex
        else:

            self.__hex = "0x"+hex

    def value(self):
        return self.__hex

    def set_value(self,new_value):
        assert(HexRepresentation_Token.is_hex(new_value))
        self.__hex = new_value

    def type(self):
        return "Hex Representation Token"

    def category(self):
        return Token.Category.BASIC_BLOCK
        
    def __str__(self) -> str:
        return str(self.__hex)

    def is_hex(s:str):
        return True if (s.startswith("0x") or s == "hex") else False

    def parse(s:str):
        assert(HexRepresentation_Token.is_hex(s))
        return HexRepresentation_Token(s)