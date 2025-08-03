#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "geometry.h"
#include "random.h"


bool check_spin_values(int *lattice, int L) {
    for (int i = 0; i < L * L; i++) {
        if (lattice[i] != 1 && lattice[i] != -1) {
            return false;
        }
    }
    return true;
}

int main(void) {
    int L = 3, *lattice;

    random_generator_init(42, 54);

    /* tests delle funzizoni: crea il reticolo, lo inizializza e lo svuota */
    printf("Creating lattice...\n");
    lattice = create_lattice(L);
    if (lattice == NULL) {
        fprintf(stderr, "Test failed: lattice allocation returned NULL.\n");
        return EXIT_FAILURE;
    }

    printf("Initializing lattice...\n");
    initialize_lattice(L, lattice);

    printf("Checking spin values...\n");
    if (!check_spin_values(lattice, L)) {
        fprintf(stderr, "Test failed: lattice contains values other than +1 or -1.\n");
        free_lattice(&lattice);
        return EXIT_FAILURE;
    }

    printf("Freeing lattice...\n");
    free_lattice(&lattice);
    if (lattice != NULL) {
        fprintf(stderr, "Test failed: lattice pointer not NULL after free.\n");
        return EXIT_FAILURE;
    }

    printf("Test passed successfully!\n");
    return EXIT_SUCCESS;
}