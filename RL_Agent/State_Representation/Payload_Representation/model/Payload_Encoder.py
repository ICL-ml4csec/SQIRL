
import torch.nn as nn
import torch
class Payload_Encoder(nn.Module,):
    def __init__(self, input_size, hidden_size,max_length):
        super(Payload_Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.max_length = max_length

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    def encode(self,input_tensor,length):
        encoder_hidden = self.initHidden()
        encoder_outputs = torch.zeros(self.max_length, self.hidden_size, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))


        for ei in range(length):
            encoder_output, encoder_hidden = self(input_tensor[ei], encoder_hidden)

            encoder_outputs[ei] = encoder_output[0, 0]

        return encoder_outputs, encoder_hidden