// funzioni per utilizzare il generatore di numeri random

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "random.h"
#include "pcg32min.h"

#define TWO32 4294967296.0 /* 2^32 */

/* una sola volta all'inizio del programma, serve a inizializzare lo stato interno del generatore */
void random_generator_init(unsigned long int initstate, unsigned long int initseq)
{
    pcg32_srandom_r(&pcg32_random_state, (uint64_t) initstate, (uint64_t) initseq);
}


/* genero un double in [0,1) */
double random_generator_doublenorm_1open(void)
{
    return (double) pcg32_random_r(&pcg32_random_state)  / TWO32;
}

double random_generator_doublenorm_open(void) {
    return (pcg32_random_r(&pcg32_random_state) + 0.5) / TWO32; /* in (0,1) */
}

/* genero interi tra 0 e RAND_MAX */
int random_generator_int(void) {

    return pcg32_random_r(&pcg32_random_state) % (RAND_MAX + 1u);
}

