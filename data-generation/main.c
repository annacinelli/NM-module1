/* main: esegue la simulazione per un solo valore di L passato da riga di comando;
   per ciascun L si genera l’intervallo di beta e si salvano i risultati */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

#include "geometry.h"
#include "ising.h"
#include "random.h"
#include "utils.h"

#define MAX_LEN 200
#define BETA_C 0.4406867935


/* argc: numero di argomenti (incluso il nome del programma)
   argv: array di stringhe con gli argomenti ->
   argv[0] è il nome del programma (es. "./main");
   argv[1] è il primo argomento passato dall’utente (in questo caso L)*/

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <L>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int L = atoi(argv[1]); /* converte la stringa argv[1] in un intero (L) usando atoi() (ASCII to Integer) */
    if (L <= 0) {
        fprintf(stderr, "Errore: L deve essere un intero positivo.\n");
        return EXIT_FAILURE;
    }

    double m, e, p_lookup[4];
    int num_beta, b, step;
    const unsigned long long T = 50000000ULL; // 5 × 10^7 sweep dell'intero reticolo

    char tau_exp_path[] = "../data-analysis/tau_exp_results.txt";
    const unsigned long long TAU_MAX = read_tau_exp_from_file(L, tau_exp_path)/(L*L); // tau_exp per termalizzazione
    double *betas = generate_beta_range(L, &num_beta), beta;

    // inizializza RNG
    unsigned long initstate = (unsigned long) time(NULL);
    unsigned long initseq = 54;
    random_generator_init(initstate, initseq);

    for (b = 0; b < num_beta; b++) {
        beta = betas[b];

        // prepara cartelle e nomi file
        char base_name[MAX_LEN], out_path[MAX_LEN], sotto_cartella_results[256];
        snprintf(base_name, sizeof(base_name), "L%d_beta%.6f", L, beta);
        snprintf(sotto_cartella_results, sizeof(sotto_cartella_results), "results/%s", base_name);

        create_directory_if_needed("results");
        create_directory_if_needed(sotto_cartella_results);
        generate_unique_filename(sotto_cartella_results, base_name, out_path, MAX_LEN);

        // inizializza lookup Metropolis
        initialize_metropolis_lookup(beta, p_lookup);

        // inizializza reticolo
        int *lattice = create_lattice(L);
        initialize_lattice(L, lattice);

        FILE *fp = fopen(out_path, "w");
        if (!fp) {
            perror("Errore apertura file");
            exit(EXIT_FAILURE);
        }

        // scrive intestazione
        fprintf(fp, "# step\tm\tenergy\n");

        for (step = 0; step < T; step++) {
            metropolis_sweep(lattice, L, beta, p_lookup);

            if (step >= TAU_MAX) { /* salva ogni L^2 steps */
                m = compute_magnetization_volume(lattice, L);
                e = compute_energy_per_spin(lattice, L);
                fprintf(fp, "%d\t%.6f\t%.6f\n", step, m, e);
            }
        }

        fclose(fp);
        free_lattice(&lattice);
    }

    free(betas);
    return 0;
}

