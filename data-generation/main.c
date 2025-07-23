/* main: si costruisce il reticolo per ogni coppia L, beta letta in params.txt; si lanciano le simulazioni e si storano
i risultati togliendo i primi tau_exp steps e poi salvando m ogni L^2 steps */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "geometry.h"
#include "ising.h"
#include "random.h"
#include "utils.h"

int main(void){

    int num_params, i, j, max_len = 200; /* num_params per avere il numero di combinazioni possibili */
    int tau_exp = 10000, T = 1000000; /* valutare....*/
    double m, e; /* per salvare la magnetizzazione per unità di volume */

    /* per prima cosa, bisogna estrarre le coppie possibili di (L, beta) con cui fare le simulazioni */
    Param *params = read_param_combinations("params.txt", &num_params);

    double p_lookup[5]; /* dichiarazione lookup table */

    /* inizializza il generatore con un seed variabile */
    unsigned long initstate = (unsigned long) time(NULL);  /* seme principale del generatore, controlla la sequenza */
    unsigned long initseq   = 54;  /* può essere qualsiasi numero, diverso da 0 */
    random_generator_init(initstate, initseq);

    /* loop delle simulazioni sulle coppie nelle strutture */
    for (i = 0; i < num_params; i++) {

        char base_name[100], out_path[100];
        sprintf(base_name, "L%d_beta%.6f", params[i].L, params[i].beta);
        char sotto_cartella_results[100];
        sprintf(sotto_cartella_results, "results/%s", base_name);

        create_directory_if_needed("results"); /* crea la cartella di base results */
        create_directory_if_needed(&sotto_cartella_results); /* crea la sottocartella corrispondente a (L, beta) estratti */
        generate_unique_filename("results", &base_name, &out_path, max_len);

        initialize_metropolis_lookup(params[i].beta, p_lookup);

        /* allocazione e inizializzazione del reticolo */
        int *lattice;
        lattice = create_lattice(params[i].L);
        initialize_lattice(params[i].L, lattice);

        /* apro il file out_path in scrittura */
        FILE *fp = fopen(out_path, "w");
        if (!fp) {
            perror("Errore apertura file di output");
            exit(EXIT_FAILURE);
        }

        /* loop Metropolis, salto i primi tau_exp speps e poi salvo i valori di m solo ogni L^2 steps */
        for(j = 0; j < tau_exp; j++) {
            metropolis_sweep(lattice, params[i].L, params[i].beta, p_lookup);
        }

        for(j = tau_exp; j < T; j++) {
            metropolis_sweep(lattice, params[i].L, params[i].beta, p_lookup);
            if((j-tau_exp) % (params[i].L * params[i].L) == 0){
                /* si calcola m ed e si salvano sul txt corrispondente */
                m = compute_magnetization_volume(lattice, params[i].L);
                e = compute_energy_per_spin(lattice, params[i].L);
                fprintf(fp, "%d\t%.6f\t%.6f\n", j, m, e);  /* salva lo step, m ed e */
            }
        }

        fclose(fp);
        free_lattice(&lattice);
        }


    free(params);
    return 0;
}