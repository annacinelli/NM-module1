# NM-module1
2d Ising model: determination of critical properties (Metropolis single site update)

Simulazione in **C** del modello di Ising 2D con **Metropolis single-site update** per la determinazione delle proprietà critiche via Monte Carlo.

---

## Struttura delle cartelle

```
2d_ising_project/
├── data-generation/        # Codice C per la simulazione Monte Carlo
│   ├── main.c              # Entry point
│   ├── ising.c             # Funzioni core Ising
│   ├── ising.h             # Header funzioni ising.c
│   ├── rng.c               # Generatore numeri casuali (pcg32)
│   ├── rng.h               # Header funzioni rng.c
│   ├── utils.c             # Funzioni di utilità I/O e analisi base
│   ├── utils.h             # Header funzioni utils.c
│   └── Makefile            # Compilazione
└── data-analysis/          # Analisi dati (Python/Julia)
    ├── analyze.py          # Analisi binning, errori, plot
    └── plot.ipynb          # Analisi interattiva opzionale
```

---

## Funzionalità principali

### `main.c`

* Legge parametri da riga di comando (`L`, `T`, `num_sweep`, `seed`).
* Inizializza il lattice.
* Esegue termalizzazione.
* Esegue sweep di misura con calcolo energia e magnetizzazione.
* Salva risultati in CSV/binario per l'analisi.

---

## File e funzioni

### `ising.h` / `ising.c`

Contiene le funzioni core del **modello di Ising 2D**:

* `void initialize_lattice(int L, int *lattice);`
  Inizializza il lattice con spin up o configurazione random.

* `double calculate_energy(int L, int *lattice);`
  Calcola l'energia totale del sistema.

* `double calculate_magnetization(int L, int *lattice);`
  Calcola la magnetizzazione media per configurazione.

* `void metropolis_sweep(int L, int *lattice, double beta);`
  Esegue uno sweep Metropolis single-site sul lattice a temperatura `T = 1/beta`.

---

### `rng.h` / `rng.c`

Wrapper del **generatore di numeri casuali**:

* `void seed_rng(uint64_t seed);`
  Inizializza il generatore con un seed.

* `double uniform();`
  Restituisce un numero casuale uniforme in `[0, 1)`.

---

### `utils.h` / `utils.c`

Funzioni di utilità per **I/O e statistiche**:

* `void save_array_to_file(const char *filename, double *array, int size);`
  Salva un array su file CSV/binario.

* `double compute_mean(double *data, int size);`
  Calcola la media di un array.

* `double compute_std(double *data, int size);`
  Calcola la deviazione standard di un array.

---

## Compilazione

```bash
cd data-generation
make
```

Genererà l'eseguibile `ising`.

---

## Esecuzione

```bash
./ising L T num_sweep seed
```

Esempio:

```bash
./ising 32 2.269 1000000 42
```

* `L`: dimensione lattice (es. 32)
* `T`: temperatura (es. 2.269)
* `num_sweep`: sweep Monte Carlo (es. 1,000,000)
* `seed`: seme RNG per riproducibilità

---

## Analisi dati

Usa `data-analysis/` per:

* Calcolo media, deviazione standard, errore statistico (binning, jackknife, bootstrap);
* Plot magnetizzazione, energia, calore specifico, suscettività;
* Stima `T_c` e degli esponenti critici tramite Finite Size Scaling.

---

## Riferimenti

* Claudio Bonati, *Numerical Methods for Physics* (2025)
* [claudio-bonati/NumericalMethods](https://github.com/claudio-bonati/NumericalMethods)
* Capitoli 3 e 5 del pdf per MCMC e Ising Model

---

## TODO

✅ Creare `ising.c`, `ising.h` con funzioni dichiarate.
✅ Creare `rng.c`, `rng.h` con wrapper `pcg32`.
✅ Creare `utils.c`, `utils.h` con funzioni di I/O.
✅ Scrivere `main.c` per orchestrare la simulazione.
✅ Eseguire test con lattice piccolo per validazione.
✅ Creare `analyze.py` per analisi automatizzata dei dati.

