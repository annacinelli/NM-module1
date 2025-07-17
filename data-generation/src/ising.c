// ising.c
// update Metropolis locale, energia della configurazione

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ising.h"
#include "random.h"

/* una lookup table è un array che contiene valori precalcolati, si calcolano una volta all'inizio della simulazione */
void initialize_metropolis_lookup(double beta, double *p_lookup) {
    int k;

    for (k=1; k <= 4; k++) {
        p_lookup[k] = exp(-2* beta * k);
    }
}

/* calcolo efficiente della differenza di energia delle due configurazioni: E' - E */
int energy_difference(int *lattice, int s_r,  int L, int i, int j){
    int up, down, left, right, S_r;

    /* valori dei 4 vicini, condizioni periodiche: ogni sito ha sempre 4 vicini, anche se si trova su un bordo */
    up = lattice[((i - 1 + L) % L) * L + j];
    down = lattice[((i + 1) % L) * L + j];
    left = lattice[i * L + ((j - 1 + L) % L)];
    right = lattice[i * L + ((j + 1) % L)];

    S_r = up + down + left + right;

    return 2* s_r * S_r; /* ritorna la differenza in energia */

}

/* update Metropolis di tutto il reticolo, uno step di simulazione */
void metropolis_sweep(int *lattice, int L, double beta, double *p_lookup) {
    double epsilon, w;
    int i, j, s_r, trial, k;

    /* scorro (sweep) il reticolo in modo deterministico */
    for (i = 0; i < L; i++) {
        for (j = 0; j < L; j++) {

        /* calcolo un valore di epsilon in (0,1) */
        epsilon = random_generator_doublenorm_open();

        if (epsilon >= 0.5)
           continue; /* sempre accettata la configurazione iniziale */
        else
           trial = (lattice[i*L + j] == -1) ? 1 : -1; /* flip dello spin in posizione i,j */

        k = energy_difference(lattice, trial, L, i, j);
        if (k <= 0)
           lattice[i * L + j] = trial; /* accettata, modifico il reticolo e vado al prossimo punto del lattice */
        else
           w = random_generator_doublenorm_1open(); /* in [0,1) */
           if (p_lookup[k] >= w) 
               lattice[i * L + j] = trial; /* accetto e modifico il reticolo */

        }
    }

}
