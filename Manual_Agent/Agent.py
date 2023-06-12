from operator import index
import pprint
class Agent:
    actions= ["add_comma","add_comment","comment_range","add_paranthesis","add_quote","add_whitespace","add_string",\
          "add_and","add_or","add_if","add_sleep","add_union","add_where",\
          "capatilize_keyword","convert_str_char","convert_str_hex","convert_str_concat","change_non_whitespace",\
          "remove_token"]
    idx_to_action_map = {i:curr_action for i,curr_action in enumerate(actions)}
    action_to_idx_map = {curr_action:i for i,curr_action in enumerate(actions)}
    def __init__(self,learning=None) -> None:
        self.pp = pprint.PrettyPrinter(indent=4)
        pass

    def get_next_action(self,current_state):
        '''
            return the action chosen by user
        '''
        # print current game
        current_game = current_state["game"]
        print(f"current game: {current_game}")
        # print current payload
        current_payload = current_state["payload"]
        print(f"current payload")
        print(current_payload)
        # print current sql statment
        current_sql = current_state["sql"]
        print(f"current sql")
        print(current_sql)
        # print available actions
        available_actions = current_state["actions"]
        print("available action")
        named_actions = [{"action": Agent.idx_to_action_map[current_action["action"]],"range": current_action["range"], "type":current_action["type"]} for current_action in available_actions]
        indexed_actions = {i:current_action for i,current_action in enumerate(named_actions)}
        self.pp.pprint(indexed_actions)
        
        valid_action = False
        while not valid_action:
            # get action index
            action_index = input("action index: ")
            try:
                # validate
                action_index = int(action_index)
                if action_index in indexed_actions.keys():
                    valid_action = True
            except:
                pass

        # return action
        return available_actions[action_index]