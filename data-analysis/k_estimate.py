import numpy as np
import os
from utils import find_file_paths_interactive, read_data_file
from plots import plot_estimated_error_vs_k


if __name__ == "__main__":
    # Vai nella cartella results/ partendo da data_analysis/
    base_dir = os.path.dirname(__file__)
    results_dir = os.path.abspath(os.path.join(base_dir, "../data-generation/results"))

    file_paths = find_file_paths_interactive(results_dir)

    # Range di k (modificabile)
    k_range = list(range(4, 51, 4))

    saturazioni_globali = []

    for path in file_paths:
        m, e = read_data_file(path)
        file_id = os.path.basename(path).replace(".txt", "")


        # Blocking
        k_sat = plot_estimated_error_vs_k(m, k_min=k_range[0], k_max=k_range[-1],
                                          func=lambda x: x, secondary=False)
        saturazioni_globali.append((file_id, "⟨m⟩", k_sat))

        k_sat = plot_estimated_error_vs_k(e, k_min=k_range[0], k_max=k_range[-1],
                                          func=lambda x: x, secondary=False)
        saturazioni_globali.append((file_id, "⟨e⟩", k_sat))

        k_sat = plot_estimated_error_vs_k(m, k_min=k_range[0], k_max=k_range[-1],
                                          func=np.abs, secondary=False)
        saturazioni_globali.append((file_id, "⟨|m|⟩", k_sat))

        k_sat = plot_estimated_error_vs_k(m, k_min=k_range[0], k_max=k_range[-1],
                                          func=lambda x: x**2, secondary=False)
        saturazioni_globali.append((file_id, "⟨m²⟩", k_sat))


        # Jackknife
        k_sat = plot_estimated_error_vs_k(m, k_min=k_range[0], k_max=k_range[-1],
                                          secondary=True,
                                          primary_functions=[lambda x: x**2, np.abs],
                                          secondary_function=lambda m2, abs_m: m2 - abs_m**2)
        saturazioni_globali.append((file_id, "χ′", k_sat))

        k_sat = plot_estimated_error_vs_k(m, k_min=k_range[0], k_max=k_range[-1],
                                          secondary=True,
                                          primary_functions=[lambda x: x, lambda x: x**2, lambda x: x**4],
                                          secondary_function=lambda m, m2, m4: 1 - m4 / (3 * m2**2))
        saturazioni_globali.append((file_id, "U", k_sat))

        k_sat = plot_estimated_error_vs_k(e, k_min=k_range[0], k_max=k_range[-1],
                                          secondary=True,
                                          primary_functions=[lambda x: x, lambda x: x**2],
                                          secondary_function=lambda e, e2: e2 - e**2)
        saturazioni_globali.append((file_id, "C", k_sat))


    # leggi risultati precedenti se esistono
    output_path = os.path.join(base_dir, "k_saturation.txt")
    mappa_saturazioni = {}  # (file_id, osservabile) → k

    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    try:
                        file_id, obs, k_str = line.strip().split(None, 2)
                        k_val = None if k_str == "NA" else int(k_str)
                        mappa_saturazioni[(file_id, obs)] = k_val
                    except Exception:
                        continue

    # aggiorna o aggiungi i nuovi risultati
    for file_id, obs, k in saturazioni_globali:
        mappa_saturazioni[(file_id, obs)] = k

    # riscrivi il file aggiornato
    with open(output_path, "w") as f:
        f.write("# file_id                      osservabile     k_saturazione\n")
        for (file_id, obs), k in sorted(mappa_saturazioni.items()):
            f.write(f"{file_id:<30} {obs:<14} {k if k is not None else 'NA'}\n")

    print(f"\n>> Risultati aggiornati in: {output_path}")
