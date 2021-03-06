from AutoEncoder import Encoder, Decoder
import string
import random
import torch
import torch.nn as nn
from io import open
import matplotlib.pyplot as plt
import time
import math
import os
import pandas as pd

SOS = '1'
EOS = '2'
PAD = '3'
DROP_OUT = '4'
ALL_CHARS = string.ascii_letters + "'-" + SOS + EOS + PAD + DROP_OUT
LETTERS_COUNT = len(ALL_CHARS)

def char_to_index(char: str) -> int:
    return ALL_CHARS.find(char)

def string_to_tensor(string: str) -> list:
    tensor = torch.zeros(len(string),1,LETTERS_COUNT)
    for i,char in enumerate(string):
        tensor[i,0,char_to_index(char)] = 1
    return tensor

def int_to_tensor(index: int) -> list:
    tensor = torch.zeros([1, LETTERS_COUNT],dtype=torch.long)
    tensor[:,index] = 1
    return tensor

def train(x):
    enc_optim.zero_grad()
    dec_optim.zero_grad()

    loss = 0.
    x = string_to_tensor(x)
    enc_hidden = enc.init_hidden()
    for i in range(x.shape[0]):
        # RNN requires 3 dimensional inputs
        _, enc_hidden = enc(x[i].unsqueeze(0), enc_hidden)

    dec_input = torch.zeros(1, 1, LETTERS_COUNT)
    dec_input[0, 0, -1] = 1.
    dec_hidden = enc_hidden
    name = ''
    
    for i in range(x.shape[0]):
        dec_probs, dec_hidden = dec(dec_input, dec_hidden)
        _, nonzero_indexes = x[i].topk(1)
        best_index = torch.argmax(dec_probs, dim=2).item()
        loss += criterion(dec_probs[0], nonzero_indexes[0])
        name += CHARS[best_index]
        dec_input = torch.zeros(1, 1, LETTERS_COUNT)
        dec_input[0, 0, best_index] = 1.

    loss.backward()
    enc_optim.step()
    dec_optim.step()
    return name, dec_probs, loss.item()

def run_iter(n_iters, column: str, chckpt: str):
    print_every = 5000
    plot_every = 500
    all_losses = []
    total_loss = 0 # Reset every plot_every iters
    start = time.time()
    for iter in range(1, n_iters + 1):
        input = randomName(df, column)
        if not isinstance(input,str):
            continue
        name, output, loss = train(input)
        total_loss += loss

        if iter % print_every == 0:
            print('%s (%d %d%%) %.4f' % (timeSince(start), iter, iter / n_iters * 100, loss))
            print('input: %s, output: %s' % (input, name))

        if iter % plot_every == 0:
            all_losses.append(total_loss / plot_every)
            total_loss = 0

    torch.save({'weights':dec.state_dict()}, os.path.join(f"{chckpt}_checkpt.pth.tar"))

hidden_layer_sz = 256
enc = Encoder(LETTERS_COUNT, hidden_layer_sz, 1)
dec = Decoder(LETTERS_COUNT, hidden_layer_sz, LETTERS_COUNT)
criterion = nn.NLLLoss()

learning_rate = 0.0005

enc_optim = torch.optim.Adam(enc.parameters(),lr=0.001)
dec_optim = torch.optim.Adam(dec.parameters(),lr=0.001)