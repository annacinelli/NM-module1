/* main */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "geometry.h"
#include "ising.h"
#include "pcg32min.h"

extern pcg32_random_t pcg32_random_state;

int main(void){
    uint64_t seed = time(NULL);
    uint64_t seq = 1u;           // può essere 1 o altro per sequenze indipendenti

    pcg32_srandom_r(&pcg32_random_state, seed, seq);  // inizializza il generatore

    double p_lookup[5]; /* dichiarazione lookup table */
    initialize_metropolis_lookup(beta, p_lookup);

    return 0;
}