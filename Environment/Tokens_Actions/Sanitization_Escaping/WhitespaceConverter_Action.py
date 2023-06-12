

from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token


class WhitespaceConverter_Action:
    def convert_to_non_whitespace(whitespace_token:Whitespace_Token):
        whitespace_token.change_type(1)