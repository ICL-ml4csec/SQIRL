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
import os
import torch
import itertools
class SQL_Representation:
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
    # starting and ending token
    start_end_token = ["sos","eos"]
    tokens_embedding = [*keywords, *operators, *comma, *comments, *hex, *string, *id, *number, *paranthesis, *quotes, *whitespace, *start_end_token]
    token_to_idx = {c:i for i,c in enumerate(tokens_embedding)}
    idx_to_token = {i:c for i,c in enumerate(tokens_embedding)}

    def __init__(self,db_type, input_size,output_size,hidden_size,max_length,acc_threshold=0.80) -> None:
        self.encoder = SQL_Encoder(input_size,hidden_size,max_length)
        self.decoder = SQL_Decoder(hidden_size,output_size,max_length)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # load trained models
        self.encoder = torch.load(os.path.join("RL_Agent","State_Representation","Generic_Syntax_State_Representation","model","encoder.model"),map_location=self.device)
        self.decoder = torch.load(os.path.join("RL_Agent","State_Representation","Generic_Syntax_State_Representation","model","decoder.model"),map_location=self.device)

        self.acc_threshold = acc_threshold
        pass

    def embedding(sql:SQL):
        result = []
        
        for current_token in sql.get_tokens().flat_idx_tokens_list():
            result.append(SQL_Representation.token_to_idx[str(current_token).casefold()])
        return result


    def generate_representation(self,sql:SQL,token:str,type=2):

        # convert sql to generic and trim
        generic_sql = sql.get_generic_statment()

        # embbed data 
        embedded_data = SQL_Representation.embedding(generic_sql)


        # convert to tensor input
        tensored_input = torch.tensor(embedded_data, dtype=torch.long, device=self.device).view(-1, 1)

        # get length of input 
        input_length = tensored_input.size(0)

        # encode
        output, hidden = self.encoder.encode(tensored_input,input_length)


        
        # # decoder input
        # decoder_input = torch.tensor([[SQL_Representation.token_to_idx["SOS".casefold()]]], device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        # # decode to evaluate error
        # decoder_output = self.decoder.decode(decoder_input,output,hidden,input_length)
        # # get number of wrong index
        # acc = 0
        # for current_output_idx in range(len(decoder_output)):
        #     if SQL_Representation.idx_to_token[embedded_data[current_output_idx]] == SQL_Representation.idx_to_token[decoder_output[current_output_idx]]:
        #         acc += 1
        # acc = float(acc)/float(input_length)

        features = list(hidden.view(-1).detach().numpy())
        return features