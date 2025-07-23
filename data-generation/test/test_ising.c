// funzioni di test per le funzioni in ising.c

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ising.h"
#include "random.h"
#include "geometry.h"


/* controllo che i valori della lookup table siano quelli calcolati tramite esponenziale */
void test_initialize_metropolis_lookup() {
    double beta = 0.5; /* sopra il valore critico */
    double p_lookup[5];
    int k;

    initialize_metropolis_lookup(beta, p_lookup);

    printf("Test initialize_metropolis_lookup:\n");
    for (k = 1; k <= 4; k++) {
        double expected = exp(-2 * beta * k);
        printf("k=%d, p_lookup=%f, expected=%f\n", k, p_lookup[k], expected); /* li stampa per confronto */

        /* fabs(x) è la distanza in valore assoluto per numeri in virgola mobile, 10^-12 è una precisione ottima 
        per test numerici;
        Nota: assert con i double non va bene, il confronto diretto == è rischioso */
        if (fabs(p_lookup[k] - expected) > 1e-12) {
            printf("FAILED: Lookup value incorrect for k=%d\n", k);
            exit(1); /* exit(int status) termina immediatamente il programma, restituendo un codice di uscita (status) al sistema operativo,
                        0 è EXIT_SUCCESS */
        }
    }
    printf("PASSED\n\n");
}


/* prendiamo una configurazione del reticolo e confrontiamo il vaalore k= E' - E atteso e quello ottenuto con la funzione */
void test_energy_difference() {
    int L = 3;
    int lattice[9] = {
        1, -1, 1,
        -1, 1, -1,
        1, -1, 1
    };
    int i = 1, j = 1;
    int s_r = -1; /* valore di trial, flipped */

    int k = energy_difference(lattice, s_r, L, i, j);

    /* S_r = -2, k (dE) = 4 */
    printf("Test energy_difference:\n");
    printf("k (energy difference) = %d, expected = 4\n", k);
    if (k != 4) {
        printf("FAILED: energy_difference returned incorrect value.\n");
        exit(1);
    }
    printf("PASSED\n\n");
}


/* test della funzione di update Metropolis su tutto il reticolo, uno spin alla volta */
void test_metropolis_sweep() {
    int L = 3, i, j, s_r, trial, k;
    int lattice[9];
    int lattice_comparison[9]; /* lattice di comparazione */
    double p_lookup[5], beta = 0.5, epsilon, w;

    /* inizializza il reticolo con tutti gli spin +1, il seed noto del generatore così da riprodurre la stessa sequenza di 
    epsilon e calcola la p_lookup */
    random_generator_init(42, 54);

    for (int i = 0; i < L*L; i++) {
        lattice[i] = 1;
        lattice_comparison[i] = 1;
    }
    initialize_metropolis_lookup(beta, p_lookup);

    printf("Test metropolis_sweep:\n");

    /* applico la funzione da testare */
    metropolis_sweep(lattice, L, beta, p_lookup);

    /* applico la stessa procedura al reticolo di comparazione e vedo se ottengo gli stessi risultati */
    random_generator_init(42, 54);
    for (i = 0; i < L; i++) {
        for (j = 0; j < L; j++) {
        epsilon = random_generator_doublenorm_open();

        if (epsilon >= 0.5)
           continue;
        else
           trial = (lattice_comparison[i*L + j] == -1) ? 1 : -1;

        k = energy_difference(lattice_comparison, trial, L, i, j);
        if (k <= 0)
           lattice_comparison[i * L + j] = trial;
        else
           w = random_generator_doublenorm_1open();
           if (p_lookup[k] >= w) 
               lattice_comparison[i * L + j] = trial;

        }
    }

    printf("Lattice e lattice_comparison dopo uno sweep:\n");
    print_lattice(lattice, L);
    print_lattice(lattice_comparison, L);

    /* confronto automatico */
    for (int i = 0; i < L * L; i++) {
        if (lattice[i] != lattice_comparison[i]) {
            printf("FAILED: lattice[%d] = %d, expected %d\n", i, lattice[i], lattice_comparison[i]);
            exit(1);
        }
    }

    printf("PASSED: metropolis_sweep behaves as expected with fixed seed.\n\n");
}
