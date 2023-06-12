


from Environment.Tokens_Actions.Basic_Block.Hex_Token import Hex_Token
from Environment.Tokens_Actions.Basic_Block.HexRepresentation_Token import HexRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Sanitization_Escaping.CHAR_Token import CHAR_Token
from Environment.Tokens_Actions.Sanitization_Escaping.CONCAT_Token import CONCAT_Token


class Representation_Action:
    def str_to_char(string_token:Token,type=0):
        string = string_token.value()
        if len(string) > 1:
            char_list = []
            for current_char in string:
                char_list.append(CHAR_Token(NumberRepresentation_Token(ord(current_char))))
            concat = CONCAT_Token(type,char_list)
            return concat
        else:
            if len(string) == 0:
                return CHAR_Token(NumberRepresentation_Token(0))
 
            return CHAR_Token(NumberRepresentation_Token(ord(string)))
        

    def str_to_hex(string_token:Token):
        string = string_token.value()
        return Hex_Token("0x" + string.encode("utf-8").hex())
 
    