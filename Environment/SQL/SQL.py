import copy
from Environment.Payload import Payload
import re
from Environment.Payload.Payload import Payload
from Environment.Tokens_Actions.Basic_Block.Base_Token import Base_Token
from Environment.Tokens_Actions.Basic_Block.FullComment_Token import FullComment_Token
from Environment.Tokens_Actions.Basic_Block.IdentifierRepresentation_Token import IdentifierRepresentation_Token

from Environment.Tokens_Actions.Basic_Block.OperatorRepresentation_Token import OperatorRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.NumberRepresentation_Token import NumberRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Identifier_Token import Identifier_Token
from Environment.Tokens_Actions.Basic_Block.Comma_Token import Comma_Token
from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Category, Comment_Token
from Environment.Tokens_Actions.Basic_Block.HexRepresentation_Token import HexRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Category
from Environment.Tokens_Actions.Basic_Block.String_Token import String_Token
from Environment.Tokens_Actions.Basic_Block.CommentRange_Token import CommentRange_Token
class SQL:
    def __init__(self,sql_statment:str,identifier:str,tokens=None) -> None:
        self.sql_statment = sql_statment
        self.sql_starting_stmt = None

        if tokens == None:
            self.__tokens,self.sql_starting_stmt = SQL.parse_string(sql_statment,identifier)
        else:
            assert(isinstance(tokens,Base_Token))
            self.__tokens = tokens
            
        # get identifier token index
        self.__identifier_token_flat_index = None
        for i,current_token in enumerate(self.__tokens.flat_idx_tokens_list()):
            if isinstance(current_token,IdentifierRepresentation_Token):
                self.__identifier_token_flat_index = i
            
        if self.__identifier_token_flat_index == None:
            print(identifier)
            print([e for e in self.__tokens.flat_idx_tokens_list()])
        assert(self.__identifier_token_flat_index != None)
        pass

    def divide_by_identifer(statment:str,identifer:str):
        '''
            function used to remove the identifer from the string and return the rest of the statment
            return: splited_statment_before, splited_statment_after OR raise exception when not found
        '''
        regex = r"(.*)" + identifer + r"(.*)"
        matcher = re.match(regex,statment)
        if matcher is not None:
            splited_statment_before = matcher.group(1)
            splited_statment_after = matcher.group(2)
            return splited_statment_before,splited_statment_after
        else:
            raise Exception(f"TOKEN NOT FOUND\n SQL: {statment}")
        pass
    def divde_string_by_word_boundries(statment:str):
        '''
            divide statment using word boundries
        '''
        result = []
        regex = r"\b";
        splits = re.split(regex,statment)
        word = True
        for i, current_match in enumerate(splits):
        # split all non word boundaries
            # check if leading white space or ending white space then skip
            if (i == len(splits) or i == 0) and (current_match == ""):
                pass
            else:
                # check white_space
                whitespace = r"|".join([re.escape(e) for e in OperatorRepresentation_Token.special_operators])  +r"|"+r"|".join([re.escape(e) for e in Whitespace_Token.whitespace_type_mapping.values()]) + r"|" + r"|".join([re.escape(e) for e in Comment_Token.comment_type_mapping.values()]) +r"|"+r"|".join([re.escape(e) for e in Quote_Token.quote_type_mapping.values()])+r"|"+r"|".join([re.escape(e) for e in Paranthesis_Token.paranthesis_type_mapping.values()])
                special_chars = re.finditer(whitespace,current_match)
                
                if len(list(re.finditer(whitespace,current_match))) > 0:
                    spans = [c.span() for c in re.finditer(whitespace,current_match)]
                    
                    starting_index = [c[0] for c in spans]
                    ending_index = [c[1] for c in spans]
                    current_index = 0
                    while current_index < len(current_match):
                        if  current_index in starting_index:
                            starting = current_index
                            ending = ending_index[starting_index.index(current_index)]
                            result.append(current_match[starting:ending])
                            current_index += ending - starting
                        else:
                            result.append(current_match[current_index])
                            current_index+= 1
                else:
                    result.append(current_match)
                word = True
        return result

    def convert_words_to_tokens(words:list,identifier:str):
        tokens = []
        # first pass
        # insitate tokens for each element
        for current_token in words:
            # if number 
            if current_token == identifier:
                tokens.append(IdentifierRepresentation_Token.parse(current_token))

            # if identifier
            elif  NumberRepresentation_Token.is_number(current_token):
                tokens.append(NumberRepresentation_Token.parse(current_token))

            # if whitespace
            elif Whitespace_Token.is_whitespace(current_token):
                tokens.append(Whitespace_Token.parse(current_token))

            # if operator
            elif OperatorRepresentation_Token.is_operator(current_token):
                tokens.append(OperatorRepresentation_Token.parse(current_token))

            # if paranthesis
            elif Paranthesis_Token.is_paranthesis(current_token):
                tokens.append(Paranthesis_Token.parse(current_token))

            # if comma
            elif Comma_Token.is_comma(current_token):
                tokens.append(Comma_Token.parse(current_token))

            # if comment
            elif Comment_Token.is_comment(current_token):
                tokens.append(Comment_Token.parse(current_token))

            # if hex
            elif HexRepresentation_Token.is_hex(current_token):
                tokens.append(HexRepresentation_Token.parse(current_token))
            
            # if quotes
            elif Quote_Token.is_quote(current_token):
                tokens.append(Quote_Token.parse(current_token))

            # if string
            else:
                tokens.append(StringRepresentation_Token.parse(current_token))
        # input(f"[SQL->convert words to tokens] tokens generated first pass are {tokens}")

        # pass until no changes
        last_pass = tokens
        changed = True
        while changed:
            changed = False
            current_index = 0
            current_pass = []
            while(current_index < len(last_pass)):
                # multi charachter oprators
                if isinstance(last_pass[current_index],OperatorRepresentation_Token) and current_index +1 < len(last_pass) and isinstance(last_pass[current_index+1],OperatorRepresentation_Token) and OperatorRepresentation_Token.is_operator(str(last_pass[current_index]) + str(last_pass[current_index+1])):
                    
                    current_pass.append(OperatorRepresentation_Token.parse(str(last_pass[current_index]) + str(last_pass[current_index+1])))
                    current_index += 1#op 1
                    current_index += 1#op 2
                    changed = True

                # full comement --
                elif current_index+2 < len(last_pass) and isinstance(last_pass[current_index],OperatorRepresentation_Token)  and isinstance(last_pass[current_index+1],OperatorRepresentation_Token) and isinstance(last_pass[current_index+2],Whitespace_Token) and Comment_Token.is_comment(str(last_pass[current_index]) + str(last_pass[current_index+1]) + str(last_pass[current_index+2])):
                    comment_Token =  Comment_Token.parse(str(last_pass[current_index]) + str(last_pass[current_index+1]) + str(last_pass[current_index+2]))
                    current_pass.append(comment_Token)
                    current_index += 3                    
                    changed = True

                # # comment range
                elif isinstance(last_pass[current_index],OperatorRepresentation_Token) and current_index +1 < len(last_pass) and isinstance(last_pass[current_index+1],OperatorRepresentation_Token) and Comment_Token.is_comment(str(last_pass[current_index]) + str(last_pass[current_index+1])):
                    open_comment_Token =  Comment_Token.parse(str(last_pass[current_index]) + str(last_pass[current_index+1]))
                    current_index += 2#open comment                   
                    current_pass.append(open_comment_Token)
                    changed = True

                # if keyword
                elif isinstance(last_pass[current_index],StringRepresentation_Token) and KeywordRepresentation_Token.is_keyword(str(last_pass[current_index])) and current_index < len(last_pass) and not(current_index > 1 and isinstance(last_pass[current_index-1],Quote_Token) and  isinstance(last_pass[current_index+1],Quote_Token)):
                    current_pass.append(KeywordRepresentation_Token.parse(str(last_pass[current_index])))
                    current_index += 1
                    changed = True

                else:
                    current_pass.append(last_pass[current_index])
                    current_index += 1

            last_pass = copy.deepcopy(current_pass)

        return current_pass

    def parse_string(statement:str,identifier:str):
        '''
            parse the statment into tokens
            we assume the identifer is the starting point 
        '''
        # split the statment to remove the staring token
        statment_before, statment_after = SQL.divide_by_identifer(statement,identifier)
        # get all words and non words
        result = []


        # divide statment before identifer by word boundries
        result.extend(SQL.divde_string_by_word_boundries(statment_before))
        # add identifer
        result.append(identifier)
        # divide statment after the idenfier by word boundries
        result.extend(SQL.divde_string_by_word_boundries(statment_after))


        # convert parsed words into tokens
        tokens = SQL.convert_words_to_tokens(result,identifier)
        

        token_found = False
        for i,current_token in enumerate(tokens):
            if isinstance(current_token,IdentifierRepresentation_Token):
                token_found = True

        if not token_found:
            print(identifier)
            print(tokens)
            print(statement)

        assert(token_found)

        base_token = Base_Token()
        for current_token in tokens:
            base_token.append_token_base_idx(current_token)
        
        return base_token,statment_before

    def get_in_between_quotes(self,payload:Payload,str_1_idx:int, str_2_idx:int) -> list:
        '''
            get the quotes inbetween the two token based on the sql statment
        '''

        # build regex using payload 
        payload_tokens = payload.get_tokens_base_idx()
        if len(payload_tokens) < 1:
            return False

        regex = [r".*?"]

        for current_payload_token_idx in range(len(payload_tokens)):
            if current_payload_token_idx == str_1_idx and current_payload_token_idx == str_2_idx:
                regex.append(re.escape(str(str(payload_tokens[current_payload_token_idx]))) + r"(.*?)")
            elif current_payload_token_idx == str_1_idx:
                regex.append(re.escape(str(str(payload_tokens[current_payload_token_idx]))) + r"(")
                regex.append(r".*?")
            elif current_payload_token_idx == str_2_idx:
                regex.append(r")" + re.escape(str(str(payload_tokens[current_payload_token_idx])) ))
                regex.append(r".*?")
            else:   
                regex.append(re.escape(str(payload_tokens[current_payload_token_idx])))
                regex.append(r".*?")

        regex = "".join(regex)

        # check that there is string exist in that area otherwise empty
        if re.search(regex,self.sql_statment) is not None :

            string = re.search(regex,self.sql_statment).groups(1)[0]

            # find all quotes in order
            quote_regex = r"|".join(Quote_Token.quote_type_mapping.values())

            return [m.group(0) for m in re.finditer(quote_regex, string)]
        else:

            return []

    def is_affective_behviour_changing(self,payload:Payload,payload_identifier_token_base_idx:int,payload_token_2_base_idx:int):
        '''
            check if token 1 and token 2 in different context and token 2 not in comment part
            a different context is considered when token 1 inside quotes and token 2 is outside the quotes
            when token 1 is without quotes around it, then token 1 and token in different context as long as no commenting precceding token 2
        '''
        # validate identifier index less than token 2 otherwise the logic does not work
        assert(payload_identifier_token_base_idx <= payload_token_2_base_idx)


        # payload flat tokens
        payload_base_tokens = payload.get_tokens_base_idx()

        # validate identifier token
        assert(isinstance(payload_base_tokens[payload_identifier_token_base_idx],IdentifierRepresentation_Token))

        # check if identifier inside quotes
        open_quotes = []
        quote_open_before_ident = 0
        for ii, current_token in enumerate(self.get_tokens().flat_idx_tokens_list()):
            # check if quote
            if isinstance(current_token,Quote_Token):
                # check if any same quote opened
                found_open = False
                for i, current_opend_quotes in reversed(list(enumerate(open_quotes))):
                    if current_opend_quotes == str(current_token):
                        open_quotes.pop(i)
                        found_open = True
                        break

                # if no quote found open same as current token thenr register as open token
                if not found_open:
                    open_quotes.append(str(current_token))

            if isinstance(current_token,IdentifierRepresentation_Token):
                quote_open_before_ident = len(open_quotes)
                break
        
        
        # if there is quote open then identifier within quotes
        if quote_open_before_ident > 0:
            # apply regex to find out if the quotes have been closed between identifer and token
            quote_list = self.get_in_between_quotes(payload,payload_identifier_token_base_idx,payload_token_2_base_idx)
            is_outside_identifer_Context,lefted_quotes = SQL.list_after(quote_list, open_quotes[0])

            if is_outside_identifer_Context:
                # get reduced quotes

                reduced_quotes = SQL.reduce_quotes_to_open(lefted_quotes)
                # check that no open quotes

                if len(reduced_quotes) == 0:
                    # all quotes closed and the token not withen quotes
                    token_inside_quote = False
                else:
                    # the token within quotes
                    token_inside_quote = True
                
                # escaped id quote
                token_in_identifier_context = False

            else:
                # there is open quote not closed
                token_in_identifier_context = True
                token_inside_quote = True
        else:
            # identifier with no context
            token_in_identifier_context = False
            token_inside_quote = False

        
        # check wether commenting before token 2 based on payload flat indexing
        # (in here we assume no extra commenting done by web service inside our payload area)
        # (can be changed to sql based to capture any extra made by web server using regex like above)
        current_token = 0
        is_commented = False
        toret = []
        pstack = []
        while current_token < payload_token_2_base_idx:

            if isinstance(payload_base_tokens[payload_identifier_token_base_idx + current_token],FullComment_Token) or (isinstance(payload_base_tokens[payload_identifier_token_base_idx + current_token],Comment_Token) and payload_base_tokens[payload_identifier_token_base_idx + current_token].comment_category( )== Comment_Category.Full_Comment):

                is_commented = True
                break
            if isinstance(payload_base_tokens[payload_identifier_token_base_idx + current_token],Comment_Token) and payload_base_tokens[payload_identifier_token_base_idx + current_token].comment_category( )== Comment_Category.Open_Range_Comment:

                pstack.append(current_token)
            elif isinstance(payload_base_tokens[payload_identifier_token_base_idx + current_token],Comment_Token) and payload_base_tokens[payload_identifier_token_base_idx + current_token].comment_category( )==Comment_Category.Close_Range_Comment:


                if len(pstack) > 0:
                    toret.append([pstack.pop(), current_token])
            current_token += 1

        
        # check whether we have opened a range comment and not closed
        if len(pstack) > 0:
            is_commented = True
            
        return not (token_in_identifier_context or  is_commented or token_inside_quote)

    def is_keyword_after_payload_commented(self,payload,identifer_token_base_index:int):
        # payload flat tokens
        payload_base_tokens = payload.get_tokens_base_idx()

        # check wether any sql keyword have been commented using full comment
        is_sql_keyowrds_after_payload_commented = False
        for current_token_idx,current_token in enumerate(payload_base_tokens):
            if isinstance(current_token,FullComment_Token) and self.is_affective_behviour_changing(payload,identifer_token_base_index,current_token_idx):
                is_sql_keyowrds_after_payload_commented = self.is_sql_keywords_after_payload(payload)
                break
        return is_sql_keyowrds_after_payload_commented
    def is_sql_keywords_after_payload(self,payload:Payload):
        '''
            identify if any keywords after the payload
            TODO this function consider reserved keywords in strings as keywords which is false
        '''
        payload_tokens = payload.get_tokens_flat_idx()
        if len(payload_tokens) < 1:
            return False
        
        regex = r".*?"
        for current_payload_token_idx in range(len(payload_tokens)):
            regex += re.escape(str(payload_tokens[current_payload_token_idx]))
            if current_payload_token_idx < len(payload_tokens) -1:
                regex += r".*?"
        regex += r"(.*)"
        results_1 = re.search(regex,self.sql_statment)
        if results_1 is not None :
            # get string of after payload
            after_payload_str  = results_1.groups(1)[0]

            if any(y in after_payload_str.casefold() for y in KeywordRepresentation_Token.reserved_keywords):
                return True
            else:
                return False
        else:
            return False

    def list_starts_with(l1,l2):
        l1_idx = 0  
        if len(l1) == len(l2) or len(l2) < len(l1):
            for current_element in l2:
                if current_element == l1[l1_idx]:
                    l1_idx += 1
                else:
                    return False,None
            return True,l1[l1_idx:]
        else:
            return False,None

    def list_contains(l1,l2):
        '''
        find sub list l1 in l2
        used for open and closed quotes where open is l2 and closed quotes is reverese of l1
        return  bool found or not
        return sublist after the part of first matched list
        '''
        sll=len(l1)
        for ind in (i for i,e in enumerate(l2) if e==l1[0]):
            if l2[ind:ind+sll]==l1:
                return True, l2[ind+sll:]
        return False, None
        
    def list_after(l1:list,quote):
        '''
        find the first match of quote in list and return all after that quote else return false and none
        '''
        for idx,current_quote in enumerate(l1):
            if current_quote == quote:
                return True,l1[idx+1:]

        return False, None

    def reduce_quotes_to_open(quotes):
        stack = []
        for current_element in quotes:
            if len(stack) > 0:
                found = False
                for curren_quote_idx, current_quote_stack in enumerate(stack):
                    if current_element == current_quote_stack:
                        stack = stack[:curren_quote_idx]
                        found = True
                        break

                if not found:
                    stack.append(current_element)
            else:
                stack.append(current_element)
        return stack

    def contains(self,payload:Payload,flat_idx:int):
        payload_tokens = payload.get_tokens_flat_idx()
        if len(payload_tokens) < 1:
            return False
        
        regex = r".*?"
        for current_payload_token_idx in range(len(payload_tokens)):
            if current_payload_token_idx == flat_idx:
                regex += r"(" + re.escape(str(str(payload_tokens[current_payload_token_idx]))) + r")"
            else:   
                regex += re.escape(str(payload_tokens[current_payload_token_idx]))
            regex += r".*?"

        if re.search(regex,self.sql_statment) is not None :
            return re.search(regex,self.sql_statment).groups(1)[0] == str(payload_tokens[flat_idx])
        else:
            return False

    def is_sanatized(self,payload:Payload,paylaod_flat_token_idx:int):
        # validate the token index
        payload.base_token.is_valid_flat_idx(paylaod_flat_token_idx)

        # get payload tokens flat index
        payload_flat_tokens = payload.base_token.flat_idx_tokens_list()

        # build regex for the given location of token in the sql to see if it get sanatized or not
        regex = r".*?"
        for current_payload_token_idx in range(len(payload_flat_tokens)):
            if current_payload_token_idx == paylaod_flat_token_idx:
                regex += r"(.*)"
                break
            else:   
                regex += re.escape(str(payload_flat_tokens[current_payload_token_idx]))
                if current_payload_token_idx+1 != paylaod_flat_token_idx:
                    regex += r".*?"
        

        # match payload regex to sql statment and see if they match the token wanted or other elements exist
        match_found = re.search(regex,self.sql_statment,flags=re.IGNORECASE)
        # if match
        if match_found:
            match_string = match_found.groups(1)[0]
            if match_string.casefold().startswith(str(payload_flat_tokens[paylaod_flat_token_idx]).casefold()):
                return None
            else:
                return paylaod_flat_token_idx
        else:
            return paylaod_flat_token_idx

    def get_generic_statment(self):
        result = copy.deepcopy(self)
        flat_list = result.get_tokens().flat_idx_tokens_list()
        for i,current_token in enumerate(flat_list):
            if isinstance(current_token,StringRepresentation_Token):
                current_token.set_value("str")
            elif isinstance(current_token,OperatorRepresentation_Token):
                current_token.set_value("op")
            elif isinstance(current_token,NumberRepresentation_Token):
                current_token.set_value("num")
            elif isinstance(current_token,HexRepresentation_Token):
                current_token.set_value("hex")
            elif isinstance(current_token,IdentifierRepresentation_Token):
                current_token.set_value("id")

        # truncate to 20 before and after
        n = 20
        ident_idx = -1
        flat_tokens_list = result.get_tokens().flat_idx_tokens_list()
        for i,current_token in enumerate(flat_tokens_list):
            if isinstance(current_token,IdentifierRepresentation_Token):
                ident_idx = i
                break

        if ident_idx == -1:
            assert(ident_idx != -1)
        token = flat_tokens_list[ident_idx]
        new_base = Base_Token()
        part_1 = flat_tokens_list[:ident_idx]
        part_2 = flat_tokens_list[ident_idx+1:]
        for current_token in part_1[-n:]:
            new_base.append_token_base_idx(current_token)
        
        new_base.append_token_base_idx(token)

        for current_token in part_2[:n]:
            new_base.append_token_base_idx(current_token)

        return SQL(str(new_base),str(token),new_base)
    def replace_identifier_with_payload(self,payload:Payload):
        '''
            replace identifer token with payload flat tokens
        '''
        # get flat tokens from payload
        paylod_flat_tokens = payload.base_token.flat_idx_tokens_list()

        # get identifier token index
        identifier_token_flat_index = None
        for i,current_token in enumerate(self.__tokens.flat_idx_tokens_list()):
            if isinstance(current_token,IdentifierRepresentation_Token):
                identifier_token_flat_index = i
        assert(identifier_token_flat_index != None)

        # replace identifer with payload
        self.__tokens.replace_flat_idx_token_with_tokens(identifier_token_flat_index,paylod_flat_tokens)

        # maintain new identifer index
        self.__identifier_token_flat_index = None
        for i,current_token in enumerate(self.__tokens.flat_idx_tokens_list()):
            if isinstance(current_token,IdentifierRepresentation_Token):
                self.__identifier_token_flat_index = i
        assert(self.__identifier_token_flat_index != None)

    def is_identifier_in_context(self):
        '''
            identify if identifer within quotes
        '''

        # check if identifier inside quotes
        open_quotes = []
        quote_open_before_ident = 0
        for ii, current_token in enumerate(self.get_tokens().flat_idx_tokens_list()):
            # check if quote
            if isinstance(current_token,Quote_Token):
                # check if any same quote opened
                found_open = False
                for i, current_opend_quotes in reversed(list(enumerate(open_quotes))):
                    if current_opend_quotes == current_token:
                        # print(f"[is_identifier_in_context] pop quote {current_opend_quotes} at index {i}")
                        open_quotes.pop(i)
                        found_open = True
                        break

                # if no quote found open same as current token then register as open token
                if not found_open:
                    open_quotes.append(str(current_token))

            if isinstance(current_token,IdentifierRepresentation_Token):
                quote_open_before_ident = len(open_quotes)
                break
        
        if quote_open_before_ident > 0:
            return True
        else:
            return False
            
    def in_context_elements(self):
        '''
            get tokens inbetween the identifer and the closing token
        '''
        # check if identifier inside quotes
        open_quotes = []
        quote_open_before_ident = 0
        for ii, current_token in enumerate(self.get_tokens().flat_idx_tokens_list()):
            # check if quote
            if isinstance(current_token,Quote_Token):
                # check if any same quote opened
                found_open = False
                for i, current_opend_quotes in reversed(list(enumerate(open_quotes))):
                    if current_opend_quotes == current_token:
                        open_quotes.pop(i)
                        found_open = True
                        break

                # if no quote found open same as current token then register as open token
                if not found_open:
                    open_quotes.append(str(current_token))

            if isinstance(current_token,IdentifierRepresentation_Token):
                quote_open_before_ident = len(open_quotes)
                break
        closing_quotes = list(reversed(open_quotes))
        in_context_elements = []
        current_token_index = 0
        is_ident_reached = False
        flat_index_sql_tokens = self.get_tokens().flat_idx_tokens_list()
        while current_token_index < len(flat_index_sql_tokens):
            if is_ident_reached:
                if len(closing_quotes) > 0:
                    if str(flat_index_sql_tokens[current_token_index]) == closing_quotes[0]:
                        closing_quotes.pop(0)
                    else:
                        in_context_elements.append(flat_index_sql_tokens[current_token_index])
                else:
                    break
                
            elif isinstance(flat_index_sql_tokens[current_token_index],IdentifierRepresentation_Token):
                is_ident_reached = True
            
            current_token_index += 1
        return in_context_elements

    def get_identifier_closing_quote(self):
        '''
            get identifer closing quote
        '''

        # check if identifier inside quotes
        open_quotes = []
        quote_open_before_ident = 0
        for ii, current_token in enumerate(self.get_tokens().flat_idx_tokens_list()):
            # check if quote
            if isinstance(current_token,Quote_Token):
                # check if any same quote opened
                found_open = False
                for i, current_opend_quotes in reversed(list(enumerate(open_quotes))):
                    if current_opend_quotes == current_token:
                        open_quotes.pop(i)
                        found_open = True
                        break

                # if no quote found open same as current token then register as open token
                if not found_open:
                    open_quotes.append(str(current_token))

            if isinstance(current_token,IdentifierRepresentation_Token):
                quote_open_before_ident = len(open_quotes)
                break
        
        return list(reversed(open_quotes))

    def get_tokens(self):
        return self.__tokens
    def get_identifier_token_flat_index(self):
        return self.__identifier_token_flat_index
    def __str__(self) -> str:
        return self.get_tokens().__str__()
    def __repr__(self) -> str:
        return self.__str__()