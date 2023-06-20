import hashlib
import random
class Input_Identifier:
    def __init__(self) -> None:
        self.current_count = random.randint(0,100)
        pass

    def get_next_token(self):
        assert(self.current_count < float('inf'))
        m = random.getrandbits(40)
        self.current_count += 1
        return str(m)