import os
import re
from collections import defaultdict

def find_file_paths_interactive(data_dir):
    """
    Interfaccia interattiva per selezionare più file da results-tau-exp:
    - permette di scegliere uno o più L disponibili;
    - per ciascun L guida alla scelta della cartella e del file versione;
    - ritorna una lista di path completi dei file scelti.
    """
    folder_pattern = re.compile(r"^L(\d+)_beta([\d.]+)$")
    version_pattern = re.compile(r"_v(\d+)\.txt$")

    # Raggruppa cartelle per L
    gruppi_per_L = defaultdict(list)
    for folder_name in os.listdir(data_dir):
        match = folder_pattern.match(folder_name)
        if match:
            L = int(match.group(1))
            beta = float(match.group(2))
            folder_path = os.path.join(data_dir, folder_name)
            if os.path.isdir(folder_path):
                gruppi_per_L[L].append((folder_name, beta, folder_path))

    if not gruppi_per_L:
        raise RuntimeError(f"Nessuna cartella trovata in '{data_dir}' con formato L*_beta*")

    # Mostra valori di L disponibili
    L_disponibili = sorted(gruppi_per_L.keys())
    print("\nValori di L disponibili:")
    for i, L in enumerate(L_disponibili):
        print(f"{i}: L = {L} ({len(gruppi_per_L[L])} cartelle)")

    # Input multiplo: indici separati da spazio o "tutti"
    while True:
        scelta = input("\nSeleziona uno o più indici dei L desiderati (es. '0 2 3') oppure scrivi 'tutti': ").strip()
        if scelta.lower() == 'tutti':
            idx_scelti = list(range(len(L_disponibili)))
            break
        try:
            idx_scelti = list(map(int, scelta.split()))
            if all(0 <= idx < len(L_disponibili) for idx in idx_scelti):
                break
            else:
                print("Alcuni indici non validi. Riprova.")
        except ValueError:
            print("Input non valido. Riprova.")

    file_paths = []

    for idx_L in idx_scelti:
        L_scelto = L_disponibili[idx_L]
        cartelle_per_L = gruppi_per_L[L_scelto]

        # Se ci sono più cartelle, chiedo quale scegliere
        if len(cartelle_per_L) > 1:
            print(f"\nCartelle disponibili per L = {L_scelto}:")
            for i, (name, beta, _) in enumerate(cartelle_per_L):
                print(f"{i}: {name} (beta = {beta})")
            while True:
                try:
                    idx_cartella = int(input("Seleziona l’indice della cartella desiderata: "))
                    if 0 <= idx_cartella < len(cartelle_per_L):
                        break
                    else:
                        print("Indice non valido. Riprova.")
                except ValueError:
                    print("Input non valido. Inserisci un numero intero.")
        else:
            idx_cartella = 0

        folder_name, beta, folder_path = cartelle_per_L[idx_cartella]

        # Trova versioni disponibili
        files = [f for f in os.listdir(folder_path) if f.startswith(folder_name) and version_pattern.search(f)]
        versions = []
        for f in files:
            m = version_pattern.search(f)
            if m:
                versions.append((int(m.group(1)), f))
        versions.sort()

        if not versions:
            print(f"Nessun file versione trovato in '{folder_name}'. Skipping.")
            continue

        print(f"\nVersioni disponibili per {folder_name}:")
        for v, fname in versions:
            print(f"v{v}  →  {fname}")

        available_versions = [v for v, _ in versions]

        while True:
            try:
                v_scelta = int(input("Inserisci il numero della versione desiderata (es. 3 per _v3.txt): "))
                if v_scelta in available_versions:
                    break
                else:
                    print("Versione non disponibile. Riprova.")
            except ValueError:
                print("Input non valido. Inserisci un numero intero.")

        fname_scelto = f"{folder_name}_v{v_scelta}.txt"
        full_path = os.path.join(folder_path, fname_scelto)
        print(f"File selezionato per L = {L_scelto}: {full_path}\n")

        file_paths.append(full_path)

    return file_paths


def update_tau_exp_file(L_values, tau_exp_values, results_path):
    """
    Crea o aggiorna un file .txt con due colonne: L   tau_exp.
    Se il file esiste, aggiorna solo gli L già presenti e aggiunge i nuovi.
    Se non esiste, lo crea da zero.
    """
    risultati = {}

    # Se esiste, leggi contenuto precedente
    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    try:
                        L, tau = map(int, line.strip().split()[:2])
                        risultati[L] = tau
                    except ValueError:
                        continue

    # Aggiungi o sovrascrivi con i nuovi valori
    for L, tau in zip(L_values, tau_exp_values):
        risultati[L] = tau

    # Scrivi su file
    with open(results_path, "w") as f:
        f.write("# L    tau_exp\n")
        for L in sorted(risultati):
            f.write(f"{L:<4} {risultati[L]}\n")


