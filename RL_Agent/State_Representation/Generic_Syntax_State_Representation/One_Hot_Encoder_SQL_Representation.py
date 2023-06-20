from Environment.Tokens_Actions.Basic_Block.Comma_Token import Comma_Token
from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Token
from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.SQL_Generic_Parser import SQL_Generic_Parser
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.model.SQL_Encoder import SQL_Encoder
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.model.SQL_Decoder import SQL_Decoder
from Environment.SQL.SQL import SQL
import itertools

import os
import torch
import itertools
class One_Hot_Encoder_SQL_Representation:
    # get all different possible tokens and join them
    # keywords
    keywords = KeywordRepresentation_Token.reserved_keywords
    # operators
    operators = ["op"]
    # comma
    comma = Comma_Token.comma_types
    # comment
    comments = list(Comment_Token.comment_type_mapping.values())
    # hex
    hex = ["hex"]
    # string
    string= ["str"]
    # id
    id = ["id"]
    # number
    number = ["num"]
    # paranthesis
    paranthesis = list(Paranthesis_Token.paranthesis_type_mapping.values())
    # quotes
    quotes = list(Quote_Token.quote_type_mapping.values())
    # whitespace
    whitespace = list(Whitespace_Token.whitespace_type_mapping.values())
    empty_space = [""]
    # starting and ending token
    start_end_token = ["sos","eos"]
    tokens_embedding = [*keywords, *operators, *comma, *comments, *hex, *string, *id, *number, *paranthesis, *quotes, *whitespace, *start_end_token,*empty_space]
    token_to_idx = {c:i for i,c in enumerate(tokens_embedding)}
    idx_to_token = {i:c for i,c in enumerate(tokens_embedding)}

    def __init__(self,max_length) -> None:
        self.max_length = max_length
        pass

    def embedding(sql:SQL):
        result = []
        
        for current_token in sql.get_tokens().flat_idx_tokens_list():
            result.append(One_Hot_Encoder_SQL_Representation.token_to_idx[str(current_token).casefold()])
        return result

    def one_hot_encode(current_embeding):
        '''
            returns a one hot encoding of the embedding
        '''
        # check embedding valid
        assert(One_Hot_Encoder_SQL_Representation.is_valid_embedding(current_embeding))
        # convert to one hot encode
        return [1 if current_hot_encode == current_embeding else 0 for current_hot_encode in range(len(One_Hot_Encoder_SQL_Representation.tokens_embedding))]
    
    def is_valid_embedding(embed):
        return True if embed >= 0 and embed < len(One_Hot_Encoder_SQL_Representation.tokens_embedding) else False

    def generate_representation(self,sql:SQL):

        # convert sql to generic and trim
        generic_sql = sql.get_generic_statment()


        # embed data 
        embedded_data = One_Hot_Encoder_SQL_Representation.embedding(generic_sql)



        # pad if needed
        for current_padd in range(len(embedded_data),self.max_length):
            embedded_data.append(One_Hot_Encoder_SQL_Representation.token_to_idx[""])

        # one hot encoder
        one_hot_encoded_data = [One_Hot_Encoder_SQL_Representation.one_hot_encode(current_embeding) for current_embeding in embedded_data]

        # flatten the list of features
        flatten_list = list(itertools.chain(*one_hot_encoded_data))


        return flatten_list