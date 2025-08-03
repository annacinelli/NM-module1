#include <math.h>
#include <stdint.h>
#include "pcg32min.h"

// *Really* minimal PCG32 code / (c) 2014 M.E. O'Neill / pcg-random.org
// Licensed under Apache License 2.0 (NO WARRANTY, etc. see website)
/* generatore di numeri casuali di alta qualità, chiamato PCG32 */


/* genera un numero casuale a 32 bit (unsigned int); la struttura pcg32_random_t contiene lo stato interno del generatore.
Restituisce un numero casuale a 32 bit (unsigned int), e aggiorna lo stato interno del generatore
usando una funzione non lineare (XOR-shift + rotazione). */
uint32_t pcg32_random_r(pcg32_random_t* rng)
    {
    uint64_t oldstate = rng->state;
    // Advance internal state: la funzione produce il numero usando lo stato precedente
    /* una congruenzia lineare: una formula deterministica che cambia lo stato */
    rng->state = oldstate * 6364136223846793005ULL + (rng->inc|1);
    // Calculate output function (XSH RR), uses old state for max ILP
    uint32_t xorshifted = (uint32_t) ( ((oldstate >> 18u) ^ oldstate) >> 27u );
    uint32_t rot = (uint32_t) ( oldstate >> 59u );
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
    }


/* serve per inizializzare il generatore con un seme iniziale */
void pcg32_srandom_r(pcg32_random_t* rng, uint64_t initstate, uint64_t initseq)
    {
    rng->state = 0U; /* pulisce lo stato iniziale */
    rng->inc = (initseq << 1u) | 1u; /* imposta l'incremento */
    pcg32_random_r(rng);
    rng->state += initstate;
    pcg32_random_r(rng);
    }

// random number internal state
pcg32_random_t pcg32_random_state;