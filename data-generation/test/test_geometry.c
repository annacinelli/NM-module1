// funzioni di test per le funzioni in geometry.c

#include <stdio.h>
#include <stdlib.h>
#include <assert.h> /* assert è una macro della libreria <assert.h> in C che serve per debug e test; assert(expr) valuta expr */
#include "geometry.h"


/* prendo un reticolo abbastanza piccolo e testo l'allocazione e la deallocazione della memoria */
void test_create_and_free_lattice() {
    int L = 5;
    int *lattice = create_lattice(L);
    assert(lattice != NULL);

    free_lattice(&lattice);
    assert(lattice == NULL);

    printf("test_create_and_free_lattice passed.\n");
}

/* verifica che ogni spin abbia valore +1 o -1, cioè che l'inizializzazione abbia funzionato correttamente */
void test_initialize_lattice() {
    int L = 5;
    int *lattice = create_lattice(L);
    initialize_lattice(L, lattice);

    for (int i = 0; i < L * L; i++) {
        assert(lattice[i] == 1 || lattice[i] == -1);
    }

    free_lattice(lattice);
    printf("test_initialize_lattice passed.\n");
}


