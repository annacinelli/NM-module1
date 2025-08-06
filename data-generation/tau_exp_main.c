/* generazione dati per stimare tau_exp: vanno storati a ogni step della simulazione:
si sceglie L da terminale e si prende un beta vicino a beta_c */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

#include "geometry.h"
#include "ising.h"
#include "random.h"
#include "utils.h"

/* Le macro sono sostituite prima della compilazione, quindi non occupano memoria a runtime -> viene sostitito il
valore in tutto il codice prima della compilazione (non possono essere modificate accidentalmente nel codice); 
utile per dichiarare array statici, ma non hanno tipo; una macro vale in tutto il progetto se messa in un header */
#define MAX_LEN 200
#define BETA  0.44068679 /* leggermente sotto beta_c */

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <L>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int L = atoi(argv[1]);
    if (L <= 0) {
        fprintf(stderr, "Errore: L deve essere un intero positivo.\n");
        return EXIT_FAILURE;
    }

    double m, e, p_lookup[4];
    const unsigned long long T = 50000000ULL * (L*L); // numero di sweep Metropolis (single update)

    /* inizializza generatore di numeri casuali */
    unsigned long initstate = (unsigned long) time(NULL);
    unsigned long initseq = 54;
    random_generator_init(initstate, initseq);

    // path e nomi di file
    char base_name[MAX_LEN], out_path[MAX_LEN], sotto_cartella_results[256];
    snprintf(base_name, sizeof(base_name), "L%d_beta%f", L, BETA);
    snprintf(sotto_cartella_results, sizeof(sotto_cartella_results), "results-tau-exp/%s", base_name);

    create_directory_if_needed("results-tau-exp");
    create_directory_if_needed(sotto_cartella_results);
    generate_unique_filename(sotto_cartella_results, base_name, out_path, MAX_LEN);

    // inizializza lookup table per Metropolis
    initialize_metropolis_lookup(BETA, p_lookup);

    // crea e inizializza reticolo
    int *lattice = create_lattice(L);
    initialize_lattice(L, lattice);

    // apre il file di output
    FILE *fp = fopen(out_path, "w");
    if (!fp) {
        perror("Errore apertura file di output");
        exit(EXIT_FAILURE);
    }

    // scrive intestazione
    fprintf(fp, "# step\tm\tenergy\n");

    // esegue T sweep singoli e salva magnetizzazione ed energia a ogni passo
    for (unsigned long long step = 0; step < T; step++) {
        int site = step % (L * L);
        /* mapping da indice lineare a coordinate bidimensionali */
        int i = site / L;
        int j = site % L;
        metropolis_sweep_single_update(lattice, L, BETA, p_lookup, i, j);

        m = compute_magnetization_volume(lattice, L);
        e = compute_energy_per_spin(lattice, L);
        fprintf(fp, "%llu\t%.8f\t%.8f\n", step, m, e);
    }

    fclose(fp);
    free_lattice(&lattice);

    return 0;
}
