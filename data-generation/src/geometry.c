// geometry.c
// Inizializza il reticolo LxL con condizioni periodiche al bordo
// e inizializza ogni sito randomicamente a +1 o -1

#include <stdio.h>
#include <stdlib.h>
#include "geometry.h"
#include "random.h"

/* funzioni: allocazione memoria per il reticolo LxL, inizializzazione reticolo, condizioni
periodiche al bordo */

/* restituisce un puntatore a interi; prende L e basta perchè è quadrato: LxL numero di spin del reticolo */
int *create_lattice(int L) {
    int *lattice;
    
    lattice = malloc(L * L * sizeof(int));

    if (lattice == NULL) {
        fprintf(stderr, "Errore: impossibile allocare memoria per un reticolo di dimensioni %d x %d.\n", L, L);
        exit(EXIT_FAILURE);
    }

    return lattice; /* ritorna il puntatore al primo intero allocato*/
}


/* inizializza il reticolo in modo random (+/-1 per i vari siti), ma qualsiasi altra scelta sarebbe andata bene;
non restituisce nulla */
void initialize_lattice(int L, int *lattice) {
    int i, j, r;

    for (i = 0; i < L; i++) {
        for (j = 0; j < L; j++) {
            r = random_generator_int(); /* intero tra 0 e RAND_MAX */
            lattice[i * L + j] = (r % 2 == 0) ? 1 : -1; /* se pari è 1, altrimenti -1; Nota: equivalente a *(lattice + (i * L + j))*/
        }
    }
}

/* Importante: libera la memoria allocata del reticolo; si passa l’indirizzo del puntatore a free_lattice */
void free_lattice(int **lattice) {
    free(*lattice);
    *lattice = NULL;
}