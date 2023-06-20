from Environment.Payload.Payload import Payload
from RL_Agent.State_Representation.Payload_Representation.model.Payload_Decoder import Payload_Decoder
from RL_Agent.State_Representation.Payload_Representation.model.Payload_Encoder import Payload_Encoder
from RL_Agent.State_Representation.Payload_Representation.Payload_Generic_Parser import Payload_Generic_Parser

import os
import torch
class Payload_Representation:
    tokens_embedding = [""," ","num","op","str","hex","id","if","and","or","sleep","union","where",",","-- ","#","/*","*/","(",")","\"","\'","`","/**/","char","concat","=","select","begin","end","else","sos","eos"]
    token_to_idx = {c:i for i,c in enumerate(tokens_embedding)}
    idx_to_token = {i:c for i,c in enumerate(tokens_embedding)}
    
    def __init__(self,input_size,output_size,hidden_size,max_length,acc_threshold=0.80) -> None:
        self.encoder = Payload_Encoder(input_size,hidden_size,max_length)
        self.decoder = Payload_Decoder(hidden_size,output_size,max_length)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


        # load trained weights
        self.encoder = torch.load(os.path.join("RL_Agent","State_Representation","Payload_Representation","model","encoder.model"),map_location=self.device)
        self.decoder = torch.load(os.path.join("RL_Agent","State_Representation","Payload_Representation","model","decoder.model"),map_location=self.device)

        self.generic_parser = Payload_Generic_Parser()
        self.acc_threshold = acc_threshold
        pass

    def payload_embedding(payload:Payload):
        # convert generic to embedding
        result = []
        tokens = payload.base_token.flat_idx_tokens_list()
        for current_token in tokens:
            result.append(Payload_Representation.token_to_idx[str(current_token).casefold()])
        
        return result

    def generate_representation(self,payload:Payload):
        # convert sql to generic and trim
        generic_sql = self.generic_parser.convert_generic(payload)

        # embed data 
        embedded_data = Payload_Representation.payload_embedding(generic_sql)
        # convert to tensor input
        tensored_input = torch.tensor(embedded_data, dtype=torch.long, device=self.device).view(-1, 1)

        # get length of input 
        input_length = tensored_input.size(0)

        # encode
        output, hidden = self.encoder.encode(tensored_input,input_length)

        return list(hidden.view(-1).detach().numpy())