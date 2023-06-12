import copy
from time import sleep
from Environment.Input.Input import Input
from Environment.SQL.SQL import SQL
from .SQL_Proxy_Worker import SQL_Proxy_Worker

class SQL_Filter_Worker:
    def __init__(self,db_type,log_file_path) -> None:
        assert(db_type is not None)
        assert(log_file_path is not None)
        self.db_type = db_type
        self.log_file_path = log_file_path

        self.sql_proxy = SQL_Proxy_Worker(self.log_file_path, self.db_type)
        pass

    def test_for_sql_statement(self,inputs):
        '''
            - send request with input token as payload
            - check logs for sql statement that has the token
            - filter inputs without sql statements
            - parse sql statements into generic form

            -- return: filtered_inputs, sql_statements
        '''
        filtered_inputs = []
        sql_statements = []
        for current_rep_input in inputs:

            # send request
            current_rep_input.send_token()

            # get all sql statements if exists
            current_sql_statements = self.sql_proxy.get_all_sql_statments(current_rep_input)



            if current_sql_statements is not None:
                for current_statment in current_sql_statements:
                    current_clone_input = copy.deepcopy(current_rep_input)
                    current_clone_input.seen_responce += 1

                    # construct sql object with input token


                    sql = SQL(current_statment,current_clone_input.token)
                    current_clone_input.sql_starting_stmt = sql.sql_starting_stmt

                    sql_statements.append(sql)
                    filtered_inputs.append(current_clone_input)

        return filtered_inputs,sql_statements
    
    def get_new_sql_statement(self,input_:Input):
        # get sql statement if exists
        sql_statement = self.sql_proxy.get_new_sql(input_)

        if sql_statement is not None:
            input_.seen_responce += 1
            # create sql object
            return SQL(sql_statement,input_.token)
        else:
            return None