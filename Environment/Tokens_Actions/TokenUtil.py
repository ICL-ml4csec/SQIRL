import random
import copy
from Environment.Tokens_Actions.Basic_Block.Condition_Token import Condition_Token

from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Statement_Token import Statement_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.Behavior_Changing.SLEEP_Token import SLEEP_Token
statement_list =[
                    [KeywordRepresentation_Token("SELECT"),Whitespace_Token(0),StringRepresentation_Token("table_name"),Whitespace_Token(0),KeywordRepresentation_Token("FROM"),Whitespace_Token(0),StringRepresentation_Token("information_schema.tables")],
                ]
class TokenUtil:

    def generate_random_condition():
        '''
            generate condition true or false randomly
        '''
        return SLEEP_Token(0)


    

    def generate_random_statement():
        '''
            generate Statement from set of predefined statements structure
        '''
        statement = random.choice(statement_list)
        
        statement_token = Statement_Token(copy.deepcopy(statement))

        return statement_token
        pass