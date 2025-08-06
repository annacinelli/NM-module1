import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from collections import defaultdict
from blocking import blocking_with_k_blocks
from jackknife import jackknife_secondary_estimate


def plot_estimated_error_vs_k(data, k_min=2, k_max=50, func=lambda x: x,
                              secondary=False, primary_functions=None,
                              secondary_function=None):
    """
    Plotta la deviazione standard stimata della media campionaria in funzione di k.
    Se secondary = False → blocking, altrimenti (se True) jackknife.
    Ritorna il primo k dove l'errore si stabilizza (entro 1% relativo).
    """
    ks = []
    devst_means = []

    if not secondary:
        for k in range(k_min, k_max + 1):
            try:
                _, error = blocking_with_k_blocks(data, k, func=func)
                ks.append(k)
                devst_means.append(error)
            except ValueError:
                continue
    else:
        for k in range(k_min, k_max + 1):
            try:
                _, error = jackknife_secondary_estimate(data, primary_functions, secondary_function, k)
                ks.append(k)
                devst_means.append(error)
            except ValueError:
                continue

    # stima della saturazione
    k_saturazione = None
    for i in range(1, len(devst_means)):
        delta = abs(devst_means[i] - devst_means[i - 1])
        if devst_means[i - 1] != 0:
            rel_delta = delta / abs(devst_means[i - 1])
            if rel_delta < 0.01:
                k_saturazione = ks[i]
                break

    plt.figure(figsize=(7, 4))
    plt.plot(ks, devst_means, marker='o')
    plt.xlabel("Numero di blocchi k")
    plt.ylabel("Deviazione standard stimata della media campionaria")
    plt.title("Deviazione standard vs k")
    plt.grid(True)
    plt.show()

    return k_saturazione

# plots per P(m)
def extract_beta_from_foldername(foldername):
    try:
        parts = foldername.split("_beta")
        return float(parts[1])
    except Exception:
        return None


def extract_L_from_foldername(foldername):
    try:
        return int(foldername[1:].split("_")[0])
    except Exception:
        return None


def find_closest_folders(base_dir, target_betas):
    """
    Cerca per ogni L le cartelle con β più vicino ai valori target.
    Ritorna un dizionario: L -> {beta_target: folder_path}
    """
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    L_groups = {}
    for folder in folders:
        L = extract_L_from_foldername(folder)
        beta = extract_beta_from_foldername(folder)
        if L is not None and beta is not None:
            if L not in L_groups:
                L_groups[L] = []
            L_groups[L].append((beta, os.path.join(base_dir, folder)))

    closest = {}
    for L, beta_paths in L_groups.items():
        betas = np.array([bp[0] for bp in beta_paths]).reshape(-1, 1)
        target_betas_array = np.array(target_betas).reshape(-1, 1)
        dists = cdist(betas, target_betas_array)
        closest_indices = np.argmin(dists, axis=0)
        closest[L] = {target_betas[i]: beta_paths[closest_indices[i]][1] for i in range(len(target_betas))}
    return closest


def get_highest_version_file(folder):
    """
    Ritorna il file con versione maggiore nella cartella, es. m_v3.txt > m_v2.txt.
    """
    txt_files = [f for f in os.listdir(folder) if f.endswith(".txt") and "_v" in f]
    if not txt_files:
        return None
    versions = sorted(txt_files, key=lambda x: int(x.split("_v")[-1].split(".")[0]), reverse=True)
    return versions[0]


def plot_magnetization_histograms_two_subplots(results_dir, target_betas=[0.35, 0.5], bins=100, normalize=True, save_path=None):
    """
    Plotta due subplot: uno per β ≈ 0.35 e uno per β ≈ 0.5, con tutti i L in ciascuno.
    """
    folders = find_closest_folders(results_dir, target_betas)
    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for ax, beta in zip(axs, target_betas):
        for L, beta_dict in sorted(folders.items()):
            folder = beta_dict[beta]
            best_file = get_highest_version_file(folder)
            if not best_file:
                continue
            data = np.loadtxt(os.path.join(folder, best_file))
            m_values = data[:, 1]
            label = f"L={L}"
            ax.hist(
                m_values,
                bins=bins,
                density=normalize,
                alpha=0.6,
                edgecolor="black",
                linewidth=0,
                label=label,
                histtype="stepfilled",
            )
        ax.set_title(f"β ≈ {beta:.3f}")
        ax.set_xlabel("m")
        ax.legend(fontsize=8)

    axs[0].set_ylabel("P(m)")
    fig.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()



