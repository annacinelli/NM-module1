import os
import re
import numpy as np
from blocking import blocking_with_k_blocks
from jackknife import jackknife_secondary_estimate
from utils import generate_unique_filename

BETA_C = 0.4406867935

BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data-generation/results"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data-analysis/analyzed_results"))

folder_pattern = re.compile(r"^L(\d+)_beta([0-9.]+)$")
version_pattern = re.compile(r"_v(\d+)\.txt$")

primary_functions = {
    "⟨m⟩": lambda m: m,
    "⟨e⟩": lambda e: e,
    "⟨|m|⟩": lambda m: np.abs(m),
    "⟨m²⟩": lambda m: m**2,
}
secondary_observables = {
    "⟨|m|⟩²": ([np.abs], lambda abs_m: abs_m**2),
    "χ′": ([lambda x: x**2, np.abs], lambda m2, abs_m: m2 - abs_m**2),
    "U": ([lambda x: x, lambda x: x**2, lambda x: x**4], lambda m, m2, m4: 1 - m4 / (3 * m2**2)),
    "C": ([lambda x: x, lambda x: x**2], lambda e, e2: e2 - e**2),
}


# ritorna un dizionario che mappa l'osservabile nel k corrispondente, per L maggiore e beta vicino e sotto il beta_c
def k_load(path_txt):
    if not os.path.exists(path_txt):
        raise FileNotFoundError("File saturazione_k.txt non trovato.")

    mappa = {}
    pattern = re.compile(r"L(\d+)_beta([0-9.]+)")

    with open(path_txt) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    records = []
    for line in lines:
        parts = line.split()
        match = pattern.match(parts[0])
        if not match:
            continue
        L = int(match.group(1))
        beta = float(match.group(2))
        osservabile = parts[1]
        k_val = None if parts[2] == "NA" else int(parts[2])
        records.append((L, beta, osservabile, k_val))

    if not records:
        raise ValueError("Nessuna riga valida trovata.")

    L_max = max(r[0] for r in records)
    beta_best = min((r[1] for r in records if r[0] == L_max), key=lambda b: abs(b - BETA_C))

    for L, beta, obs, k in records:
        if L == L_max and abs(beta - BETA_C) == abs(beta_best - BETA_C):
            mappa[obs] = k

    return mappa


# calcolo dei valori medi e errori delle varie quantità per ogni cartella i results, ultima versione dei files
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    k_map = k_load(os.path.join(BASE_DIR, "k_saturation.txt"))

    rows = []

    for folder in os.listdir(RESULTS_DIR):
        full_folder = os.path.join(RESULTS_DIR, folder)
        if not os.path.isdir(full_folder):
            continue

        match = folder_pattern.match(folder)
        if not match:
            continue
        L = int(match.group(1))
        beta = float(match.group(2))

        all_files = [f for f in os.listdir(full_folder) if version_pattern.search(f)]
        if not all_files:
            continue

        versions = sorted(((int(version_pattern.search(f).group(1)), f) for f in all_files), key=lambda x: x[0])
        _, file_name = versions[-1]
        file_path = os.path.join(full_folder, file_name)

        print(f"Analizzo {file_path}")
        data = np.loadtxt(file_path)
        m_values = data[:, 1]
        e_values = data[:, 2]

        row = [L, beta]

        # variabili primarie
        for name in primary_functions:
            k = k_map.get(name)
            try:
                mean, err = blocking_with_k_blocks(m_values, k, primary_functions[name])
                row.extend([mean, err])
            except Exception:
                row.extend([np.nan, np.nan])

        # variabili secondarie
        for name in secondary_observables:
            k = k_map.get(name)
            if name == "C":
                source = e_values
            else:
                source = m_values
            try:
                mean, err = jackknife_secondary_estimate(source, *secondary_observables[name], k)
                row.extend([mean, err])
            except Exception:
                row.extend([np.nan, np.nan])

        rows.append(row)

    output_file = generate_unique_filename(OUTPUT_DIR)
    print(f"→ Salvo risultati in: {output_file}")

    with open(output_file, "w") as f:
        header = [
            "L", "beta",
            "⟨m⟩", "err⟨m⟩", "⟨|m|⟩", "err⟨|m|⟩", "⟨m²⟩", "err⟨m²⟩",
            "⟨|m|⟩²", "err⟨|m|⟩²", "χ′", "errχ′", "U", "errU", "C", "errC"
        ]
        f.write("# " + "\t".join(header) + "\n")
        for row in rows:
            formatted = "\t".join(f"{x:.8f}" if isinstance(x, float) else str(x) for x in row)
            f.write(formatted + "\n")


if __name__ == "__main__":
    main()