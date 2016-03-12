import string
import os
import numpy as np

directory = os.path.dirname(os.path.abspath(__file__))
f = open(directory + "/shakespeare.txt", 'r')

def forwards(A, E, Y, start):
    alphas = []
    alphas.append(start * E[Y[0]])
    
    for t in range(1, len(Y)):
        alpha = []
        for j in range(len(alphas[t-1])):
            alpha_a = 0
            for i in range(len(alphas[t-1])):
                alpha_a += E[Y[t]][j] * alphas[t-1][i] * A[i][j]
            alpha.append(alpha_a)
        alphas.append(np.array(alpha))
    
    return np.array(alphas)
    
def backwards(A, E, Y):
    betas = []
    betas.append([1 for i in range(len(start))])
    
    for t in range(1, len(Y)):
        beta = []
        for i in range(len(betas[0])):
            beta_ab = 0
            for j in range(len(betas[0])):
                beta_ab += betas[0][j] * A[i][j] * E[Y[t]][j]
            beta.append(beta_ab)
        betas.insert(0, np.array(beta))
    
    return np.array(betas)

d = {}
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
        if word not in d:
            d[word] = index
            index += 1
        order.append(d[word])
    O.append(np.array(order))

O = np.array(O)
num_states = 100
start = np.array([1.0 / num_states for _ in range(num_states)])
A = [np.array([1.0 / num_states for _ in range(num_states)]) for _ in range(num_states)]
E = [np.array([1.0 / len(d) for _ in range(num_states)]) for _ in range(len(d))]

idx = 0
while idx < 5:
    gammas = []
    xis = []
    
    for Y in O:
        alphas = forwards(A, E, Y, start)
        betas = backwards(A, E, Y)
        
        numerator = alphas * betas
        #numerator = np.multiply (alphas, betas)
        denom = np.sum(alphas * betas, axis=1)
        #denom = np.sum(np.multiply(alphas, betas), axis=1)
        gamma = [numerator[t] / denom[t] for t in range(len(Y))]
        print denom
        
        denom = np.sum(alphas[len(alphas)-1])
        xi = []
        for t in range(len(Y) - 1):
            mat = []
            for i in range(num_states):
                row = []
                for j in range(num_states):
                    numerator = alphas[t][i] * A[i][j] * betas[t+1][j] * E[Y[t+1]][j]
                    row.append(numerator / denom)
                mat.append(row)
            xi.append(mat)
    
        gammas.append(np.array(gamma))
        xis.append(np.array(xi))
    start = np.sum(gammas, axis=0)[0]
    
    a_nums = np.sum(np.sum(xis, axis=1), axis=0)
    a_denoms = np.sum(np.sum(gammas, axis=1), axis=0)
    for i in range(num_states):
        for j in range(num_states):
            A[i][j] = a_nums[i][j] / a_denoms[i]
        
    e_denoms = np.sum(np.sum(gammas, axis=1), axis=0)
    # NEED TO GET E_NUMERATORS
    print A
    print E
    gamma = np.array(gamma)
    xi = np.array(xi)
    start = gamma[0]
    
    numerator = np.sum(xi, axis=0)
    denom = np.sum(gamma, axis=0)
    #print denom
    A = [numerator[i] / denom[i] for i in range(num_states)]
    
    gamma_sum = np.sum(gamma, axis=0)
    for v in range(len(d)):
        for i in range(num_states):
            numerator = 0
            for t in range(len(Y)):
                if Y[t] == i:
                    numerator += gamma[t][i]
            E[v][i] = numerator / gamma_sum[i]
    #print A
    #print E
    idx += 1
    