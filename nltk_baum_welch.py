import string
import os
import numpy as np
import nltk.tag.hmm as hmm
from nltk.corpus import cmudict

# Generates Shakespearean Sonnets using NLTK


def num_syllables(word):
    ''' Counts the number of syllables in a word'''
    word = word.lower()
    while word not in d:
        # take off letters from the end until we find a word
        word = word[:len(word)-1]
    if len(word) == 0:
        # if it doesn't recognize the word at all, return 1 as default
        return 1
    return max([len([y for y in x if y[-1].isdigit()]) for x in d[word]])

directory = os.path.dirname(os.path.abspath(__file__))
shakespeare = open(directory + "/shakespeare.txt", 'r')
spenser = open(directory + "/spenser.txt", 'r')
d = cmudict.dict()

words = {} # dictionary of a word, and its frequency
O = [] # observations

# trains using both Shakespeare and Spenser. 
# use "for file_name in [shakespeare]" if only training on Shakespeare
for file_name in [shakespeare, spenser]:
    for line in file_name:
        line = line.strip()
        if  len(line) < 10:
            # This line is empty, or its the sonnet number
            continue
        order = [] # order of words in a line
        line = "".join(l for l in line if l not in string.punctuation)
        line = string.lower(line)
        line = line.split()
    
        for word in line:
            try:
                # try to see if the word is in the dictionary already
                idx = words.keys().index(word)
                words[word] += 1
            except ValueError:
                # if not, add the word
                idx = len(words)
                words[word] = 1
           # NLTK requires each  observation to be in the form (word, tag) 
            order.append((idx, None))
        O.append(np.array(order))

word_keys = words.keys() # the actual words
num_states = 20 # number of hidden states
O = np.array(O)
hmmt = hmm.HiddenMarkovModelTrainer(states=range(num_states), symbols=range(len(words)))
model = hmmt.train_unsupervised(O, max_iterations=200)
A = model._transitions # transitions
E = model._outputs # emissions

# get top 10 probable words for each hidden state
for i in range(num_states):
    probs = []
    for j in range(len(words)):
        probs.append((E[i].prob(j), j))
    probs.sort(reverse=True)
    top_words = [word_keys[k] for (_, k) in probs[:10]]
    print "State " + str(i) + " " + str(top_words)

# get probability of transitioning to state j from state i
for i in range(num_states):
    total = []
    for j in range(num_states):
        total.append(model._transitions[i].prob(j))
    print str(total)

# Generate a poem
poem = ""

for i in range(14):
    # get starting state
    next_item = model._priors.generate()
    word = word_keys[E[next_item].generate()]
    poem += word
    syllables = num_syllables(word)
    while syllables < 10:
        next_item = A[next_item].generate()
        word = word_keys[E[next_item].generate()]
        # keep generating words until syllable count of a line is <= 10
        while (syllables + num_syllables(word) > 10):
            word = word_keys[E[next_item].generate()]
        poem += " " + word
        syllables += num_syllables(word)
    poem += "\n"

print poem


