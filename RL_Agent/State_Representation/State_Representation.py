import torch
import torch.nn as nn
import torch.nn.functional as F

from RL_Agent.State_Representation.Generic_Syntax_State_Representation.SQL_Representation import SQL_Representation
from RL_Agent.State_Representation.Payload_Representation.Payload_Representation import Payload_Representation
class State_Representation():
    hidden_size = 1024
    def __init__(self,db_type) -> None:
        # static values of the models
        self.sql_input_size = len(SQL_Representation.tokens_embedding)
        self.payload_input_size = len(Payload_Representation.tokens_embedding)
        self.sql_output_size = len(SQL_Representation.tokens_embedding)
        self.payload_output_size = len(Payload_Representation.tokens_embedding)
        self.sql_max_length = 41
        self.payload_max_length = 255

        # init the representation of sql and payload
        self.sql_representation = SQL_Representation(db_type,self.sql_input_size,self.sql_output_size,self.hidden_size,self.sql_max_length)
        self.payload_representation = Payload_Representation(self.payload_input_size,self.payload_output_size,self.hidden_size,self.payload_max_length)

    
    def represent_state(self,payload:str,sql:str,token:str):
        '''
            encode both payload and sql into representable vectors
        '''
        # encode payload
        payload_vector = self.payload_representation.generate_representation(payload)

        # encode sql
        sql_vector = self.sql_representation.generate_representation(sql,token)

        # concatenate representation
        payload_vector.extend(sql_vector)

        return payload_vector
    def size():
        return  State_Representation.hidden_size * 2