""" Analisi dati Ising 2D: date le serie temporali per m, e, si vuole calcolare:
    - la suscettibilità ' e non ' (serve av(m^2), av(|m|)^2)
    - calore specifico (serve av(e^2), av(e)^2)
    - U (cumulante di Binder) (serve av(m^4), av(m^2)^2)
    - av(m), av(|m|)

    vanno tutti plottati in funzione di beta, quindi per si crea un ulteriore file .txt estreno alle cartelle in cui mettere 
    av(m), av(|m|), ..., come funzioni di beta

    - Plots
"""
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from blocking import blocking_with_k_blocks
from jackknife import jackknife_secondary_estimate


def get_latest_file(folder, pattern):
    matches = [f for f in os.listdir(folder) if re.match(pattern, f)]
    if not matches:
        return None
    # Ordina in base alla versione finale (es. file_v3.txt -> 3)
    matches.sort(key=lambda f: int(re.search(r'_v(\d+)\.txt$', f).group(1)))
    return os.path.join(folder, matches[-1])


def analyze_all_results(base_dir='results', k=16, output_file='osservabili.txt'):
    results = []

    for subfolder in sorted(os.listdir(base_dir)):
        full_path = os.path.join(base_dir, subfolder)
        if not os.path.isdir(full_path):
            continue

        match = re.search(r'beta([0-9.]+)', subfolder)
        if not match:
            continue
        beta = float(match.group(1))

        latest_file = get_latest_file(full_path, r'^data_v\d+\.txt$')
        if latest_file is None:
            continue

        try:
            data = np.loadtxt(latest_file)
        except Exception as e:
            print(f"Errore nel leggere {latest_file}: {e}")
            continue

        if data.ndim == 1 or data.shape[1] < 3:
            print(f"Dati insufficienti in {latest_file}")
            continue

        m = data[:, 1]
        e = data[:, 2]

        # Osservabili primarie
        m_mean, m_err = blocking_with_k_blocks(m, k)
        abs_m_mean, abs_m_err = blocking_with_k_blocks(m, k, func=np.abs)

        # Osservabili secondarie con jackknife
        L = int(re.search(r'L(\d+)', subfolder).group(1))
        V = L**2

        chi_p, chi_p_err = jackknife_secondary_estimate(
            m, [lambda x: x**2, lambda x: np.abs(x)],
            lambda m2, abs_m: V * (m2 - abs_m**2), k)

        chi, chi_err = jackknife_secondary_estimate(
            m, [lambda x: x**2], lambda m2: V * m2, k)

        C, C_err = jackknife_secondary_estimate(
            e, [lambda x: x**2, lambda x: x],
            lambda e2, e_: V * (e2 - e_**2), k)

        U, U_err = jackknife_secondary_estimate(
            m, [lambda x: x**4, lambda x: x**2],
            lambda m4, m2: m4 / m2**2, k)

        results.append((beta, m_mean, m_err, abs_m_mean, abs_m_err,
                        chi_p, chi_p_err, chi, chi_err, C, C_err, U, U_err))

    results.sort()

    with open(output_file, 'w') as f:
        f.write("# beta   <m> ± err   <|m|> ± err   χ' ± err   χ ± err   C ± err   U ± err\n")
        for r in results:
            f.write("{:8.6f}  {: .6f} {: .6f}  {: .6f} {: .6f}  {: .6f} {: .6f}  {: .6f} {: .6f}  {: .6f} {: .6f}  {: .6f} {: .6f}\n".format(*r))


def plot_observable_vs_beta(root_dir='analyzed_results', observable_index=1, observable_label='<m>', ylabel='⟨m⟩'):
    """
    Plotta un'osservabile in funzione di beta per ogni L.

    Parametri:
        root_dir : str
            Directory dove si trovano le cartelle L*/ con i file observables_vX.txt
        observable_index : int
            Indice dell'osservabile da plottare (1 per <m>, 2 per <m|>, 3 per χ', ecc.)
        observable_label : str
            Etichetta nel file da usare per la legenda
        ylabel : str
            Etichetta dell'asse y
    """
    plt.figure(figsize=(8,6))

    for folder in sorted(os.listdir(root_dir)):
        if not folder.startswith("L"):
            continue
        L = int(folder[1:])
        subfolder = os.path.join(root_dir, folder)

        # Trova il file più recente observables_vX.txt
        files = [f for f in os.listdir(subfolder) if re.match(r'observables_v\d+\.txt', f)]
        if not files:
            continue
        files.sort(key=lambda f: int(re.search(r'_v(\d+)', f).group(1)))
        latest_file = os.path.join(subfolder, files[-1])

        # Carica i dati
        beta, obs, obs_err = [], [], []
        with open(latest_file) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                cols = line.strip().split()
                beta.append(float(cols[0]))
                value = float(cols[1 + 2 * observable_index])
                err = float(cols[2 + 2 * observable_index])
                obs.append(value)
                obs_err.append(err)

        plt.errorbar(beta, obs, yerr=obs_err, label=f"L={L}", fmt='o-', capsize=3)

    plt.xlabel(r'$\beta$')
    plt.ylabel(ylabel)
    plt.title(f'{ylabel} vs $\\beta$ per ogni L')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

