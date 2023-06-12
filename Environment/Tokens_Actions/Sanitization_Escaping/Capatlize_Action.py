

from random import choice

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token

class Capatilize_Action:
    def captilize_keyword_randomly(keyword_representation_token: KeywordRepresentation_Token):
        keyword = keyword_representation_token.value()
        new_keyword = ''.join(choice((str.upper, str.lower))(c) for c in keyword)
        keyword_representation_token.change_keyword(new_keyword)

    