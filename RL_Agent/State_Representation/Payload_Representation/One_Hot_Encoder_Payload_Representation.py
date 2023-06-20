import itertools
from Environment.Payload.Payload import Payload
from RL_Agent.State_Representation.Payload_Representation.model.Payload_Decoder import Payload_Decoder
from RL_Agent.State_Representation.Payload_Representation.model.Payload_Encoder import Payload_Encoder
from RL_Agent.State_Representation.Payload_Representation.Payload_Generic_Parser import Payload_Generic_Parser

import os
import torch
class One_Hot_Encoder_Payload_Representation:
    tokens_embedding = [""," ","num","op","str","hex","id","if","and","or","sleep","union","where",",","-- ","#","/*","*/","(",")","\"","\'","`","/**/","char","concat","=","select","begin","end","else","sos","eos"]
    token_to_idx = {c:i for i,c in enumerate(tokens_embedding)}
    idx_to_token = {i:c for i,c in enumerate(tokens_embedding)}
    
    def __init__(self,max_length) -> None:
        self.max_length = max_length
        self.generic_parser = Payload_Generic_Parser()
        pass

    def payload_embedding(payload:Payload):
        # convert generic to embedding
        result = []
        tokens = payload.base_token.flat_idx_tokens_list()
        for current_token in tokens:
            result.append(One_Hot_Encoder_Payload_Representation.token_to_idx[str(current_token).casefold()])
        
        return result

    def one_hot_encode(current_embeding):
        '''
            returns a one hot encoding of the embedding
        '''
        # check embedding valid
        assert(One_Hot_Encoder_Payload_Representation.is_valid_embedding(current_embeding))
        # convert to one hot encode
        return [1 if current_hot_encode == current_embeding else 0 for current_hot_encode in range(len(One_Hot_Encoder_Payload_Representation.tokens_embedding))]
    
    def is_valid_embedding(embed):
        return True if embed >= 0 and embed < len(One_Hot_Encoder_Payload_Representation.tokens_embedding) else False

    def generate_representation(self,payload:Payload):
        # convert sql to generic and trim
        generic_sql = self.generic_parser.convert_generic(payload)

        # embed data 
        embedded_data = One_Hot_Encoder_Payload_Representation.payload_embedding(generic_sql)
        

        # pad if needed
        for current_padd in range(len(embedded_data),self.max_length):
            embedded_data.append(One_Hot_Encoder_Payload_Representation.token_to_idx[""])

        # one hot encoder
        one_hot_encoded_data = [One_Hot_Encoder_Payload_Representation.one_hot_encode(current_embeding) for current_embeding in embedded_data]

        # flatten the list of features
        flatten_list = list(itertools.chain(*one_hot_encoded_data))

        return flatten_list