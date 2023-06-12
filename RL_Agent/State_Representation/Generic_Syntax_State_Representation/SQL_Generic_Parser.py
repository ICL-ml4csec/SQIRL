from sql_metadata import Parser
import re
class SQL_Generic_Parser:
    def __init__(self,operators, reserved_keywords) -> None:
        self.operators = operators
        self.reserved_keywords = reserved_keywords
        self.generic_parser = Parser
        pass

    def parse(self,sql_stmt):
        return self.generic_parser(sql_stmt)



    def convert_generic(self,sql_stmt,token):
        result_statment = []

        # convert literals to one type
        sql_stmt = sql_stmt.replace("\"","\'").replace("`","'")
        result = self.generic_parser(sql_stmt)

        for current_token in result.tokens:
            if current_token.is_name or current_token.is_float or current_token.is_integer or current_token.is_integer or current_token.is_wildcard or(current_token.value.startswith("\'") and current_token.value.endswith("\'")):
                if token in current_token.value:
                    result_statment.append("\'token\'")
                elif current_token.value.startswith("\""):
                    result_statment.append("\"xxxx\"")
                elif current_token.value.startswith("`"):
                    result_statment.append("`xxxx`")
                elif current_token.value.startswith("\'"):
                    result_statment.append("\'xxxx\'")
                else:

                    result_statment.append("xxxx")
            else:
                result_statment.append(current_token.value)
        return " ".join(result_statment)

    def convert_syntax_generic(self,sql_stmt,token):
        result_statment = []

        # convert literals to one type
        result = self.generic_parser(sql_stmt)

        token_index = 0
        for current_token in result.tokens:

                if token in current_token.value:
                    regex = r".*(" + re.escape(str(token)) + r").*"
                    match_obj = re.match(regex,sql_stmt)
                    starting_index = match_obj.span(1)[0]
                    ending_index =  match_obj.span(1)[1]
                    
                    if starting_index == 0:
                        result_statment.append([1,"token"])
                    elif sql_stmt[starting_index-1] == "\'":
                        result_statment.append([0,"\'"])
                        result_statment.append([1,"token"])
                        result_statment.append([0,"\'"])

                    elif sql_stmt[starting_index-1] == "\"":
                        result_statment.append([0,"\""])
                        result_statment.append([1,"token"])
                        result_statment.append([0,"\""])

                    elif sql_stmt[starting_index-1] == "'":
                        result_statment.append([0,"'"])
                        result_statment.append([1,"token"])
                        result_statment.append([0,"'"])

                    elif sql_stmt[starting_index-1] == "`":
                        result_statment.append([0,"`"])
                        result_statment.append([1,"token"])
                        result_statment.append([0,"`"])

                    else:
                        result_statment.append([1,"token"])
                elif current_token.is_punctuation or current_token.is_left_parenthesis or current_token.is_right_parenthesis:
                    result_statment.append([0,current_token.value])
                elif current_token.is_float or current_token.is_integer:
                    result_statment.append([0,"num"])
                elif  (current_token.value.startswith("\'") and current_token.value.endswith("\'")):
                        result_statment.append([0,"\'"])
                        result_statment.append([0,"str"])
                        result_statment.append([0,"\'"])
                else:
                    if re.match(r".*(\.).*",current_token.value) != None:
                        values = current_token.value.split(".")
                        for index, current_value in enumerate(values):
                            regex = r".*(" + str(re.escape(current_value)) + r").*"
                            match_obj = re.match(regex,sql_stmt)
                            starting_index = match_obj.span(1)[0]
                            if sql_stmt[starting_index-1] == "\'" :
                                result_statment.append([0,"\'"])
                                result_statment.append([0,"str"])
                                result_statment.append([0,"\'"])
                            elif sql_stmt[starting_index-1] == "\"":
                                result_statment.append([0,"\""])
                                result_statment.append([0,"str"])
                                result_statment.append([0,"\""])
                            elif sql_stmt[starting_index-1] == "'":
                                result_statment.append([0,"'"])
                                result_statment.append([0,"str"])
                                result_statment.append([0,"'"])
                            elif sql_stmt[starting_index-1] == "`":
                                result_statment.append([0,"`"])
                                result_statment.append([0,"str"])
                                result_statment.append([0,"`"])
                            else:
                                result_statment.append([0,"str"])

                            if index < len(values)-1:
                                result_statment.append([0,"."])


                    else:
                        regex = r".*(" + str(re.escape(current_token.value)) + r").*"
                        match_obj = re.match(regex,sql_stmt)
                        starting_index = match_obj.span(1)[0]
                        ending_index =  match_obj.span(1)[1]
                        if sql_stmt[starting_index-1] == "\'":
                            result_statment.append([0,"\'"])
                            result_statment.append([0,"str"])
                            result_statment.append([0,"\'"])
                        elif sql_stmt[starting_index-1] == "\"":
                            result_statment.append([0,"\""])
                            result_statment.append([0,"str"])
                            result_statment.append([0,"\""])
                        elif sql_stmt[starting_index-1] == "'":
                            result_statment.append([0,"'"])
                            result_statment.append([0,"str"])
                            result_statment.append([0,"'"])
                        elif sql_stmt[starting_index-1] == "`":
                            result_statment.append([0,"`"])
                            result_statment.append([0,"str"])
                            result_statment.append([0,"`"])
                        else:
                            # check if keyword from reserved keywords
                            if current_token.value.casefold() in self.operators:
                                result_statment.append([0,"op"])
                            elif current_token.value.casefold() in self.reserved_keywords:
                                result_statment.append([0,current_token.value])
                            else:
                                result_statment.append([0,"str"])


                token_index += len(current_token.value)



        # trucate to 20 pos before and 20 after token
        result_truncated = []
        for index, current_token in enumerate(result_statment):
            if current_token[0]:
                part_1 = result_statment[:index]
                part_2 = result_statment[index+1:]
                result_truncated.extend(part_1[-20:])
                result_truncated.append(result_statment[index])
                result_truncated.extend(part_2[:20])
                return " ".join([i[1] for i in result_truncated])

        raise Exception("no token found!")

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
    def check_keyword(self,w,result):
        if w.span()[0]-1 < 0 and  w.span()[0]-1 > len(w.group()):
            return w.group().casefold() in self.reserved_keywords
        elif w.span()[0]-1 > len(w.group()):
            return w.group().casefold() in self.reserved_keywords\
             and result[w.span()[0]-1] != "`"\
             and result[w.span()[0]-1] != "\""\
             and result[w.span()[0]-1] != "\'"
        elif w.span()[0]-1 < 0 :
            return w.group().casefold() in self.reserved_keywords\
             and result[w.span()[1]+1] != "("
        else:
            return w.group().casefold() in self.reserved_keywords\
             and result[w.span()[0]-1] != "`"\
             and result[w.span()[0]-1] != "\""\
             and result[w.span()[0]-1] != "\'"\
             and result[w.span()[1]+1] != "("\
                