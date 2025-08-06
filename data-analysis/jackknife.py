import numpy as np

def jackknife_secondary_estimate(data, primary_funcs, secondary_func, k):
    """
    Stima media e errore jackknife su una variabile secondaria F = f(F1, ..., Fn),
    dove Fi sono medie di funzioni primarie applicate ai dati.

    Parametri:
        primary_funcs : list of callables
            Funzioni primarie F_i(x) da mediare (es. [lambda x: x, lambda x: x**2]).
        secondary_func : callable
            Funzione secondaria f(F1, ..., Fn) su cui si vuole stimare l'errore.
    """
    data = np.asarray(data)
    N = len(data)
    if k < 2 or k > N:
        raise ValueError(f"Numero di blocchi non valido: k={k}, deve essere 2 <= k <= {N}")
    
    M = N // k
    N_used = M * k

    data_used = data[:N_used]
    
    # si costruiscono i blocchi (autocorrelazioni)
    blocks = data_used.reshape(k, M)

    # prepara array per F_jackknife
    F_jk = []

    for i in range(k): # per ogni numero di blocchi costruisce il sample con il blocco i-esimo rimosso
        reduced_data = np.delete(blocks, i, axis=0).reshape((k - 1) * M)

        # calcola medie delle funzioni primarie sul sample ridotto e calcola la funzione secondaria
        primary_means = [np.mean(f(reduced_data)) for f in primary_funcs]
        F_i = secondary_func(*primary_means) # media calcolata sul sample senza il blocco i-esimo
        F_jk.append(F_i)

    F_jk = np.array(F_jk)
    F_mean = np.mean(F_jk) # media totale

    F_var = (k - 1) / k * np.sum((F_jk - F_mean)**2)
    F_error = np.sqrt(F_var) # calcolo della dev st

    return F_mean, F_error

