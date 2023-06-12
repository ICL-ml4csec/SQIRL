import torch
import torch.nn as nn
import torch.nn.functional as F

from RL_Agent.State_Representation.Generic_Syntax_State_Representation.One_Hot_Encoder_SQL_Representation import One_Hot_Encoder_SQL_Representation
from RL_Agent.State_Representation.Payload_Representation.One_Hot_Encoder_Payload_Representation import One_Hot_Encoder_Payload_Representation

class One_Hot_Encoder_State_Representation():
    sql_max_length = 41
    payload_max_length = 255
    def __init__(self,db_type) -> None:
        # static values of the models


        # init the representation of sql and payload
        self.sql_representation = One_Hot_Encoder_SQL_Representation(One_Hot_Encoder_State_Representation.sql_max_length)
        self.payload_representation = One_Hot_Encoder_Payload_Representation(One_Hot_Encoder_State_Representation.payload_max_length)

    
    def represent_state(self,payload:str,sql:str,token:str):
        '''
            encode both payload and sql into representable vectors
        '''
        # encode payload
        payload_vector = self.payload_representation.generate_representation(payload)

        # encode sql
        sql_vector = self.sql_representation.generate_representation(sql)

        # concatenate representation
        payload_vector.extend(sql_vector)

        return payload_vector

    def size():
        return (One_Hot_Encoder_State_Representation.sql_max_length * len(One_Hot_Encoder_SQL_Representation.tokens_embedding)) + (One_Hot_Encoder_State_Representation.payload_max_length * len(One_Hot_Encoder_Payload_Representation.tokens_embedding))
