from itertools import repeat, chain, islice
from torch import nn
import torch
import sklearn
import random 
from queue import PriorityQueue
def trimmer(seq, size, filler=""):
    return islice(chain(seq, repeat(filler)), size)

# initialize weights
def init_weights(m):
    for name, param in m.named_parameters():
        nn.init.normal_(param.data, mean=0, std=0.01)

# calculate the number of trainable parameters in the model.
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

teacher_forcing_ratio = 0.5


def train(input_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,device,embedder):
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[embedder.token_to_idx_2["SOS".casefold()]]], device=device)

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
    pred_output = []
    if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
        for di in range(input_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            loss += criterion(decoder_output, input_tensor[di])
            topv, topi = decoder_output.topk(1)
            pred_output.append(topi.cpu().detach().numpy()[0][0])

            decoder_input = input_tensor[di]  # Teacher forcing

    else:
        # Without teacher forcing: use its own predictions as the next input
        for di in range(input_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.topk(1)
            decoder_input = topi.squeeze().detach()  # detach from history as input

            loss += criterion(decoder_output, input_tensor[di])
            pred_output.append(topi.cpu().detach().numpy()[0][0])
            if decoder_input.item() == embedder.token_to_idx_2["EOS".casefold()]:
                break
        
    print(" ".join([embedder.idx_to_token_2[current] for current in pred_output]))
    print(" ".join([embedder.idx_to_token_2[current] for current in input_tensor.cpu().detach().numpy().flatten()]))
       

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / input_length
def evaluate(input_tensor, encoder, decoder,device,embedder,max_length,criterion):
    wrong_indexs = 0
    encoder_hidden = encoder.initHidden()

    input_length = input_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[embedder.token_to_idx_2["SOS".casefold()]]], device=device)

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
    pred_output = []

    for di in range(input_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        topv, topi = decoder_output.topk(1)
        decoder_input = topi.squeeze().detach()  # detach from history as input

        loss += criterion(decoder_output, input_tensor[di])
        if embedder.idx_to_token_2[input_tensor[di].item()] == embedder.idx_to_token_2[topi.cpu().detach().numpy()[0][0]]:
          wrong_indexs += 1
    wrong_indexs = float(wrong_indexs)/float(input_length)
    return wrong_indexs

def tensorFromStatment(sentence,device):    
    return torch.tensor(sentence, dtype=torch.long, device=device).view(-1, 1)

# epcoh time 
import time
import math


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))

  # epcoh time 
def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

class DualPriorityQueue(PriorityQueue):
    def __init__(self, maxPQ=False):
        super().__init__()
        self.reverse = -1 if maxPQ else 1

    def put(self, priority, data):
        PriorityQueue.put(self, (self.reverse * priority, data))

    def get(self, *args, **kwargs):
        priority, data = PriorityQueue.get(self, *args, **kwargs)
        return self.reverse * priority, data