#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "ising.h"
#include "random.h"
#include "geometry.h"

/* tests */
int main(void) {
    int L = 25, *lattice, step;
    double beta = 0.5, p_lookup[4], M, E;

    random_generator_init(4, 54);

    /* creo e inizializzo il reticolo usando le funzioni in geometry.c */
    lattice = create_lattice(L);
    initialize_lattice(L, lattice);

    M = compute_magnetization_volume(lattice, L);
    E = compute_energy_per_spin(lattice, L);

    // Check iniziali: controllo che i valori siano fisicamente sensati
    assert(M >= -1.0 && M <= 1.0);
    assert(E >= -2.0 && E <= 2.0);

    printf("Initial magnetization: %.6f\n", M);
    printf("Initial energy: %.6f\n", E);

    initialize_metropolis_lookup(beta, p_lookup);

    /* 10 sweep di Metropolis */
    for (step = 1; step <= 160; step++) {
        metropolis_sweep(lattice, L, beta, p_lookup);

        M = compute_magnetization_volume(lattice, L);
        E = compute_energy_per_spin(lattice, L);

        assert(M >= -1.0 && M <= 1.0);
        assert(E >= -2.0 && E <= 2.0);

        printf("Step %2d — M: %.6f  E: %.6f\n", step, M, E);
    }

    free_lattice(&lattice);
    return 0;
}
