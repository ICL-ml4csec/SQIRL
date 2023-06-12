
import random
import os
from RL_Agent.State_Representation.Payload_Representation.Payload_Generic_Parser import Payload_Generic_Parser
from RL_Agent.State_Representation.Payload_Representation.Payload_Representation import Payload_Representation

from RL_Agent.State_Representation.Payload_Representation.model.dataset.Payload_Generator import Payload_Generator

import pickle
class Dataset_Generator:
    def __init__(self,file_path) -> None:
        self.dataset_file = file_path
        self.gen = Payload_Generator()
        self.generic_parser = Payload_Generic_Parser()

    def generate_dataset(self,size):
        full_payload_path = os.path.join(self.dataset_file, 'full_payload.dataset')
        generic_payload_path = os.path.join(self.dataset_file, 'generic_payload.dataset')

        full_payload_file_path = open(full_payload_path,"w+")
        generic_payload_file_path = open(generic_payload_path,"w+")
        generic_payloads  = []
        for current_stmt_idx in range(size):
            current_payload = self.gen.generate_payload()
            full_payload_file_path.write(str(current_payload) + "\n")
            generic_payload = self.generic_parser.convert_generic(current_payload)
            generic_payloads.append(generic_payload)
            print(generic_payload)
            print(Payload_Representation.payload_embedding(generic_payload))
        with open(generic_payload_path,"wb") as f:
            pickle.dump(generic_payloads,f)        
            