# collapse plots
def plot_collapse_from_file(txt_path, beta_c=0.4406868, nu=1, gamma=1.75, beta_exp=0.125, save_path=None):
    """
    Plotta i collapse plots di:
      - χ' (suscettività ridotta)
      - <|m|> (magnetizzazione assoluta)
      - χ  (suscettività tradizionale)
      - U  (cumulante di Binder)

    dai file observables_vX.txt
    """
    data = np.loadtxt(txt_path, comments="#")

    L = data[:, 0]
    beta = data[:, 1]
    abs_m = data[:, 4]
    err_abs_m = data[:, 5]
    chi_red = data[:, 10]
    err_chi_red = data[:, 11]
    chi = data[:, 8]
    err_chi = data[:, 9]
    U = data[:, 12]
    err_U = data[:, 13]

    # Asse x comune
    x = (beta - beta_c) * L**(1 / nu)

    # Scaling delle y
    y_chi_red = chi_red * L**(-gamma / nu)
    err_chi_red *= L**(-gamma / nu)

    y_m = abs_m * L**(beta_exp / nu)
    err_abs_m *= L**(beta_exp / nu)

    y_chi = chi * L**(-gamma / nu)
    err_chi *= L**(-gamma / nu)

    # U non scala, si usa direttamente

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    axs[0, 0].errorbar(x, y_chi_red, yerr=err_chi_red, fmt='o', capsize=3)
    axs[0, 0].set_title(r"Collapse: $\chi'$")
    axs[0, 0].set_ylabel(r"$\chi' \cdot L^{-\gamma/\nu}$")

    axs[0, 1].errorbar(x, y_m, yerr=err_abs_m, fmt='o', capsize=3)
    axs[0, 1].set_title(r"Collapse: $\langle |m| \rangle$")
    axs[0, 1].set_ylabel(r"$\langle |m| \rangle \cdot L^{\beta/\nu}$")

    axs[1, 0].errorbar(x, y_chi, yerr=err_chi, fmt='o', capsize=3)
    axs[1, 0].set_title(r"Collapse: $\chi$")
    axs[1, 0].set_ylabel(r"$\chi \cdot L^{-\gamma/\nu}$")

    axs[1, 1].errorbar(x, U, yerr=err_U, fmt='o', capsize=3)
    axs[1, 1].set_title(r"Collapse: $U$ (Binder)")
    axs[1, 1].set_ylabel(r"$U$")

    for ax in axs.flat:
        ax.set_xlabel(r"$(\beta - \beta_c) \cdot L^{1/\nu}$")
        ax.grid(True)

    plt.suptitle("Data Collapse — Ising 2D ($\nu=1$, $\gamma=7/4$, $\beta=1/8$)")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Figura salvata in: {save_path}")
    else:
        plt.show()



# plot delle osservabili
def plot_observables_vs_beta(txt_path, save_path_prefix=None):
    """
    Plotta vs beta per ciascun L:
    ⟨m⟩, ⟨|m|⟩, ⟨ε⟩, χ′, χ, U, C (con errori)
    """
    data = np.loadtxt(txt_path, comments="#")
    beta = data[:, 1]
    L = data[:, 0].astype(int)

    # Osservabili (dalla struttura di observables_vX.txt)
    m, err_m = data[:, 2], data[:, 3]
    abs_m, err_abs_m = data[:, 4], data[:, 5]
    e, err_e = data[:, 6], data[:, 7]
    chi, err_chi = data[:, 8], data[:, 9]
    chi_red, err_chi_red = data[:, 10], data[:, 11]
    U, err_U = data[:, 12], data[:, 13]
    C, err_C = data[:, 14], data[:, 15]

    # Raggruppa per L
    gruppi = defaultdict(list)
    for i, l in enumerate(L):
        gruppi[l].append(i)

    # Funzioni da plottare (nome, dati, errore)
    osservabili = [
        ("⟨m⟩", m, err_m),
        ("⟨|m|⟩", abs_m, err_abs_m),
        ("⟨ε⟩", e, err_e),
        ("χ′", chi_red, err_chi_red),
        ("χ", chi, err_chi),
        ("U", U, err_U),
        ("C", C, err_C),
    ]

    for nome, y, yerr in osservabili:
        plt.figure(figsize=(6, 4))
        for l, idxs in sorted(gruppi.items()):
            plt.errorbar(
                beta[idxs], y[idxs], yerr=yerr[idxs],
                label=f"L = {l}", marker='o', capsize=3
            )

        plt.title(f"{nome} vs $\\beta$")
        plt.xlabel(r"$\beta$")
        plt.ylabel(nome)
        plt.grid(True)
        plt.legend()
        if save_path_prefix:
            fname = f"{save_path_prefix}_{nome.replace('|', '').replace('⟨', '').replace('⟩', '').replace('′', 'p').replace('ε', 'eps')}.png"
            plt.savefig(fname, bbox_inches="tight")
            print(f"→ Salvato: {fname}")
        else:
            plt.show()



if __name__ == "__main__":
    plot_magnetization_histograms_two_subplots("../data-generation/results", target_betas=[0.35, 0.5], bins=100, normalize=True, save_path=None)