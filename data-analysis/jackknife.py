""" file jackknife.py, funzioni per il jackknife: metodo la stima dell'errore
da associare alle variabili secondarie variabili secondarie (funzione di più F primarie, si ha sempre la stessa X, ma più F,
come il quadrato del valor medio di x^2, ..., quindi è una funzione di valori medi, variabili primarie).

Problema legato alla stima dell'incertezza: se si hanno più valori medi e si usa lo stesso sample statistico, le incertezze saranno correlate.
Jackknife: i mock samples sono generati in modo deterministico, assumiamo inizialmente i draws indipendenti e generiamo i samples rimuovendo un singolo punto, 
quindi abbiamo N samples di N-1 punti, che forniscono N stime delle osservabili primarie da cui si ottengono N stime di quelle secondarie; 
sia F_J il sample composto dalle N stime F_i, si può stimare la square fluctuation indotta dal cambiamento del sample rimuovendo un elemento.
+ autocorrelazioni: si divide il sample in k blocchi, poi si generano i Jackkinfe samples rimuovendo l'i-esimo blocco invece che i-esimo draw
(analogo al blocking, come se fossero indipendenti) """

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
    
    # Costruisci i blocchi
    blocks = data_used.reshape(k, M)

    # Prepara array per F_jackknife
    F_jk = []

    for i in range(k):
        # Costruisci sample con il blocco i-esimo rimosso
        reduced_data = np.delete(blocks, i, axis=0).reshape((k - 1) * M)

        # Calcola medie delle funzioni primarie sul sample ridotto e calcola la funzione secondaria
        primary_means = [np.mean(f(reduced_data)) for f in primary_funcs]
        F_i = secondary_func(*primary_means)
        F_jk.append(F_i)

    F_jk = np.array(F_jk)
    F_mean = np.mean(F_jk)
    F_var = (k - 1) / k * np.sum((F_jk - F_mean)**2)
    F_error = np.sqrt(F_var)

    return F_mean, F_error

