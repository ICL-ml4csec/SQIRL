from Environment.Input.Input_Identifier import Input_Identifier
from Environment.SQL.SQL import SQL
from Environment.Tokens_Actions.Basic_Block.CommentRange_Token import CommentRange_Token
from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Token
from Environment.Tokens_Actions.Basic_Block.FullComment_Token import FullComment_Token
from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.String_Token import String_Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.Behavior_Changing.SLEEP_Token import SLEEP_Token
from Environment.Tokens_Actions.Sanitization_Escaping.CONCAT_Token import CONCAT_Token
from Environment.Tokens_Actions.Sanitization_Escaping.Capatlize_Action import Capatilize_Action
from Environment.Tokens_Actions.Sanitization_Escaping.Represerntation_Action import Representation_Action
from Environment.Tokens_Actions.Sanitization_Escaping.WhitespaceConverter_Action import WhitespaceConverter_Action
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.SQL_Representation import SQL_Representation
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.model.dataset.SQL_Generator import SQL_Generator
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.SQL_Generic_Parser import SQL_Generic_Parser
import random
import os
import pickle
import json

from RL_Agent.State_Representation.Payload_Representation.model.dataset.Payload_Generator import Payload_Generator
class Dataset_Generator:
    def __init__(self,db_type,file_path) -> None:
        self.tokenizor = Input_Identifier()
        self.gen = SQL_Generator(db_type)
        # self.generic_parser = SQL_Generic_Parser(SQL_Representation.operator,SQL_Representation.tokens_embedding_2)
        self.dataset_file = file_path
        self.payload_gen = Payload_Generator()

    def generate_syntax_dataset(self,size):
        real_stmt_path = os.path.join(self.dataset_file, 'full_synatx_statment.dataset')
        generic_stmt_path = os.path.join(self.dataset_file, 'generic_synatx_statment.dataset')

        real_stmt_file_path = open(real_stmt_path,"w+")
        generic_stmt_file_path = open(generic_stmt_path,"w+")
        generic_sqls = []
        for current_stmt_idx in range(size):
            current_stmt = self.gen.generate_mysql()
            sql = self.convert_SQL(current_stmt)
            payload = self.payload_gen.generate_payload()
            if random.randint(0,1):
                sql.replace_identifier_with_payload(payload)
            # self.add_comments(sql)
            # self.add_sleep(sql)
            # self.captilize_keywords(sql)
            # self.convert_str_representation(sql)
            # self.replace_whitespace_with_no_white_space(sql)
            real_stmt_file_path.write(str(sql) + "\n")
            generic_sql = sql.get_generic_statment()
            print(generic_sql)
            print([c.type() for c in generic_sql.get_tokens().flat_idx_tokens_list()])
            generic_sqls.append(generic_sql)
            print(SQL_Representation.embedding(generic_sql))
            print()

        with open(generic_stmt_path,"wb") as f:
            pickle.dump(generic_sqls, f,pickle.HIGHEST_PROTOCOL)


    def add_comments(self,sql:SQL):
        len_base_tokens = sql.get_tokens().base_idx_length()
        no_comments = random.randint(0,4)
        # add full comment
        for current_comment in range(no_comments):
            #get all possible comment tokens
            possible_locations = []
            for current_pos in range(1,len_base_tokens+1):
                possible_locations.append(current_pos)

            #pick one action
            picked_pos = random.choice(possible_locations)

            # pick type
            type = random.randint(0,3)
            
            #apply action
            comment_token = Comment_Token(type)

            sql.get_tokens().insert_token_base_idx(comment_token,picked_pos)

    def add_sleep(self,sql:SQL):
        # check if add or not
        if random.randint(0,1):
            # flat index length
            flat_idx_length = sql.get_tokens().flat_idx_length()
            possible_locations = []
            # get possible locations
            for current_pos in range(1,flat_idx_length+1):
                possible_locations.append(current_pos)

            # pick random pos
            pos = random.choice(possible_locations)
            # create sleep
            assert(sql.get_tokens().is_valid_append_base_idx(pos))
            time = 20
            sleep_token = SLEEP_Token(time)

            # get flat tokens
            flat_tokens = sleep_token.flat_idx_tokens_list()

            # insert into sql
            for current_Token in flat_tokens:
                sql.get_tokens().insert_token_base_idx(current_Token,pos)
                pos += 1

    def replace_whitespace_with_no_white_space(self,sql:SQL):
        # check if add or not
        if random.randint(0,1):
            # flat index length
            flat_idx_length = sql.get_tokens().flat_idx_length()
            possible_locations = []
            # get possible locations
            for current_pos in range(flat_idx_length):
                if isinstance(sql.get_tokens().get_token_flat_idx(current_pos),Whitespace_Token):
                    possible_locations.append(current_pos)
            # pick random pos
            pos = random.choice(possible_locations)
            # validate 
            assert(sql.get_tokens().is_valid_flat_idx(pos))
            assert(sql.get_tokens().is_whitespace_flat_idx(pos))

            # convert whitespace to non whitespace
            whitespace = sql.get_tokens().get_token_flat_idx(pos)  
            WhitespaceConverter_Action.convert_to_non_whitespace(whitespace)
    def captilize_keywords(self,sql:SQL):
        # check if add or not
        if random.randint(0,1):
            # flat index length
            flat_idx_length = sql.get_tokens().flat_idx_length()
            possible_locations = []
            # get possible locations
            for current_pos in range(flat_idx_length):
                if isinstance(sql.get_tokens().get_token_flat_idx(current_pos),KeywordRepresentation_Token):
                    possible_locations.append(current_pos)
            # pick random pos
            pos = random.choice(possible_locations)
            # validate
            assert(sql.get_tokens().is_valid_flat_idx(pos))
            assert(sql.get_tokens().is_keyword_flat_idx(pos))

            # capatilze randomly the keyword
            keyword = sql.get_tokens().get_token_flat_idx(pos)
            Capatilize_Action.captilize_keyword_randomly(keyword)

    def convert_str_representation(self,sql:SQL):
        # check if add or not
        rand = random.randint(0,3)
        if rand == 0:
            # flat index length
            flat_idx_length = sql.get_tokens().flat_idx_length()
            possible_locations = []
            # get possible locations
            for current_pos in range(flat_idx_length):
                if isinstance(sql.get_tokens().get_token_flat_idx(current_pos),StringRepresentation_Token):
                    possible_locations.append(current_pos)
            # pick random pos
            pos = random.choice(possible_locations)
            # validate 
            assert(sql.get_tokens().is_valid_flat_idx(pos-1))
            assert(sql.get_tokens().is_valid_flat_idx(pos))
            assert(sql.get_tokens().is_valid_flat_idx(pos+1))


            # convert str to char
            string = sql.get_tokens().get_token_flat_idx(pos)   
            token = Representation_Action.str_to_char(string)
            # remove quote before and after
            sql.get_tokens().remove_token_flat_idx(pos-1)
            sql.get_tokens().remove_token_flat_idx(pos)
            sql.get_tokens().replace_flat_idx(pos-1,token)
        elif rand == 1:
            # flat index length
            flat_idx_length = sql.get_tokens().flat_idx_length()
            possible_locations = []
            # get possible locations
            for current_pos in range(flat_idx_length):
                if isinstance(sql.get_tokens().get_token_flat_idx(current_pos),StringRepresentation_Token):
                    possible_locations.append(current_pos)
            # pick random pos
            pos = random.choice(possible_locations)
            # validate 
            assert(sql.get_tokens().is_valid_flat_idx(pos))
            assert(sql.get_tokens().is_string_flat_idx(pos))

            # convert str to hex
            string = sql.get_tokens().get_token_flat_idx(pos)    
            token = Representation_Action.str_to_hex(string)
            # remove quote before and after
            sql.get_tokens().remove_token_flat_idx(pos-1)
            sql.get_tokens().remove_token_flat_idx(pos)
            sql.get_tokens().replace_flat_idx(pos-1,token)
        elif rand == 2:
            # flat index length
            flat_idx_length = sql.get_tokens().flat_idx_length()
            possible_locations = []
            # get possible locations
            for current_pos in range(flat_idx_length):
                if isinstance(sql.get_tokens().get_token_flat_idx(current_pos),StringRepresentation_Token):
                    possible_locations.append(current_pos)
            # pick random pos
            pos = random.choice(possible_locations)
            # validate 
            assert(sql.get_tokens().is_valid_flat_idx(pos))
            assert(sql.get_tokens().is_string_flat_idx(pos))
            assert(CONCAT_Token.is_valid_type(0))

            # convert str to concat
            string = sql.get_tokens().get_token_flat_idx(pos)     
            string_value = string.value()
            string_length = (len(string_value)//2) - 1
            string_1 = string_value[0:string_length]
            string_2 = string_value[string_length:]
            quote_type = random.randint(0,len(Quote_Token.quote_type_mapping.keys())-1)
            token = CONCAT_Token(0,[String_Token(string_1,quote_type),String_Token(string_2,quote_type)])
            # remove quote before and after
            sql.get_tokens().remove_token_flat_idx(pos-1)
            sql.get_tokens().remove_token_flat_idx(pos)
            sql.get_tokens().replace_flat_idx(pos-1,token)

    def convert_SQL(self,statment):
        literals = ['\'','\"','`']
        result_literals = []
        for current_literal in literals:
            result_literals.extend(Dataset_Generator.find_parens(statment,current_literal))
        token = self.tokenizor.get_next_token()
        pos_token = random.choice(result_literals)
        assert(len(current_literal) > 0 )
        statment = "".join(statment[:pos_token[0]+1]) + str(token) + "".join(statment[pos_token[1]:])
        return SQL(statment, token)

    def find_parens(s,to_be_matched):
        toret = []
        pstack = []

        for i, c in enumerate(s):
            if c in to_be_matched:
                if len(pstack) == 0:
                    pstack.append(i)
                else:
                    toret.append([pstack.pop(), i])


        return toret