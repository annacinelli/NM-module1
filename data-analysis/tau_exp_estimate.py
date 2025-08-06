import os, re
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from collections import defaultdict
from numpy.fft import fft, ifft
from utils import find_file_paths_interactive, update_tau_exp_file

BETA_C = 0.4406867935

"""
La funzione di autocorrelazione di una serie temporale misura quanto il valore in un certo istante 
è correlato con il valore a distanza di tempo τ.
- Se la serie è stazionaria, C(τ) dipende solo da τ, non da t.
- Per lag alti τ → N, il numero di coppie utilizzabili diminuisce ⇒ la C(τ) diventa rumorosa, si plotta
tutto, ma ci aspettiamo rumore per grandi τ (eventuale cutoff successivo).
"""

# modello in input alla funzione di fit per stimare il tempo caratteristico tau_exp
def exp_decay(tau, A, tau_exp):
    return A * np.exp(-tau / tau_exp)


# calcolo dell'autocorrelazione normalizzata (adimensionalità, confronto) di una serie temporale x
# ! se abbiamo due variabili e una ha correlazione maggiore, per onfrontarle bisogna considerare la
# scala delle fluttuaizoni delle singole variabili
def autocorrelation_function(x, max_lag):
    """
    Calcola l'autocorrelazione normalizzata per lag in [0, ..., max_lag - 1].
    - Essendo una catena di Markov, il lag è intero.
    - All'inizio sia la media che la varianza dipenderanno dal tempo, poi una volta raggiunta
    la stazionarietà non sarà così.
    """
    x = np.asarray(x)
    N = len(x)

    if max_lag >= N:
        raise ValueError("max_lag deve essere minore della lunghezza della serie.")

    # Centra la serie
    x = x - np.mean(x)

    # Calcola autocorrelazione (convoluzione discreta di due array laggati)
    f = fft(x, n=2*N)
    acf = np.real(ifft(f * np.conjugate(f)))[:max_lag]
    acf /= acf[0] # normalizza

    return acf


def stima_tau_exp_media_acf(data_dir, max_lag=None):
    """
    Per ogni L, prende tutte le run (più versioni), calcola e media le ACF,
    poi stima tau_exp da questa media.
    """
    file_paths = find_file_paths_interactive(data_dir)

    # Raggruppa i path per valore di L
    gruppi_per_L = defaultdict(list)
    for path in file_paths:
        match = re.search(r"L(\d+)_beta", os.path.basename(path))
        if match:
            L = int(match.group(1))
            gruppi_per_L[L].append(path)

    L_values = []
    tau_exp_values = []

    plt.figure(figsize=(7, 5))

    for L in sorted(gruppi_per_L.keys()):
        paths = gruppi_per_L[L]
        acf_list = []

        for path in paths:
            data = np.loadtxt(path, skiprows=1)
            m = data[:, 1]

            # imposta max_lag se non specificato
            if max_lag is None:
                max_lag_local = len(m)-1
            else:
                max_lag_local = min(max_lag, len(m) - 1)

            acf = autocorrelation_function(m, max_lag_local)
            acf_list.append(acf)

        # calcola media delle autocorrelazioni
        acf_array = np.array(acf_list)
        acf_mean = np.mean(acf_array, axis=0)
        lags = np.arange(len(acf_mean))

        # fit per tau_exp
        try:
            popt, _ = curve_fit(exp_decay, lags, acf_mean, p0=(1.0, 100.0))
            _, tau_exp = popt
            tau_exp = int(round(tau_exp))
        except RuntimeError:
            print(f"Fit fallito per L = {L}, si salta.")
            continue

        print(f"→ L = {L} → τ_exp = {tau_exp} (media su {len(paths)} run)\n")

        L_values.append(L)
        tau_exp_values.append(tau_exp)

        plt.plot(lags, acf_mean, linestyle= '-.', label=f"L = {L} (mean)")

    plt.xlabel(r'$\tau$', fontsize=14)
    plt.ylabel(r'$C(\tau)$', fontsize=14)
    plt.title('Autocorrelazione media $C(\\tau)$ per ogni $L$', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True)
    plt.tick_params(labelsize=12)
    plt.tight_layout()
    plt.show()

    return L_values, tau_exp_values



if __name__ == "__main__":

    data_dir = "../data-generation/results-tau-exp"

    L_vals, tau_exp_vals = stima_tau_exp_media_acf(data_dir)
    update_tau_exp_file(L_vals, tau_exp_vals, "tau_exp_results.txt")
