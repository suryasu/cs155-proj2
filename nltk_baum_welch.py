import string
import os
import numpy as np
import nltk.tag.hmm as hmm
from nltk.corpus import cmudict

def num_syllables(word):
    word = word.lower()
    while word not in d:
        word = word[:len(word)-1]
    if len(word) == 0:
        return 1
    return max([len([y for y in x if y[-1].isdigit()]) for x in d[word]])

directory = os.path.dirname(os.path.abspath(__file__))
f = open(directory + "/shakespeare.txt", 'r')
d = cmudict.dict()

words = []
index = 0
order = []
O = []

for line in f:
    line = line.strip()
    if  line == "" or line[0] in string.digits:
        continue
    order = []
    line = "".join(l for l in line if l not in string.punctuation)
    line = string.lower(line)
    line = line.split()

    for word in line:
        try:
            idx = words.index(word)
        except ValueError:
            idx = len(words)
            words.append(word)
        order.append((idx, None))
    O.append(np.array(order))

num_samples = 20
O = np.array(O)
hmmt = hmm.HiddenMarkovModelTrainer(states=range(num_samples), symbols=range(len(words)))
model = hmmt.train_unsupervised(O, max_iterations=50)

# get probability of emission j given state i
for i in range(num_samples):
    total = 0
    for j in range(len(words)):
        total += model._outputs[i].prob(j)
    assert (abs(total - 1.0) < 1e-6)

# get probability of transitioning to state j from state i
for i in range(num_samples):
    total = 0
    for j in range(num_samples):
        total += model._transitions[i].prob(j)
    assert (abs(total - 1.0) < 1e-6)

# i = 0
# get random emission given state i
# print model._outputs[i].generate()

# get random transition given current state i
# print model._transitions[i].generate()

poem = ""
for i in range(14):
    next_item = model._priors.generate()
    word = words[model._outputs[next_item].generate()]
    poem += word
    syllables = num_syllables(word)
    while syllables < 10:
        next_item = model._transitions[next_item].generate()
        word = words[model._outputs[next_item].generate()]
        while (syllables + num_syllables(word) > 10):
            word = words[model._outputs[next_item].generate()]
        poem += " " + word
        syllables += num_syllables(word)
    poem += "\n"

print poem

