import os, re
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
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
    acf_full = np.correlate(x, x, mode='full')  # lunghezza 2N - 1 (c'è lo 0)
    acf = acf_full[N - 1:N - 1 + max_lag]  # prende solo lag >= 0
    acf /= acf[0] # normalizza

    return acf


def stima_tau_exp_e_plot_acf_vs_L(data_dir):
    """
    Sceglie i paths da analizzare per L scelti dall'utente, plotta la acf, stima tau_exp per ogni L
    e plotta anche tau_exp in funzione di L.
    """
    file_paths = find_file_paths_interactive(data_dir)

    L_values = []
    tau_exp_values = []

    # plot per C(tau)
    plt.figure(figsize=(7, 5))

    for path in file_paths:
        data = np.loadtxt(path, skiprows=1)
        m = data[:, 1]

        # Estrai L dal nome del file
        match = re.search(r"L(\d+)_beta", os.path.basename(path))
        if match:
            L = int(match.group(1))
        else:
            raise ValueError(f"Impossibile estrarre L da {path}")

        max_lag = len(m) - 1
        acf = autocorrelation_function(m, max_lag=max_lag)
        lags = np.arange(max_lag)

        # Fit per stimare tau_exp
        try:
            popt, _ = curve_fit(exp_decay, lags, acf, p0=(1.0, 100.0))
            _, tau_exp = popt
            tau_exp = int(round(tau_exp))
        except RuntimeError:
            print(f"Fit fallito per L = {L}, si salta.")
            continue

        print(f"→ L = {L} → τ_exp = {tau_exp}\n")

        L_values.append(L)
        tau_exp_values.append(tau_exp)

        # Aggiungi curva C(tau) al plot
        plt.plot(lags, acf, label=f"L = {L}")

    plt.xlabel(r'$\tau$', fontsize=10)
    plt.ylabel(r'$C(\tau)$', fontsize=10)
    plt.title('Funzione di autocorrelazione $C(\\tau)$ per vari $L$', fontsize=10)
    plt.legend(fontsize=9)
    plt.grid(True)
    plt.tick_params(labelsize=10)
    plt.tight_layout()
    plt.show()

    # Ordina risultati per L
    L_values, tau_exp_values = zip(*sorted(zip(L_values, tau_exp_values)))

    # Plot tau_exp vs L
    plt.figure(figsize=(6, 4))
    plt.plot(L_values, np.array(tau_exp_values)/1e3, 'o-', label=r'$\tau_{\mathrm{exp}}(L)/10^{3}$')
    plt.xlabel(r'$L$', fontsize=10)
    plt.ylabel(r'$\tau_{\mathrm{exp}}$', fontsize=10)
    plt.title(r'Stima di $\tau_{\mathrm{exp}}$ in funzione di $L$', fontsize=10)
    plt.grid(True)
    plt.legend(fontsize=10)
    plt.tick_params(labelsize=10)
    plt.tight_layout()
    plt.show()

    return L_values, tau_exp_values


if __name__ == "__main__":

    data_dir = "../data-generation/results-tau-exp"

    L_vals, tau_exp_vals = stima_tau_exp_e_plot_acf_vs_L(data_dir)
    update_tau_exp_file(L_vals, tau_exp_vals, "tau_exp_results.txt")
