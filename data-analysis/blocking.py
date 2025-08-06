import numpy as np
import matplotlib.pyplot as plt


def blocking_with_k_blocks(data, k, func = lambda x: x):
    """
    In input:
        data, il numero di blocchi k e la funzione F
        func : callable (default: identità)
             - una lambda function è un modo rapido per definire una funzione anonima, 
             cioè senza darle un nome esplicito, direttamente nel punto in cui serve
    """
    data = np.asarray(data)
    N = len(data)

    if k < 2 or k > N: # controllo
        raise ValueError(f"Numero di blocchi non valido: k={k}, deve essere 2 <= k <= {N}")

    M = N // k  # se non divisibile si prende la parte intera inferiore
    N_used = M * k # lunghezza effettiva del sample, k blocchi da N_used/k elementi

    Fx = func(data[:N_used]) # un array
    blocks = Fx.reshape(k, M) # la divide in una matrice di forma (k, M), ogni riga è un blocco

    block_means = np.mean(blocks, axis=1) # media degli elementi nei singoli blocchi
    mean_F = np.mean(block_means) # media delle medie dei singoli blocchi, stimatore di av(F)

    squared_diffs = np.sum((block_means - mean_F)**2)
    error = np.sqrt(squared_diffs / (k * (k - 1))) # stimatore per la dev st di mean_F

    return mean_F, error