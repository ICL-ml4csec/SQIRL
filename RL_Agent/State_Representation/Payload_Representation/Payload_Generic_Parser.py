from Environment.Payload.Payload import Payload


import copy
from Environment.Tokens_Actions.Basic_Block.HexRepresentation_Token import HexRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.IdentifierRepresentation_Token import IdentifierRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Identifier_Token import Identifier_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token

from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
class Payload_Generic_Parser:
    def __init__(self) -> None:
        pass

    def convert_generic(self,payload:Payload):
        result = copy.deepcopy(payload)
        for current_token in result.base_token.flat_idx_tokens_list():
            if isinstance(current_token,StringRepresentation_Token):
                current_token.set_value("str")
            elif isinstance(current_token,OperatorRepresentation_Token):
                current_token.set_value("op")
            elif isinstance(current_token,NumberRepresentation_Token):
                current_token.set_value("num")
            elif isinstance(current_token,HexRepresentation_Token):
                current_token.set_value("hex")
            elif isinstance(current_token,IdentifierRepresentation_Token):
                current_token.set_value("id")

        return result
        