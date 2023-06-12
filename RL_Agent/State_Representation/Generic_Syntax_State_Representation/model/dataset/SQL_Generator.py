import random
from Environment.SQL.SQL import SQL
from RL_Agent.State_Representation.Generic_Syntax_State_Representation.model.dataset.MYSQL_Generator import MYSQL_Generator
class SQL_Generator:
    def __init__(self,db_type) -> None:
        self.db_type = db_type
        if db_type == "mysql":
            self.gen =  MYSQL_Generator()
        else:
            # defualt
            self.gen =  MYSQL_Generator()
        
    def generate_mysql(self):
        '''
            generate a mysql statment randomly from three choices
            - select
            - insert
            - update
        '''
        random_operation = random.randint(1,3)
        if random_operation == 1:
            query,_ = self.gen.select()
        elif random_operation == 2:
            query = self.gen.insert()
        else:
            query = self.gen.update()

        result = query.get_sql()
        # tweak some literals ' " `
        # randomly select som paranthesis matching and change them to one of the three types
        for current_type_literal in ["\'","\"","`"]:
            matchings = SQL_Generator.find_parens(result,current_type_literal)
            numb = random.randint(0,len(matchings))
            chosen_To_replace = random.choices(matchings,k=numb)
            choices = [random.choice(["\'","\"","`"]) for c in range(numb)]
            for current_replace_idx in range(len(chosen_To_replace)):
                first_oc = chosen_To_replace[current_replace_idx][0]
                sec_oc = chosen_To_replace[current_replace_idx][1]
                current_result = list(result)
                current_result[first_oc] = choices[current_replace_idx]
                current_result[sec_oc] = choices[current_replace_idx]
                result = ''.join(current_result)

        return result

    def find_parens(s,to_be_matched):
        toret = []
        pstack = []

        for i, c in enumerate(s):
            if c == to_be_matched:
                if len(pstack) == 0:
                    pstack.append(i)
                else:
                    toret.append([pstack.pop(), i])


        return toret