from Environment.Payload.Payload import Payload
from Environment.Input.Input_Identifier import Input_Identifier
from Environment.Environment import Game_Type
from Environment. Environment import SQLI_Environment
import random
class Payload_Generator:
    def __init__(self) -> None:
        self.identifier_generator = Input_Identifier()
        self.max_actions = 30
        self.games = [Game_Type.BEHAVIOR_CHANGING,Game_Type.SANITIZATION_ESCAPING,Game_Type.SYNTAX_FIXING]
        pass

    def generate_payload(self):
        token_identifier = self.identifier_generator.get_next_token()
        payload = Payload(token_identifier)

        no_payload_actions = random.randint(1,self.max_actions)
        for current_action in range(no_payload_actions):
            current_av_actions = 0
            while current_av_actions == 0:
                
                game_type = random.choice(self.games)

                available_actions = payload.available_actions(SQLI_Environment.game_to_token[game_type])
                current_av_actions = len(available_actions)


            chosen_action = random.choice(available_actions)
            payload.apply_action(chosen_action)
        return payload