from enum import Enum


class Token:
    class Category(Enum):
        BASIC_BLOCK = 1
        SYNTAX_FIXING = 2
        SANATISATION_ESCAPING = 3
        BEHAVIOR_CHANGING = 4
        def __str__(self) -> str:
            return self._name_
        def __repr__(self) -> str:
            return self.__str__()

    def __init__(self) -> None:
        self.token_list = []
        pass

    def value(self):
        return self.token_list

    def type(self):
        return "Token"

    def category(self):
        return Token.Category.BASIC_BLOCK

    def __str__(self) -> str:
        rev = [str(current) for current in self.token_list]
        return "".join(rev)

    def __repr__(self) -> str:
        return self.__str__()

    def flat_idx_length(self):
        counter = 0
        for current_token in self.token_list:
            if len(current_token.token_list) > 0:   
                counter += current_token.flat_idx_length()
            else:
                counter += 1
        return counter

    def flat_idx_tokens_list(self):
        tokens = []
        for current_token in self.token_list:
            if len(current_token.token_list) > 0:  
                tokens.extend(current_token.flat_idx_tokens_list())
            else:
                tokens.append(current_token)
        return tokens

    def replace_flat_idx(self,pos:int,token,current_global_pos=-1):
        assert(isinstance(pos,int))
        local_idx = -1
        for current_token in self.token_list: 
            is_basic_token = current_token.is_basic_token()
            if is_basic_token:
                current_global_pos += 1
                local_idx += 1
                if pos == current_global_pos:
                    assert(self.is_valid_base_idx(local_idx))
                    self.token_list.pop(local_idx)
                    self.token_list.insert(local_idx,token)
                    return True,current_global_pos
            else:
                is_finished,current_global_pos = current_token.replace_flat_idx(pos,token,current_global_pos)
                if is_finished:
                    return True,current_global_pos

        return False,current_global_pos
    def replace_flat_idx_token_with_tokens(self,pos:int,tokens:list,current_global_pos=-1):
        assert(isinstance(pos,int))
        local_idx = -1
        for current_token in self.token_list: 
            is_basic_token = current_token.is_basic_token()
            if is_basic_token:
                current_global_pos += 1
                local_idx += 1
                if pos == current_global_pos:
                    assert(self.is_valid_base_idx(local_idx))
                    self.token_list.pop(local_idx)
                    self.token_list[local_idx:local_idx] = tokens
                    return True,current_global_pos
            else:
                is_finished,current_global_pos = current_token.replace_flat_idx(pos,tokens,current_global_pos)
                if is_finished:
                    return True,current_global_pos

        return False,current_global_pos

    def is_valid_base_idx(self,pos:int):
        return pos < len(self.token_list) and pos >= 0

    def remove_token_flat_idx(self,pos:int,current_global_pos=-1):
        local_idx = -1

        for current_token in self.token_list: 
            is_basic_token = current_token.is_basic_token()
            if is_basic_token:
                current_global_pos += 1
                local_idx += 1
                if pos == current_global_pos:
                    assert(self.is_valid_base_idx(local_idx))
                    self.token_list.pop(local_idx)
                    return True,current_global_pos                    
            else:
                is_finished,current_global_pos = current_token.remove_token_flat_idx(pos,current_global_pos)
                if is_finished:
                    return True,current_global_pos     
        return False,current_global_pos

    def is_basic_token(self):
        if len(self.token_list) > 0:   
            return False
        else:
            return True 

    def __eq__(self, other): 
        if not isinstance(other, Token):
            # don't attempt to compare against unrelated types
            return NotImplemented
        else:
            if len(self.token_list) > 0:
                if self.token_list == other.token_list:
                    return True
                else:
                    return False
            else:
                # print(f"[!] __eq__ compare {self.value()} with {other.value()}")

                return self.value() == other.value()
                
