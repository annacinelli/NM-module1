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
    mean_F = np.mean(block_means) # media delle medie dei singoli blocchi
    error = np.std(block_means, ddof=1) / np.sqrt(N / k) # deviazione standard rispetto alla media mean_F
    # ddof=1 specifica l’uso del denominatore corretto per la stima della varianza campionaria

    return mean_F, error


# itera per un range di valori di k e fa il plot
def plot_variance_of_sample_mean_vs_k(data, k_min=2, k_max=50, func=lambda x: x):
    """
    Plotta la varianza stimata della media campionaria in funzione di k
    """
    ks = []
    var_means = []

    for k in range(k_min, k_max + 1):
        try:
            _, error = blocking_with_k_blocks(data, k, func=func)
            ks.append(k)
            var_means.append(error**2)
        except ValueError:
            continue  # Salta k non validi

    plt.figure(figsize=(7, 4))
    plt.plot(ks, var_means, marker='o')
    plt.xlabel("Numero di blocchi k")
    plt.ylabel("Varianza stimata della media campionaria")
    plt.title("Blocking: varianza di ⟨F⟩ vs k")
    plt.grid(True)
    plt.show()
