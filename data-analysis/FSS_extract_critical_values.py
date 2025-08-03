""" Stima di beta_c, 1/nu, gamma:
    - dobbiamo cercare il max di xi' per un dato L, con beta, farlo per ogni L;
    fittando i valori al picco in funzione di L, l'intercetta ci dà beta_c,
    e poi si ottiene 1/nu,
    - fittando i valori al picco si stima gamma/nu
    - dalla procedura FSS per il av(|m|) si ottiene beta

    -> check con il collpase plot (anche check iniziale)

    - in realtà per le leggi di scala ne bastano due di esponenti critici

    -> * 

"""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
import re
from scipy.interpolate import interp1d
from scipy.optimize import brentq

def chi_prime_parabola(beta, a, beta_pc, chi_max):
    return a * (beta - beta_pc)**2 + chi_max

def fit_peak_parabola_single_L(file_path, L, observable_column_index=5, err_column_index=6, window=5, plot=True):
    """
    Fit parabolico locale di χ'(β) per un singolo L, da file observables_vX.txt.

    Ritorna:
        beta_pc, err_beta_pc, chi_max, err_chi_max
    """
    beta_vals, chi_vals, chi_errs = [], [], []

    with open(file_path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.strip().split()
            beta_vals.append(float(cols[0]))
            chi_vals.append(float(cols[observable_column_index]))
            chi_errs.append(float(cols[err_column_index]))

    beta_vals = np.array(beta_vals)
    chi_vals = np.array(chi_vals)
    chi_errs = np.array(chi_errs)

    idx_max = np.argmax(chi_vals)
    i_start = max(0, idx_max - window)
    i_end = min(len(beta_vals), idx_max + window + 1)

    beta_fit = beta_vals[i_start:i_end]
    chi_fit = chi_vals[i_start:i_end]
    err_fit = chi_errs[i_start:i_end]

    popt, pcov = curve_fit(chi_prime_parabola, beta_fit, chi_fit, sigma=err_fit, absolute_sigma=True)
    a, beta_pc, chi_max = popt
    err_a, err_beta_pc, err_chi_max = np.sqrt(np.diag(pcov))

    if plot:
        beta_dense = np.linspace(beta_fit[0], beta_fit[-1], 200)
        chi_dense = chi_prime_parabola(beta_dense, *popt)
        plt.errorbar(beta_fit, chi_fit, yerr=err_fit, fmt='o', label='data')
        plt.plot(beta_dense, chi_dense, '-', label='fit')
        plt.axvline(beta_pc, color='r', linestyle='--', label=r'$\beta_{pc}$')
        plt.title(f"Parabolic fit of χ' for L = {L}")
        plt.xlabel(r"$\beta$")
        plt.ylabel(r"$\chi'(\beta)$")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return beta_pc, err_beta_pc, chi_max, err_chi_max


def extract_fit_data_all_L(root_dir='analyzed_results', observable_column_index=5, err_column_index=6, window=5, plot=False):
    """
    Esegue il fit parabolico per tutti i file observables_vX.txt trovati in analyzed_results/L*/

    Ritorna:
        Lista di tuple: (L, beta_pc, err_beta_pc, chi'_max, err_chi'_max)
    """
    results = []

    for folder in sorted(os.listdir(root_dir)):
        if not folder.startswith("L"):
            continue
        L = int(folder[1:])
        subfolder = os.path.join(root_dir, folder)

        files = [f for f in os.listdir(subfolder) if re.match(r'observables_v\d+\.txt', f)]
        if not files:
            continue
        files.sort(key=lambda f: int(re.search(r'_v(\d+)', f).group(1)))
        file_path = os.path.join(subfolder, files[-1])

        try:
            beta_pc, err_beta_pc, chi_max, err_chi_max = fit_peak_parabola_single_L(
                file_path, L, observable_column_index, err_column_index, window, plot=plot
            )
            results.append((L, beta_pc, err_beta_pc, chi_max, err_chi_max))
        except Exception as e:
            print(f"[L={L}] Fit fallito: {e}")

    results.sort()
    return results


def fit_beta_pc_vs_L(L_array, beta_pc_array, err_beta_pc_array, plot=True):
    """
    Fit di beta_pc(L) = beta_c + b * L^{-1/nu}
    Ritorna: beta_c, err_beta_c, 1/nu, err_1/nu
    """
    def fit_func(L, beta_c, b, inv_nu):
        return beta_c + b * L**(-inv_nu)

    popt, pcov = curve_fit(fit_func, L_array, beta_pc_array, sigma=err_beta_pc_array, absolute_sigma=True)
    beta_c, b, inv_nu = popt
    err_beta_c, _, err_inv_nu = np.sqrt(np.diag(pcov))

    if plot:
        L_dense = np.linspace(min(L_array), max(L_array), 300)
        plt.errorbar(L_array, beta_pc_array, yerr=err_beta_pc_array, fmt='o', label='dati')
        plt.plot(L_dense, fit_func(L_dense, *popt), '-', label='fit')
        plt.xlabel("L")
        plt.ylabel(r"$\beta_{\mathrm{pc}}(L)$")
        plt.title(r"Fit: $\beta_{\mathrm{pc}}(L) \approx \beta_c + b L^{-1/\nu}$")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return beta_c, err_beta_c, 1/inv_nu, err_inv_nu / (inv_nu**2)


def fit_chi_max_vs_L(L_array, chi_max_array, err_chi_max_array, plot=True):
    """
    Fit di chi'_max(L) = c0 + c1 * L^{gamma/nu}
    Ritorna: gamma/nu, err_gamma/nu
    """
    def fit_func(L, c0, c1, gamma_su_nu):
        return c0 + c1 * L**gamma_su_nu

    popt, pcov = curve_fit(fit_func, L_array, chi_max_array, sigma=err_chi_max_array, absolute_sigma=True)
    c0, c1, gamma_su_nu = popt
    err_c0, err_c1, err_gamma_su_nu = np.sqrt(np.diag(pcov))

    if plot:
        L_dense = np.linspace(min(L_array), max(L_array), 300)
        plt.errorbar(L_array, chi_max_array, yerr=err_chi_max_array, fmt='o', label='dati')
        plt.plot(L_dense, fit_func(L_dense, *popt), '-', label='fit')
        plt.xlabel("L")
        plt.ylabel(r"$\chi'_{\mathrm{max}}(L)$")
        plt.title(r"Fit: $\chi'_{\mathrm{max}}(L) \approx c_0 + c_1 L^{\gamma/\nu}$")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return gamma_su_nu, err_gamma_su_nu


def estimate_betac_from_binder_crossings(root_dir='analyzed_results', observable_column_index=11, plot=True):
    """
    Stima beta_c dal crossing di U(beta) tra taglie L consecutive.
    
    Parametri:
        observable_column_index: colonna di U(beta) nei file observables_vX.txt
    
    Ritorna:
        lista di stime beta_c da crossing
    """
    binder_data = {}

    # Leggi tutti i dati
    for folder in sorted(os.listdir(root_dir)):
        if not folder.startswith("L"):
            continue
        L = int(folder[1:])
        subfolder = os.path.join(root_dir, folder)

        files = [f for f in os.listdir(subfolder) if re.match(r'observables_v\d+\.txt', f)]
        if not files:
            continue
        files.sort(key=lambda f: int(re.search(r'_v(\d+)', f).group(1)))
        file_path = os.path.join(subfolder, files[-1])

        beta_vals, U_vals = [], []
        with open(file_path) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                cols = line.strip().split()
                beta_vals.append(float(cols[0]))
                U_vals.append(float(cols[observable_column_index]))

        binder_data[L] = (np.array(beta_vals), np.array(U_vals))

    # Ordina L e stima crossing per L1 < L2
    Ls = sorted(binder_data.keys())
    beta_crossings = []

    for i in range(len(Ls) - 1):
        L1, L2 = Ls[i], Ls[i + 1]
        beta1, U1 = binder_data[L1]
        beta2, U2 = binder_data[L2]

        # Interpolazioni continue
        f1 = interp1d(beta1, U1, kind='cubic')
        f2 = interp1d(beta2, U2, kind='cubic')

        # Trova intervallo comune
        beta_min = max(beta1[0], beta2[0])
        beta_max = min(beta1[-1], beta2[-1])

        try:
            # Trova root della differenza
            root = brentq(lambda b: f1(b) - f2(b), beta_min, beta_max)
            beta_crossings.append(root)
        except ValueError:
            print(f"Crossing non trovato tra L={L1} e L={L2}")

    if plot:
        plt.figure(figsize=(8,6))
        for L in Ls:
            beta, U = binder_data[L]
            plt.plot(beta, U, label=f"L={L}")
        for b in beta_crossings:
            plt.axvline(b, color='gray', linestyle='--')
        plt.xlabel(r"$\beta$")
        plt.ylabel("Binder cumulant $U$")
        plt.title("Crossing del cumulante di Binder")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return beta_crossings


def plot_fig_5_5(L_array, beta_pc_array, beta_pc_err, chi_max_array, chi_max_err):
    fig, ax1 = plt.subplots(figsize=(8, 6))

    color = 'tab:blue'
    ax1.set_xlabel("L")
    ax1.set_ylabel(r"$\beta_{\mathrm{pc}}(L)$", color=color)
    ax1.errorbar(L_array, beta_pc_array, yerr=beta_pc_err, fmt='o', color=color, label=r"$\beta_{\mathrm{pc}}(L)$")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel(r"$\chi'_{\mathrm{max}}(L)$", color=color)
    ax2.errorbar(L_array, chi_max_array, yerr=chi_max_err, fmt='s', color=color, label=r"$\chi'_{\mathrm{max}}(L)$")
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title("Figura 5.5: $\chi'_{\max}(L)$ e $\\beta_{pc}(L)$")
    plt.show()


def plot_fig_5_6(L_array, beta_pc_array, beta_pc_err, chi_max_array, chi_max_err,
                 beta_c_fit, err_beta_c, nu_fit, err_nu, gamma_fit, err_gamma):
    
    logL = np.log(L_array)

    # Fit log-log di βpc
    inv_nu_fit = 1 / nu_fit
    beta_pc_fit = beta_c_fit + (beta_pc_array[0] - beta_c_fit) * (L_array[0] / L_array)**inv_nu_fit

    # Fit log-log di χ'max
    gamma_su_nu = gamma_fit / nu_fit
    chi_max_fit = chi_max_array[0] * (L_array / L_array[0])**gamma_su_nu

    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.errorbar(logL, beta_pc_array, yerr=beta_pc_err, fmt='o', color='tab:blue', label=r"$\beta_{pc}(L)$")
    ax1.plot(logL, beta_pc_fit, '--', color='tab:blue', label='fit βpc')
    ax1.set_xlabel(r"$\log L$")
    ax1.set_ylabel(r"$\beta_{pc}(L)$", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.errorbar(logL, chi_max_array, yerr=chi_max_err, fmt='s', color='tab:red', label=r"$\chi'_{\mathrm{max}}(L)$")
    ax2.plot(logL, chi_max_fit, '--', color='tab:red', label='fit $\chi_{\max}$')
    ax2.set_ylabel(r"$\chi'_{\mathrm{max}}(L)$", color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.tight_layout()
    plt.title("Figura 5.6: Fit di scaling critico")
    plt.show()
